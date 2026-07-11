from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import Final, Sequence

from google.auth.exceptions import GoogleAuthError
from google.oauth2.service_account import Credentials

from app.core.config import Settings, get_settings
from app.integrations.google.exceptions import GoogleCredentialsError


GOOGLE_SHEETS_READONLY_SCOPE: Final[str] = (
    "https://www.googleapis.com/auth/spreadsheets.readonly"
)


class GoogleCredentialsProvider:
    """
    Creates and provides Google service-account credentials.

    Responsibilities:
    - Resolve the service-account JSON file path.
    - Validate that the file exists.
    - Load service-account credentials.
    - Apply the required OAuth scopes.

    This class does not create a Google Sheets client and does not read data.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        scopes: Sequence[str] | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._scopes = tuple(
            scopes or (GOOGLE_SHEETS_READONLY_SCOPE,)
        )

    @cached_property
    def credentials_file(self) -> Path:
        """
        Return the resolved absolute credentials-file path.
        """
        return (
            self._settings.google_service_account_file
            .expanduser()
            .resolve()
        )

    def _validate_credentials_file(self) -> None:
        path = self.credentials_file

        if not path.exists():
            raise GoogleCredentialsError(
                f"Google service-account file does not exist: {path}"
            )

        if not path.is_file():
            raise GoogleCredentialsError(
                f"Google service-account path is not a file: {path}"
            )

        if path.suffix.lower() != ".json":
            raise GoogleCredentialsError(
                "Google service-account credentials must be a JSON file."
            )

    @cached_property
    def credentials(self) -> Credentials:
        """
        Load and cache scoped service-account credentials.
        """
        self._validate_credentials_file()

        try:
            return Credentials.from_service_account_file(
                filename=str(self.credentials_file),
                scopes=list(self._scopes),
            )

        except (GoogleAuthError, ValueError, OSError) as exc:
            raise GoogleCredentialsError(
                "Could not load Google service-account credentials. "
                "Confirm that the JSON file is valid and contains a "
                "service-account private key."
            ) from exc

    @property
    def service_account_email(self) -> str:
        """
        Return the service-account email.

        The Google Sheet must be shared with this email address.
        """
        email = self.credentials.service_account_email

        if not email:
            raise GoogleCredentialsError(
                "The credentials file does not contain a service-account email."
            )

        return email