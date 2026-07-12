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
from app.repositories.exceptions import (
    ProductKnowledgeRepositoryError,
)
from app.schemas.product_knowledge import ProductKnowledge


class ProductKnowledgeRepository:
    def __init__(
        self,
        sheets_client: GoogleSheetsClient | None = None,
        table_parser: GoogleSheetTableParser | None = None,
        settings: Settings | None = None,
    ) -> None:
        self._sheets_client = sheets_client or GoogleSheetsClient()
        self._table_parser = table_parser or GoogleSheetTableParser()
        self._settings = settings or get_settings()

    async def list_products(self) -> list[ProductKnowledge]:
        range_name = GoogleSheetRangeBuilder.build(
            sheet_name=self._settings.product_sheet_name,
            cell_range=self._settings.product_sheet_columns,
        )

        try:
            raw_rows = await self._sheets_client.read_range(
                spreadsheet_id=self._settings.google_spreadsheet_id,
                range_name=range_name,
            )

            parsed_rows = self._table_parser.parse(raw_rows)

            products: list[ProductKnowledge] = []

            for row_number, row in enumerate(parsed_rows, start=2):
                try:
                    products.append(ProductKnowledge.model_validate(row))

                except ValidationError as exc:
                    raise ProductKnowledgeRepositoryError(
                        f"Invalid product data at sheet row {row_number}: "
                        f"{exc.errors()}"
                    ) from exc

            return products

        except ProductKnowledgeRepositoryError:
            raise

        except Exception as exc:
            raise ProductKnowledgeRepositoryError(
                "Could not load product knowledge."
            ) from exc

    async def get_product_by_id(
        self,
        product_id: str,
    ) -> ProductKnowledge | None:
        normalized_product_id = product_id.strip().upper()

        if not normalized_product_id:
            raise ValueError("product_id cannot be empty.")

        products = await self.list_products()

        for product in products:
            if product.product_id == normalized_product_id:
                return product

        return None