"""Validated payloads used by the unified admin visual library."""

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


VisualLibraryKind = Literal["image", "video", "simulation", "scientific"]
VisualLibraryStatus = Literal["draft", "validated", "published", "archived"]


class AdminVisualItemCreate(BaseModel):
    lesson_id: str = Field(min_length=1)
    kind: VisualLibraryKind
    title: str = Field(min_length=2, max_length=180)
    description: str = Field(default="", max_length=1200)
    section_title: str = Field(default="Bibliothèque visuelle", max_length=180)
    file_path: Optional[str] = Field(default=None, max_length=1200)
    external_url: Optional[str] = Field(default=None, max_length=1200)
    trigger_text: Optional[str] = Field(default=None, max_length=400)
    phase: str = Field(default="explanation", max_length=40)
    difficulty_tier: str = Field(default="intermediate", max_length=40)
    concepts: list[str] = Field(default_factory=list, max_length=30)
    status: VisualLibraryStatus = "draft"
    scientific: Optional[dict[str, Any]] = None
    source: str = Field(default="admin", max_length=40)


class AdminVisualItemUpdate(BaseModel):
    lesson_id: Optional[str] = Field(default=None, min_length=1)
    kind: Optional[VisualLibraryKind] = None
    title: Optional[str] = Field(default=None, min_length=2, max_length=180)
    description: Optional[str] = Field(default=None, max_length=1200)
    section_title: Optional[str] = Field(default=None, max_length=180)
    file_path: Optional[str] = Field(default=None, max_length=1200)
    external_url: Optional[str] = Field(default=None, max_length=1200)
    trigger_text: Optional[str] = Field(default=None, max_length=400)
    phase: Optional[str] = Field(default=None, max_length=40)
    difficulty_tier: Optional[str] = Field(default=None, max_length=40)
    concepts: Optional[list[str]] = Field(default=None, max_length=30)
    status: Optional[VisualLibraryStatus] = None
    scientific: Optional[dict[str, Any]] = None


class AdminVisualGenerate(BaseModel):
    prompt: str = Field(min_length=8, max_length=4000)
    subject: str = Field(default="", max_length=80)
    lesson_id: Optional[str] = None
    title: Optional[str] = Field(default=None, max_length=180)
    engine: Literal["auto", "roughsvg", "jsxgraph", "cytoscape", "matter", "three"] = "auto"
    mode: Literal["create", "edit"] = "create"
    current_spec: Optional[dict[str, Any]] = None
