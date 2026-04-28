from fastapi import APIRouter
from app.api.v1.endpoints import auth, content, sessions, coaching, libre, exam, admin, exam_extraction, registration, mock_exam
from app.api import resources

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(content.router)
api_router.include_router(sessions.router)
api_router.include_router(coaching.router)
api_router.include_router(libre.router)
api_router.include_router(exam.router)
api_router.include_router(admin.router)
api_router.include_router(exam_extraction.router)
api_router.include_router(registration.public_router)
api_router.include_router(registration.admin_router)
api_router.include_router(mock_exam.router)

# Admin resources management
api_router.include_router(resources.router, prefix="/admin-resources", tags=["admin-resources"])
