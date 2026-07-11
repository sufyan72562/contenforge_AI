from fastapi import FastAPI, HTTPException

from app.core.config import get_settings
from app.integrations.google.exceptions import GoogleSheetsError
from app.integrations.google.client import GoogleSheetsClient


app = FastAPI(title="ContentForge AI Service")


@app.get("/test/google-sheet")
async def test_google_sheet() -> dict:
    settings = get_settings()
    client = GoogleSheetsClient()

    try:
        rows = await client.read_range(
            spreadsheet_id=settings.google_spreadsheet_id,
            range_name="products!A:Z",
        )

        return {
            "row_count": len(rows),
            "rows": rows,
        }

    except GoogleSheetsError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc