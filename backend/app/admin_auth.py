"""Authentication for every administrative API; no built-in credentials."""
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from app.config import get_settings

_security = HTTPBearer()
_settings = get_settings()


def admin_signing_key() -> str:
    if (len(_settings.secret_key) < 32
            or _settings.secret_key == 'your-secret-key-change-in-production'
            or len(_settings.admin_password) < 9
            or _settings.admin_password.lower() in {'admin123', 'password123', '123456789'}):
        raise HTTPException(503, 'Administration non configuree de maniere securisee')
    # Changing the password also revokes previously issued admin tokens.
    return hmac.new(_settings.secret_key.encode(),
                    b'moalim-admin-v2:' + _settings.admin_password.encode(), hashlib.sha256).hexdigest()


def create_admin_token() -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({
        'sub': 'admin', 'role': 'admin', 'iss': 'moalim', 'aud': 'moalim-admin',
        'iat': now, 'exp': now + timedelta(minutes=_settings.admin_token_expire_minutes),
    }, admin_signing_key(), algorithm='HS256')


def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(_security)) -> bool:
    key = admin_signing_key()
    try:
        payload = jwt.decode(credentials.credentials, key, algorithms=['HS256'],
            audience='moalim-admin', issuer='moalim',
            options={'require': ['exp', 'iat', 'sub', 'aud', 'iss']})
        if payload.get('sub') != 'admin' or payload.get('role') != 'admin':
            raise ValueError('Invalid role')
        return True
    except Exception as exc:
        raise HTTPException(401, 'Invalid or expired admin token') from exc
