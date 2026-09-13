from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.schemas.auth import StudentLogin, Token, StudentResponse, RefreshRequest
from app.config import get_settings
from app.dependencies import get_current_student, student_from_token
from app.services.subject_access_service import subject_access_service

router = APIRouter(prefix='/auth', tags=['auth'])
settings = get_settings()


@router.get('/me', response_model=StudentResponse)
async def get_me(student: dict = Depends(get_current_student)):
    return StudentResponse(**student)


@router.get('/learning-context')
async def get_learning_context(student: dict = Depends(get_current_student)):
    return subject_access_service.get_context(student)


@router.post('/register')
async def register():
    # Only administrators create accounts. Public applications use registration-requests.
    raise HTTPException(403, 'Inscription sur validation administrative uniquement')


async def _exchange(grant: str, body: dict) -> Token:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f'{settings.supabase_url}/auth/v1/token',
                params={'grant_type': grant}, headers={'apikey': settings.supabase_anon_key}, json=body)
        if response.status_code >= 400:
            raise HTTPException(401, 'refresh_token_invalid' if grant == 'refresh_token'
                                else 'Identifiants incorrects ou compte non confirme')
        payload = response.json()
        token = payload.get('access_token')
        if not token:
            raise HTTPException(401, 'Authentication failed')
        await student_from_token(token)
        return Token(access_token=token, refresh_token=payload.get('refresh_token'),
                     expires_in=payload.get('expires_in'))
    except HTTPException:
        raise
    except httpx.TimeoutException as exc:
        raise HTTPException(504, 'Service de connexion temporairement indisponible') from exc
    except Exception as exc:
        raise HTTPException(401, 'Authentication failed') from exc


@router.post('/login', response_model=Token)
async def login(data: StudentLogin):
    return await _exchange('password', {'email': data.email, 'password': data.password})


@router.post('/refresh', response_model=Token)
async def refresh_token(data: RefreshRequest):
    return await _exchange('refresh_token', {'refresh_token': data.refresh_token})
