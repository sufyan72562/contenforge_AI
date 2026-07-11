from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_service_account_file: Path

    google_spreadsheet_id: str = Field(min_length=1)

    product_sheet_name: str = "products"
    product_sheet_columns: str = "A:Z"

    brand_memory_sheet_name: str = "brand_memory"
    brand_memory_sheet_columns: str = "A:B"

    content_library_sheet_name: str = "content_library"
    content_library_sheet_columns: str = "A:Z"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()