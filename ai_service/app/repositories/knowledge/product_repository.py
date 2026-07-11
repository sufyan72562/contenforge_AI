from __future__ import annotations


from app.core.config import Settings, get_settings
from app.integrations.google.range_builder import (
    GoogleSheetRangeBuilder,
)
from app.integrations.google.client import GoogleSheetsClient
from app.integrations.google.table_parser import (
    GoogleSheetTableParser,
)
from app.repositories.exceptions import (
    ProductKnowledgeRepositoryError,
)


class ProductKnowledgeRepository:
    """
    Loads product knowledge from Google Sheets.

    Responsibilities:
    - Know the configured product sheet.
    - Build the product sheet range.
    - Fetch raw product rows.
    - Parse rows into dictionaries.

    This repository does not:
    - Generate LangChain documents.
    - Generate embeddings.
    - Contain prompt logic.
    """

    def __init__(
        self,
        sheets_client: GoogleSheetsClient | None = None,
        table_parser: GoogleSheetTableParser | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._sheets_client = (
            sheets_client or GoogleSheetsClient()
        )
        self._table_parser = (
            table_parser or GoogleSheetTableParser()
        )
        self._settings = settings or get_settings()

    async def list_products(self) -> list[dict[str, str]]:
        range_name = GoogleSheetRangeBuilder.build(
            sheet_name=self._settings.product_sheet_name,
            cell_range=self._settings.product_sheet_columns,
        )

        try:
            raw_rows = await self._sheets_client.read_range(
                spreadsheet_id=self._settings.google_spreadsheet_id,
                range_name=range_name,
            )

            return self._table_parser.parse(raw_rows)

        except Exception as exc:
            raise ProductKnowledgeRepositoryError(
                "Could not load product knowledge."
            ) from exc

    async def get_product_by_id(
        self,
        product_id: str,
    ) -> dict[str, str] | None:
        normalized_product_id = product_id.strip().upper()

        if not normalized_product_id:
            raise ValueError("product_id cannot be empty.")

        products = await self.list_products()

        for product in products:
            current_product_id = (
                product.get("product_id", "")
                .strip()
                .upper()
            )

            if current_product_id == normalized_product_id:
                return product

        return None