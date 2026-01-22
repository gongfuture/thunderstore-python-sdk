"""Pydantic models for Thunderstore API responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class PackageCategory(BaseModel):
    """Represents a package category."""

    name: str
    slug: str


class PackageVersion(BaseModel):
    """Represents a package version (v1 API)."""

    name: str
    full_name: str
    description: str
    icon: HttpUrl
    version_number: str
    dependencies: list[str]
    download_url: HttpUrl
    downloads: int
    date_created: datetime
    website_url: HttpUrl | None = None
    is_active: bool
    uuid4: str
    file_size: int


class Package(BaseModel):
    """Represents a package in the Thunderstore (v1 API)."""

    name: str
    full_name: str
    owner: str
    package_url: HttpUrl
    donation_link: HttpUrl | None = None
    date_created: datetime
    date_updated: datetime
    uuid4: str
    rating_score: int
    is_pinned: bool
    is_deprecated: bool
    has_nsfw_content: bool
    categories: list[str]
    versions: list[PackageVersion]


class PackageVersionExperimental(BaseModel):
    """Represents a package version (experimental API)."""

    namespace: str | None = None
    name: str
    version_number: str
    full_name: str | None = None
    description: str
    icon: HttpUrl | None = None
    dependencies: str | None = None
    download_url: HttpUrl | None = None
    downloads: int = 0
    date_created: datetime | None = None
    website_url: str | None = None
    is_active: bool = True


class PackageListingExperimental(BaseModel):
    """Represents a package listing in a community (experimental API)."""

    has_nsfw_content: bool = False
    categories: str | None = None
    community: str | None = None
    review_status: str = "unreviewed"


class PackageExperimental(BaseModel):
    """Represents a package (experimental API)."""

    namespace: str | None = None
    name: str
    full_name: str | None = None
    owner: str | None = None
    package_url: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    rating_score: str | None = None
    is_pinned: bool = False
    is_deprecated: bool = False
    total_downloads: str | None = None
    latest: PackageVersionExperimental
    community_listings: list[PackageListingExperimental] = Field(default_factory=list)


class Community(BaseModel):
    """Represents a game community."""

    identifier: str
    name: str
    discord_url: HttpUrl | None = None
    wiki_url: HttpUrl | None = None
    require_package_listing_approval: bool = False


class CyberstormCommunity(BaseModel):
    """Represents a community in the Cyberstorm API."""

    name: str
    identifier: str
    short_description: str | None = None
    description: str | None = None
    discord_url: str | None = None
    wiki_url: str | None = None
    datetime_created: datetime
    background_image_url: str | None = None
    hero_image_url: str | None = None
    cover_image_url: str | None = None
    icon_url: str | None = None
    community_icon_url: str | None = None
    total_download_count: int | None = None
    total_package_count: int | None = None
    has_mod_manager_support: bool
    is_listed: bool


class PackageMetrics(BaseModel):
    """Package download and rating metrics."""

    downloads: int
    rating_score: int
    latest_version: str


class PackageVersionMetrics(BaseModel):
    """Package version download metrics."""

    downloads: int


class PaginatedResponse(BaseModel):
    """Generic paginated response."""

    next: HttpUrl | None = None
    previous: HttpUrl | None = None
    results: list[Any] = Field(default_factory=list)
