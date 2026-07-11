from __future__ import annotations

import asyncio
import logging
from functools import cached_property
from typing import Any

from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from app.integrations.google.credentials import GoogleCredentialsProvider
from app.integrations.google.exceptions import GoogleSheetsError


logger = logging.getLogger(__name__)


class GoogleSheetsClient:
    """
    Low-level client for reading values from Google Sheets.

    Responsibilities:
    - Build and reuse the Google Sheets API service.
    - Read raw values from a spreadsheet range.
    - Convert synchronous Google SDK calls into async-friendly calls.

    This class does not:
    - Know sheet names such as Products or Brand Memory.
    - Parse rows into dictionaries.
    - Validate product or content-library schemas.
    - Contain business logic.
    """

    def __init__(
        self,
        credentials_provider: GoogleCredentialsProvider | None = None,
    ) -> None:
        self._credentials_provider = (
            credentials_provider or GoogleCredentialsProvider()
        )

    @cached_property
    def service(self) -> Resource:
        """
        Build and cache the Google Sheets API service.
        """
        try:
            return build(
                serviceName="sheets",
                version="v4",
                credentials=self._credentials_provider.credentials,
                cache_discovery=False,
            )

        except Exception as exc:
            logger.exception("Failed to build Google Sheets API service.")

            raise GoogleSheetsError(
                "Could not initialize the Google Sheets API client."
            ) from exc

    def _read_range_sync(
        self,
        spreadsheet_id: str,
        range_name: str,
    ) -> list[list[Any]]:
        """
        Synchronously read raw values from a spreadsheet range.

        Example range names:
            Products!A:Z
            'Brand Memory'!A:B
            'Content Library'!A:H
        """
        if not spreadsheet_id.strip():
            raise ValueError("spreadsheet_id cannot be empty.")

        if not range_name.strip():
            raise ValueError("range_name cannot be empty.")

        try:
            response = (
                self.service
                .spreadsheets()
                .values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    majorDimension="ROWS",
                )
                .execute()
            )

            values = response.get("values", [])

            if not isinstance(values, list):
                raise GoogleSheetsError(
                    "Google Sheets API returned an unexpected values format."
                )

            return values

        except HttpError as exc:
            logger.exception(
                "Google Sheets API error. spreadsheet_id=%s range=%s",
                spreadsheet_id,
                range_name,
            )

            status_code = getattr(exc.resp, "status", None)

            if status_code == 403:
                message = (
                    "Google Sheets access was denied. Confirm that the sheet "
                    "is shared with the service-account email and that the "
                    "Google Sheets API is enabled."
                )
            elif status_code == 404:
                message = (
                    "Spreadsheet or range was not found. Check the spreadsheet "
                    "ID and range name."
                )
            else:
                message = (
                    f"Could not read Google Sheets range: {range_name}"
                )

            raise GoogleSheetsError(message) from exc

        except GoogleSheetsError:
            raise

        except Exception as exc:
            logger.exception(
                "Unexpected error while reading Google Sheets range: %s",
                range_name,
            )

            raise GoogleSheetsError(
                f"Unexpected error while reading range: {range_name}"
            ) from exc

    async def read_range(
        self,
        spreadsheet_id: str,
        range_name: str,
    ) -> list[list[Any]]:
        """
        Asynchronously read raw spreadsheet values.

        The Google API Python client is synchronous. Running it through
        asyncio.to_thread prevents it from blocking FastAPI's event loop.
        """
        return await asyncio.to_thread(
            self._read_range_sync,
            spreadsheet_id,
            range_name,
        )