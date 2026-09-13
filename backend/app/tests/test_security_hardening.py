"""Regression tests for the attack paths identified on 2026-09-09.

All data and authentication calls are replaced with local fakes. These tests
never create users, contact providers, or modify the production database.
"""
import asyncio
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient
import jwt

from app import admin_auth, dependencies
from app.api.v1.endpoints import auth, exam_extraction, tts
from app.config import Settings
from app.security_middleware import SecurityMiddleware
from app.utils.safe_paths import safe_child_path


@pytest.fixture
def admin_settings(monkeypatch):
    settings = SimpleNamespace(secret_key='s' * 48, admin_password='strong-test-password-123',
                               admin_token_expire_minutes=60)
    monkeypatch.setattr(admin_auth, '_settings', settings)
    return settings


def bearer(token):
    return HTTPAuthorizationCredentials(scheme='Bearer', credentials=token)


def test_valid_admin_and_password_rotation(admin_settings):
    token = admin_auth.create_admin_token()
    assert admin_auth.verify_admin_token(bearer(token)) is True
    admin_settings.admin_password = 'another-strong-test-password-456'
    with pytest.raises(HTTPException) as exc:
        admin_auth.verify_admin_token(bearer(token))
    assert exc.value.status_code == 401


@pytest.mark.parametrize('change', [
    {'exp': None}, {'aud': 'student'}, {'iss': 'attacker'}, {'sub': 'student'},
    {'role': 'student'}, {'exp': 1}, {'iat': None},
])
def test_incomplete_or_wrong_admin_claims_denied(admin_settings, change):
    now = datetime.now(timezone.utc)
    claims = {'sub': 'admin', 'role': 'admin', 'iss': 'moalim', 'aud': 'moalim-admin',
              'iat': now, 'exp': now + timedelta(hours=1)}
    for key, value in change.items():
        if value is None:
            claims.pop(key)
        else:
            claims[key] = value
    token = jwt.encode(claims, admin_auth.admin_signing_key(), algorithm='HS256')
    with pytest.raises(HTTPException):
        admin_auth.verify_admin_token(bearer(token))


@pytest.mark.parametrize('password', ['', 'admin123', '123456789', 'password123'])
def test_default_admin_credentials_disabled(admin_settings, password):
    admin_settings.admin_password = password
    with pytest.raises(HTTPException) as exc:
        admin_auth.create_admin_token()
    assert exc.value.status_code == 503


@pytest.mark.parametrize('student', [
    {}, {'is_active': False}, {'is_active': True, 'expires_at': 'bad-date'},
    {'is_active': True, 'expires_at': '2020-01-01T00:00:00'},
    {'is_active': True, 'expires_at': '2020-01-01T00:00:00Z'},
])
def test_disabled_or_expired_accounts_denied(student):
    with pytest.raises(HTTPException) as exc:
        dependencies.ensure_student_active(student)
    assert exc.value.status_code == 403


def test_active_owner_account_remains_available():
    student = {'id': 'owner', 'is_active': True, 'expires_at': None}
    assert dependencies.ensure_student_active(student) is student


def test_valid_auth_user_still_requires_active_student(monkeypatch):
    sb = Mock()
    sb.auth.get_user.return_value = SimpleNamespace(user=SimpleNamespace(id='blocked'))
    sb.table.return_value.select.return_value.eq.return_value.execute.return_value = SimpleNamespace(data=[{'is_active': False}])
    monkeypatch.setattr(dependencies, 'get_supabase', lambda: sb)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(dependencies.student_from_token('previously-valid-token'))
    assert exc.value.status_code == 403


def test_registration_cannot_create_a_user(monkeypatch):
    sb = Mock(side_effect=AssertionError('No database call should be made'))
    monkeypatch.setattr(dependencies, 'get_supabase', sb)
    app = FastAPI()
    app.include_router(auth.router)
    with TestClient(app) as client:
        response = client.post('/auth/register', json={'email': 'fake@example.com', 'password': 'long-test-password'})
    assert response.status_code == 403
    sb.assert_not_called()


