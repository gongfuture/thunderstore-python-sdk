"""Tests for Thunderstore SDK exceptions."""

from thunderstore_sdk.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ThunderstoreError,
    ValidationError,
)


def test_base_exception() -> None:
    """Test base ThunderstoreError."""
    error = ThunderstoreError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_api_error() -> None:
    """Test APIError with status code."""
    error = APIError("API failed", status_code=500)
    assert str(error) == "API failed"
    assert error.status_code == 500
    assert isinstance(error, ThunderstoreError)


def test_api_error_without_status_code() -> None:
    """Test APIError without status code."""
    error = APIError("API failed")
    assert str(error) == "API failed"
    assert error.status_code is None


def test_validation_error() -> None:
    """Test ValidationError."""
    error = ValidationError("Validation failed")
    assert str(error) == "Validation failed"
    assert isinstance(error, ThunderstoreError)


def test_rate_limit_error() -> None:
    """Test RateLimitError."""
    error = RateLimitError("Rate limit exceeded", status_code=429)
    assert str(error) == "Rate limit exceeded"
    assert error.status_code == 429
    assert isinstance(error, APIError)


def test_not_found_error() -> None:
    """Test NotFoundError."""
    error = NotFoundError("Resource not found", status_code=404)
    assert str(error) == "Resource not found"
    assert error.status_code == 404
    assert isinstance(error, APIError)


def test_authentication_error() -> None:
    """Test AuthenticationError."""
    error = AuthenticationError("Authentication failed", status_code=401)
    assert str(error) == "Authentication failed"
    assert error.status_code == 401
    assert isinstance(error, APIError)
