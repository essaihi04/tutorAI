from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.supabase_client import get_supabase
from starlette.concurrency import run_in_threadpool

security = HTTPBearer()


def _expired_error() -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token_expired',
        headers={'WWW-Authenticate': 'Bearer error="invalid_token"'})


def ensure_student_active(student: dict) -> dict:
    if student.get('is_active') is not True:
        raise HTTPException(403, 'account_disabled')
    expires_at = student.get('expires_at')
    if expires_at:
        try:
            expiry = datetime.fromisoformat(str(expires_at).replace('Z', '+00:00'))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
        except (TypeError, ValueError) as exc:
            raise HTTPException(403, 'account_expired') from exc
        if datetime.now(timezone.utc) >= expiry:
            raise HTTPException(403, 'account_expired')
    return student


def _lookup_student(token: str) -> dict:
    sb = get_supabase()
    try:
        response = sb.auth.get_user(token)
        if not response or not response.user:
            raise _expired_error()
        result = sb.table('students').select('*').eq('id', str(response.user.id)).execute()
        if not result.data:
            raise HTTPException(401, 'Student not found')
        return ensure_student_active(result.data[0])
    except HTTPException:
        raise
    except Exception as exc:
        if 'expired' in str(exc).lower():
            raise _expired_error() from exc
        raise HTTPException(401, 'Authentication failed') from exc


async def student_from_token(token: str) -> dict:
    if not isinstance(token, str) or not token or len(token) > 8192:
        raise HTTPException(401, 'Authentication failed')
    return await run_in_threadpool(_lookup_student, token)


async def get_current_student(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    return await student_from_token(credentials.credentials)
