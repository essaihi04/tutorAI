from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID


class StudentRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    preferred_language: str = "fr"


class StudentLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None  # seconds before access_token expires


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    student_id: Optional[str] = None


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    username: str
    email: str
    full_name: str
    preferred_language: str
    is_active: bool
