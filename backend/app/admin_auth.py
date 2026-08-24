"""Shared authentication dependency for every administrative API.

Keeping this outside an endpoint module prevents feature routers from importing
each other just to reuse the admin JWT verifier.
"""

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from app.config import get_settings


_security = HTTPBearer()
_settings = get_settings()
_ADMIN_JWT_SECRET = _settings.secret_key + "_admin"
_ADMIN_TOKEN_EXPIRE_HOURS = 24


def create_admin_token() -> str:
    payload = {
        "sub": "admin",
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(hours=_ADMIN_TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, _ADMIN_JWT_SECRET, algorithm="HS256")


def verify_admin_token(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
) -> bool:
    try:
        payload = jwt.decode(
            credentials.credentials,
            _ADMIN_JWT_SECRET,
            algorithms=["HS256"],
        )
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not an admin token")
        return True
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired admin token",
        ) from exc
