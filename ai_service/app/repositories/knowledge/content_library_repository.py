from __future__ import annotations

from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.integrations.google.range_builder import (
    GoogleSheetRangeBuilder,
)
from app.integrations.google.client import GoogleSheetsClient
from app.integrations.google.table_parser import (
    GoogleSheetTableParser,
)
from app.schemas.content_library import (
    ContentLibraryItem,
)


class ContentLibraryRepository:

    def __init__(
        self,
        sheets_client: GoogleSheetsClient | None = None,
        table_parser: GoogleSheetTableParser | None = None,
        settings: Settings | None = None,
    ) -> None:

        self._client = sheets_client or GoogleSheetsClient()
        self._parser = table_parser or GoogleSheetTableParser()
        self._settings = settings or get_settings()

    async def list_content(
        self,
    ) -> list[ContentLibraryItem]:

        range_name = GoogleSheetRangeBuilder.build(
            self._settings.content_library_sheet_name,
            self._settings.content_library_sheet_columns,
        )

        rows = await self._client.read_range(
            spreadsheet_id=self._settings.google_spreadsheet_id,
            range_name=range_name,
        )

        parsed_rows = self._parser.parse(rows)

        content_items: list[ContentLibraryItem] = []

        for row_number, row in enumerate(parsed_rows, start=2):

            try:
                content_items.append(
                    ContentLibraryItem.model_validate(row)
                )

            except ValidationError as exc:

                raise ValueError(
                    f"Invalid Content Library row {row_number}\n{exc}"
                ) from exc

        return content_items