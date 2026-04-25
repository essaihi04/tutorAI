"""Admin API schemas."""
from pydantic import BaseModel
from typing import Optional


class AdminLogin(BaseModel):
    password: str


class CreateUser(BaseModel):
    email: str
    password: str
    full_name: str
    username: str
    promo_code: Optional[str] = None
    is_admin: bool = False


class UpdateUser(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    preferred_language: Optional[str] = None
    promo_code: Optional[str] = None


class ResetPassword(BaseModel):
    new_password: str


class CreatePromoCode(BaseModel):
    code: str
    label: Optional[str] = None
    is_active: bool = True


class UpdatePromoCode(BaseModel):
    label: Optional[str] = None
    is_active: Optional[bool] = None
