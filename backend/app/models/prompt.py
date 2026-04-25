import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base


class AIPrompt(Base):
    __tablename__ = "ai_prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_category = Column(String(30), nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    template_text = Column(Text, nullable=False)
    variables = Column(JSONB, default=[])
    language = Column(String(10), default="fr")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