@pytest.mark.parametrize('method,path', [
    ('POST', '/exam-extract/ocr-page'), ('POST', '/exam-extract/detect-zones'),
    ('POST', '/exam-extract/describe-doc'), ('POST', '/exam-extract/publish'),
    ('POST', '/exam-extract/structure-exam'), ('GET', '/exam-extract/published-exams'),
    ('DELETE', '/exam-extract/published-exams/example'),
    ('PUT', '/exam-extract/published-exams/example'), ('POST', '/tts/speak'),
])
def test_sensitive_endpoints_deny_anonymous_before_work(method, path):
    app = FastAPI()
    app.include_router(exam_extraction.router)
    app.include_router(tts.router)
    with TestClient(app) as client:
        response = client.request(method, path, json={})
    assert response.status_code in (401, 403)


def test_student_token_cannot_manage_exams(admin_settings):
    token = jwt.encode({'sub': 'student', 'role': 'authenticated', 'exp': 9999999999},
                       'different-student-signing-key', algorithm='HS256')
    app = FastAPI()
    app.include_router(exam_extraction.router)
    with TestClient(app) as client:
        assert client.get('/exam-extract/published-exams', headers={'Authorization': 'Bearer ' + token}).status_code == 401


def rate_app():
    app = FastAPI()
    app.add_middleware(SecurityMiddleware)
    @app.post('/api/v1/admin/login')
    async def login():
        return {'ok': True}
    return app


def test_brute_force_limit_cannot_be_spoofed_with_forwarded_headers():
    with TestClient(rate_app()) as client:
        for i in range(8):
            assert client.post('/api/v1/admin/login', json={}, headers={'X-Forwarded-For': f'192.0.2.{i}'}).status_code == 200
        response = client.post('/api/v1/admin/login', json={}, headers={'X-Forwarded-For': '192.0.2.99'})
        assert response.status_code == 429
        assert int(response.headers['retry-after']) > 0


def test_body_limit_including_chunked_requests():
    with TestClient(rate_app()) as client:
        response = client.post('/api/v1/admin/login', content=iter([b'x' * (1024 * 1024), b'x']))
        assert response.status_code == 413


def test_limiter_expires_and_bounds_memory():
    now = [0.0]
    limiter = SecurityMiddleware(None, max_clients=10, clock=lambda: now[0])
    assert limiter.limited('a', 1, 60) == 0
    assert limiter.limited('a', 1, 60) > 0
    now[0] = 61
    assert limiter.limited('a', 1, 60) == 0
    for i in range(100):
        limiter.limited(i, 1, 60)
    assert len(limiter.buckets) == 10


@pytest.mark.parametrize('parts', [('../outside',), ('/etc/passwd',), ('C:/Windows',),
                                   ('..\\outside',), ('svt', '../../outside'), ('.',)])
def test_path_escape_denied(tmp_path, parts):
    with pytest.raises(HTTPException):
        safe_child_path(tmp_path, *parts)


def test_normal_path_allowed(tmp_path):
    assert safe_child_path(tmp_path, 'svt', '2026-normale', 'exam.json') == tmp_path / 'svt/2026-normale/exam.json'


def test_cors_never_accepts_wildcard():
    settings = Settings(_env_file=None, cors_origins='*,https://moalim.online, https://www.moalim.online/')
    assert settings.allowed_origins == ['https://moalim.online', 'https://www.moalim.online']


def socket_app(monkeypatch):
    from app.websockets import security as socket_security
    async def lookup(token):
        if token == 'blocked':
            raise HTTPException(403, 'account_disabled')
        return {'id': 'intruder' if token == 'other-account' else 'owner', 'is_active': True}
    monkeypatch.setattr(socket_security, 'student_from_token', lookup)
    app = FastAPI()
    from starlette.websockets import WebSocket, WebSocketDisconnect
    @app.websocket('/socket')
    async def echo(websocket: WebSocket):
        socket_security.protect_tutor_socket(websocket, 'owner', 'initial')
        await websocket.accept()
        try:
            while True:
                frame = await websocket.receive()
                if frame['type'] == 'websocket.disconnect':
                    break
                await websocket.send_json({'text': frame.get('text'), 'audio': bool(frame.get('bytes'))})
        except WebSocketDisconnect:
            pass
    return app, socket_security


