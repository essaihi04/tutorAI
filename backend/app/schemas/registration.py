"""Registration request schemas (pre-inscription)."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class RegistrationRequestCreate(BaseModel):
    nom: str = Field(..., min_length=2, max_length=80)
    prenom: str = Field(..., min_length=2, max_length=80)
    phone: str = Field(..., min_length=6, max_length=30)
    ville: str = Field(..., min_length=2, max_length=80)
    email: Optional[str] = Field(None, max_length=120)
    niveau: Optional[str] = Field(None, max_length=80)
    promo_code: Optional[str] = Field(None, max_length=80)
    message: Optional[str] = Field(None, max_length=500)

    @field_validator("nom", "prenom", "ville")
    @classmethod
    def _strip(cls, v: str) -> str:
        return v.strip()

    @field_validator("phone")
    @classmethod
    def _clean_phone(cls, v: str) -> str:
        cleaned = "".join(c for c in v if c.isdigit() or c == "+")
        if len(cleaned) < 6:
            raise ValueError("Numéro de téléphone invalide")
        return cleaned


class RegistrationRequestUpdate(BaseModel):
    status: Optional[str] = None   # pending | contacted | activated | rejected
    admin_notes: Optional[str] = None


class RegistrationRequestOut(BaseModel):
    id: str
    nom: str
    prenom: str
    phone: str
    ville: str
    email: Optional[str] = None
    niveau: Optional[str] = None
    promo_code: Optional[str] = None
    message: Optional[str] = None
    status: str
    admin_notes: Optional[str] = None
    contacted_at: Optional[datetime] = None
    activated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
