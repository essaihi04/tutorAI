from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.supabase_client import get_supabase
from jose import jwt, JWTError
from app.config import get_settings

security = HTTPBearer()
settings = get_settings()


def _expired_error() -> HTTPException:
    """401 that tells the frontend to call /auth/refresh and retry."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token_expired",
        headers={"WWW-Authenticate": 'Bearer error="invalid_token", error_description="The access token expired"'},
    )


async def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    supabase = get_supabase()

    try:
        # Verify token with Supabase Auth
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise _expired_error()

        user_id = user_response.user.id

        # Get student from database
        result = supabase.table('students').select('*').eq('id', str(user_id)).execute()

        if not result.data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Student not found")

        student = result.data[0]

        # Block expired test accounts
        expires_at = student.get("expires_at")
        if expires_at:
            from datetime import datetime as _dt
            try:
                exp = _dt.fromisoformat(expires_at.replace("Z", "+00:00"))
                if _dt.now(exp.tzinfo) > exp:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="account_expired",
                    )
            except HTTPException:
                raise
            except Exception:
                pass  # malformed date → let through, don't block

        return student

    except HTTPException:
        raise
    except Exception as e:
        err = str(e).lower()
        # Supabase / GoTrue / PostgREST all raise these phrasings when the JWT is expired
        if any(tok in err for tok in ("expired", "jwt expired", "invalid jwt", "invalid claims")):
            raise _expired_error()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )
