from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductKnowledge(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    product_id: str = Field(min_length=1)
    product_name: str = Field(min_length=1)
    subtitle: str
    category: str
    size: str
    skin_type: str
    concerns: str
    main_purpose: str
    short_description: str
    key_benefits: str
    hero_ingredients: str
    full_ingredients: str
    usage: str
    recommended_time: str
    texture: str
    finish: str
    keywords: str
    warnings: str
    image_url: str = ""
    product_status: str = "active"

    @field_validator("product_id")
    @classmethod
    def normalize_product_id(cls, value: str) -> str:
        return value.upper()

    @field_validator("product_status")
    @classmethod
    def normalize_product_status(cls, value: str) -> str:
        return value.lower()

    @property
    def benefits_list(self) -> list[str]:
        return self._split_values(self.key_benefits)

    @property
    def hero_ingredients_list(self) -> list[str]:
        return self._split_values(self.hero_ingredients)

    @property
    def concerns_list(self) -> list[str]:
        return self._split_values(self.concerns)

    @property
    def keywords_list(self) -> list[str]:
        return self._split_values(self.keywords)

    @staticmethod
    def _split_values(value: str) -> list[str]:
        if not value:
            return []

        return [
            item.strip()
            for item in value.replace("|", ",").split(",")
            if item.strip()
        ]