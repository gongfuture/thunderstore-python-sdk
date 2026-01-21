"""Pydantic models for Thunderstore API responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class PackageCategory(BaseModel):
    """Represents a package category."""

    name: str
    slug: str


class PackageVersion(BaseModel):
    """Represents a package version."""

    namespace: str
    name: str
    version_number: str
    full_name: str
    description: str
    icon: HttpUrl
    dependencies: list[str]
    download_url: HttpUrl
    downloads: int
    date_created: datetime
    website_url: HttpUrl | None = None
    is_active: bool
    file_size: int


class Package(BaseModel):
    """Represents a package in the Thunderstore."""

    namespace: str
    name: str
    full_name: str
    owner: str
    package_url: HttpUrl
    date_created: datetime
    date_updated: datetime
    rating_score: int
    is_pinned: bool
    is_deprecated: bool
    has_nsfw_content: bool
    categories: list[str]
    versions: list[PackageVersion]
    latest: PackageVersion | None = None


class Community(BaseModel):
    """Represents a game community."""

    identifier: str
    name: str
    discord_url: HttpUrl | None = None
    wiki_url: HttpUrl | None = None
    require_package_category_choice: bool


class PackageListing(BaseModel):
    """Represents a package listing (simplified package info)."""

    namespace: str
    name: str
    full_name: str
    owner: str
    package_url: HttpUrl
    date_created: datetime
    date_updated: datetime
    rating_score: int
    is_pinned: bool
    is_deprecated: bool
    has_nsfw_content: bool
    categories: list[str]
    latest_version_number: str | None = None
    total_downloads: int = 0


class PaginatedResponse(BaseModel):
    """Generic paginated response."""

    count: int
    next: HttpUrl | None = None
    previous: HttpUrl | None = None
    results: list[Any] = Field(default_factory=list)
