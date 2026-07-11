class GoogleIntegrationError(Exception):
    """Base exception for Google integrations."""


class GoogleCredentialsError(GoogleIntegrationError):
    """Raised when Google credentials cannot be loaded."""