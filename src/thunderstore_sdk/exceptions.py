"""Exceptions for the Thunderstore SDK."""


class ThunderstoreError(Exception):
    """Base exception for all Thunderstore SDK errors."""


class APIError(ThunderstoreError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ValidationError(ThunderstoreError):
    """Raised when request/response validation fails."""


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""


class NotFoundError(APIError):
    """Raised when a resource is not found."""


class AuthenticationError(APIError):
    """Raised when authentication fails."""