def test_websocket_refresh_preserves_session_and_does_not_reach_tutor(monkeypatch):
    app, _ = socket_app(monkeypatch)
    with TestClient(app).websocket_connect('/socket') as ws:
        ws.send_json({'type': 'auth_refresh', 'token': 'refreshed'})
        ws.send_text('continue lesson')
        assert ws.receive_json()['text'] == 'continue lesson'
        ws.send_bytes(b'audio')
        assert ws.receive_json()['audio'] is True


@pytest.mark.parametrize('token', ['other-account', 'blocked', None, {'fake': 'token'}])
def test_websocket_refresh_cannot_switch_account_or_restore_banned_access(monkeypatch, token):
    from starlette.websockets import WebSocketDisconnect
    app, _ = socket_app(monkeypatch)
    with TestClient(app).websocket_connect('/socket') as ws:
        ws.send_json({'type': 'auth_refresh', 'token': token})
        with pytest.raises(WebSocketDisconnect) as exc:
            ws.receive_json()
        assert exc.value.code == 4001


def test_existing_socket_checks_revocation_on_raw_text_frames(monkeypatch):
    from starlette.websockets import WebSocketDisconnect
    app, socket_security = socket_app(monkeypatch)
    async def blocked(token):
        raise HTTPException(403, 'account_disabled')
    with TestClient(app).websocket_connect('/socket') as ws:
        monkeypatch.setattr(socket_security, 'student_from_token', blocked)
        ws.send_text('paid work')
        with pytest.raises(WebSocketDisconnect):
            ws.receive_json()


def test_existing_socket_checks_revocation_on_binary_audio(monkeypatch):
    from starlette.websockets import WebSocketDisconnect
    app, socket_security = socket_app(monkeypatch)
    async def blocked(token):
        raise HTTPException(403, 'account_disabled')
    with TestClient(app).websocket_connect('/socket') as ws:
        monkeypatch.setattr(socket_security, 'student_from_token', blocked)
        ws.send_bytes(b'audio')
        with pytest.raises(WebSocketDisconnect):
            ws.receive_json()


def test_static_routes_never_serve_drafts_or_scripts(tmp_path):
    from app.public_media import PublicMediaFiles
    (tmp_path / 'exam.json').write_text('{"secret":"draft"}')
    (tmp_path / 'payload.html').write_text('<script>alert(1)</script>')
    (tmp_path / 'figure.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
    app = FastAPI()
    app.mount('/static', PublicMediaFiles(directory=tmp_path))
    with TestClient(app) as client:
        assert client.get('/static/exam.json').status_code == 404
        assert client.get('/static/payload.html').status_code == 404
        response = client.get('/static/figure.svg')
        assert response.status_code == 200
        assert response.headers['x-content-type-options'] == 'nosniff'
        assert response.headers['content-security-policy'].startswith('sandbox;')


@pytest.mark.parametrize('doc_id', ['*', 'image?', '[ab]', '../outside', '..\\outside', ''])
def test_image_deletion_rejects_wildcards_and_traversal(monkeypatch, doc_id):
    from app.api.v1.endpoints import mock_exam
    lookup = Mock()
    monkeypatch.setattr(mock_exam.mock_exam_service, 'get_mock_exam', lookup)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(mock_exam.delete_image('svt', 'exam-1', doc_id, admin=True))
    assert exc.value.status_code == 400
    lookup.assert_not_called()


def test_student_photo_requests_are_bounded_without_rejecting_normal_photos():
    from fastapi import Request
    app = FastAPI()
    app.add_middleware(SecurityMiddleware)

    @app.post('/api/v1/exam/extract-text')
    async def photo(request: Request):
        return {'size': len(await request.body())}

    with TestClient(app) as client:
        normal = b'x' * (2 * 1024 * 1024)
        response = client.post('/api/v1/exam/extract-text', content=normal)
        assert response.status_code == 200
        assert response.json()['size'] == len(normal)
        assert client.post('/api/v1/exam/extract-text', content=b'x' * (8 * 1024 * 1024 + 1)).status_code == 413
