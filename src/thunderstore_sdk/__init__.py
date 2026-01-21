"""Thunderstore Python SDK.

A Python SDK for the Thunderstore API, a mod distribution platform for games.
"""

from .client import ThunderstoreClient
from .exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ThunderstoreError,
    ValidationError,
)
from .models import (
    Community,
    CyberstormCommunity,
    Package,
    PackageCategory,
    PackageExperimental,
    PackageMetrics,
    PackageVersion,
    PackageVersionExperimental,
    PackageVersionMetrics,
)

__version__ = "0.1.0"

__all__ = [
    "ThunderstoreClient",
    "ThunderstoreError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "Package",
    "PackageVersion",
    "PackageExperimental",
    "PackageVersionExperimental",
    "PackageCategory",
    "Community",
    "CyberstormCommunity",
    "PackageMetrics",
    "PackageVersionMetrics",
]
