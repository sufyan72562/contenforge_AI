from pydantic import ValidationError

from app.core.config import get_settings
from app.integrations.google.key_value_parser import (
    GoogleSheetKeyValueParser,
)
from app.integrations.google.range_builder import (
    GoogleSheetRangeBuilder,
)
from app.integrations.google.client import GoogleSheetsClient
from app.schemas.brand_memory import BrandMemory


class BrandMemoryRepository:

    def __init__(self):

        self.settings = get_settings()

        self.client = GoogleSheetsClient()

        self.parser = GoogleSheetKeyValueParser()

    async def get_brand_memory(
        self,
    ) -> BrandMemory:

        range_name = GoogleSheetRangeBuilder.build(
            self.settings.brand_memory_sheet_name,
            self.settings.brand_memory_sheet_columns,
        )

        rows = await self.client.read_range(
            spreadsheet_id=self.settings.google_spreadsheet_id,
            range_name=range_name,
        )

        data = self.parser.parse(rows)

        try:

            return BrandMemory.model_validate(data)

        except ValidationError as exc:

            raise ValueError(
                f"Invalid Brand Memory Sheet\n{exc}"
            ) from exc