"""Tests for Thunderstore SDK models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from thunderstore_sdk.models import Community, Package, PackageCategory, PackageVersion


def test_package_category_valid() -> None:
    """Test PackageCategory with valid data."""
    category = PackageCategory(name="Mods", slug="mods")
    assert category.name == "Mods"
    assert category.slug == "mods"


def test_package_version_valid() -> None:
    """Test PackageVersion with valid data."""
    version = PackageVersion(
        name="TestMod",
        version_number="1.0.0",
        full_name="TestTeam-TestMod-1.0.0",
        description="A test mod",
        icon="https://example.com/icon.png",
        dependencies=["TestTeam-Dependency-1.0.0"],
        download_url="https://example.com/download.zip",
        downloads=100,
        date_created=datetime(2024, 1, 1, 12, 0, 0),
        website_url="https://example.com",
        is_active=True,
        uuid4="test-uuid",
        file_size=1024,
    )
    assert version.name == "TestMod"
    assert version.version_number == "1.0.0"
    assert version.downloads == 100
    assert version.is_active is True
    assert version.file_size == 1024


def test_package_version_without_optional_fields() -> None:
    """Test PackageVersion without optional fields."""
    version = PackageVersion(
        name="TestMod",
        version_number="1.0.0",
        full_name="TestTeam-TestMod-1.0.0",
        description="A test mod",
        icon="https://example.com/icon.png",
        dependencies=[],
        download_url="https://example.com/download.zip",
        downloads=0,
        date_created=datetime(2024, 1, 1, 12, 0, 0),
        is_active=True,
        uuid4="test-uuid",
        file_size=1024,
    )
    assert version.website_url is None


def test_package_valid() -> None:
    """Test Package with valid data."""
    package = Package(
        name="TestMod",
        full_name="TestTeam-TestMod",
        owner="TestUser",
        package_url="https://thunderstore.io/package/TestTeam/TestMod/",
        date_created=datetime(2024, 1, 1, 12, 0, 0),
        date_updated=datetime(2024, 1, 2, 12, 0, 0),
        uuid4="test-uuid",
        rating_score=100,
        is_pinned=False,
        is_deprecated=False,
        has_nsfw_content=False,
        categories=["mods"],
        versions=[],
    )
    assert package.name == "TestMod"
    assert package.rating_score == 100


def test_community_valid() -> None:
    """Test Community with valid data."""
    community = Community(
        identifier="riskofrain2",
        name="Risk of Rain 2",
        discord_url="https://discord.gg/example",
        wiki_url="https://wiki.example.com",
        require_package_listing_approval=True,
    )
    assert community.identifier == "riskofrain2"
    assert community.name == "Risk of Rain 2"
    assert community.require_package_listing_approval is True


def test_community_without_optional_fields() -> None:
    """Test Community without optional fields."""
    community = Community(
        identifier="valheim",
        name="Valheim",
        require_package_listing_approval=False,
    )
    assert community.discord_url is None
    assert community.wiki_url is None


def test_package_invalid_url() -> None:
    """Test that invalid URLs raise ValidationError."""
    with pytest.raises(ValidationError):
        Package(
            name="TestMod",
            full_name="TestTeam-TestMod",
            owner="TestUser",
            package_url="not-a-valid-url",  # type: ignore
            date_created=datetime(2024, 1, 1, 12, 0, 0),
            date_updated=datetime(2024, 1, 2, 12, 0, 0),
            uuid4="test-uuid",
            rating_score=100,
            is_pinned=False,
            is_deprecated=False,
            has_nsfw_content=False,
            categories=["mods"],
            versions=[],
        )
