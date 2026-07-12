from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ContentLibraryItem(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    content_id: str = Field(min_length=1)
    content_type: str = Field(min_length=1)

    marketing_angle: str = Field(min_length=1)
    psychology: str = Field(min_length=1)
    objective: str = Field(min_length=1)

    hook_instruction: str = Field(min_length=1)

    content_structure: str = Field(min_length=1)

    cta_style: str = Field(min_length=1)