from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import StudentRegister, StudentLogin, Token, StudentResponse, RefreshRequest
from app.supabase_client import get_supabase
from app.config import get_settings
from app.dependencies import get_current_student
from datetime import datetime
import uuid
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])
supabase = get_supabase()
settings = get_settings()


@router.get("/me", response_model=StudentResponse)
async def get_me(student: dict = Depends(get_current_student)):
    """Return the currently-authenticated student."""
    return StudentResponse(**student)


@router.post("/register", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def register(data: StudentRegister):
    try:
        # Check if email already exists
        existing_email = supabase.table('students').select('id').eq('email', data.email).execute()
        if existing_email.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        existing_username = supabase.table('students').select('id').eq('username', data.username).execute()
        if existing_username.data:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Sign up user with Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        # Create student record in database
        student_data = {
            "id": str(auth_response.user.id),
            "username": data.username,
            "email": data.email,
            "full_name": data.full_name,
            "preferred_language": data.preferred_language,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        student_response = supabase.table('students').insert(student_data).execute()
        
        if not student_response.data:
            raise HTTPException(status_code=500, detail="Failed to create student record")
        
        student = student_response.data[0]
        
        # Create student profile
        profile_data = {
            "id": str(uuid.uuid4()),
            "student_id": student['id'],
            "proficiency_level": "intermediate",
            "learning_style": "Socratique",
            "strengths": [],
            "weaknesses": [],
            "total_study_time_minutes": 0,
            "sessions_completed": 0,
            "exercises_completed": 0,
            "average_score": 0.0,
        }
        
        supabase.table('student_profiles').insert(profile_data).execute()
        
        return StudentResponse(**student)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=Token)
async def login(data: StudentLogin):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.supabase_url}/auth/v1/token?grant_type=password",
                headers={
                    "apikey": settings.supabase_anon_key,
                    "Content-Type": "application/json",
                },
                json={
                    "email": data.email,
                    "password": data.password,
                },
            )

        if response.status_code >= 400:
            error_payload = response.json() if response.content else {}
            error_message = str(
                error_payload.get("msg")
                or error_payload.get("message")
                or error_payload.get("error_description")
                or error_payload.get("error")
                or ""
            )
            lowered_error = error_message.lower()

            if "email not confirmed" in lowered_error or "email non confirmé" in lowered_error:
                raise HTTPException(status_code=401, detail="Email non confirmé. Vérifiez votre boîte mail ou activez la confirmation automatique dans Supabase.")

            if "invalid login credentials" in lowered_error or "invalid credentials" in lowered_error:
                raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

            raise HTTPException(status_code=401, detail=f"Échec de connexion: {error_message or response.text}")

        payload = response.json()
        access_token = payload.get("access_token")

        if not access_token:
            raise HTTPException(status_code=401, detail="Échec de connexion: token manquant")

        return Token(
            access_token=access_token,
            refresh_token=payload.get("refresh_token"),
            expires_in=payload.get("expires_in"),
        )

    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Le service de connexion met trop de temps à répondre. Réessayez dans quelques secondes.")
    except Exception as e:
        error_message = str(e)
        if "Email not confirmed" in error_message:
            raise HTTPException(status_code=401, detail="Email non confirmé. Vérifiez votre boîte mail ou activez la confirmation automatique dans Supabase.")
        if "Invalid login credentials" in error_message:
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        raise HTTPException(status_code=401, detail=f"Échec de connexion: {error_message}")


@router.post("/refresh", response_model=Token)
async def refresh_token(data: RefreshRequest):
    """Exchange a refresh_token for a new access_token + refresh_token pair.

    The frontend should call this when it receives a 401 with detail=="token_expired",
    then retry the original request with the fresh access_token.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.supabase_url}/auth/v1/token?grant_type=refresh_token",
                headers={
                    "apikey": settings.supabase_anon_key,
                    "Content-Type": "application/json",
                },
                json={"refresh_token": data.refresh_token},
            )

        if response.status_code >= 400:
            # The refresh token itself is expired/revoked — the user must re-login
            raise HTTPException(
                status_code=401,
                detail="refresh_token_invalid",
            )

        payload = response.json()
        access_token = payload.get("access_token")
        if not access_token:
            raise HTTPException(status_code=401, detail="refresh_token_invalid")

        return Token(
            access_token=access_token,
            refresh_token=payload.get("refresh_token"),
            expires_in=payload.get("expires_in"),
        )

    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Refresh timeout")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"refresh_failed: {str(e)}")
