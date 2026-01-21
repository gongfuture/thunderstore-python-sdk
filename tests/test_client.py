"""Tests for Thunderstore SDK client."""

import pytest
from pytest_httpx import HTTPXMock

from thunderstore_sdk.client import ThunderstoreClient
from thunderstore_sdk.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)


@pytest.fixture
def client() -> ThunderstoreClient:
    """Create a test client."""
    return ThunderstoreClient(base_url="https://thunderstore.io")


def test_client_initialization() -> None:
    """Test client initialization."""
    client = ThunderstoreClient()
    assert client.base_url == "https://thunderstore.io"
    assert client.api_token is None
    assert client.timeout == 30.0


def test_client_with_token() -> None:
    """Test client initialization with API token."""
    client = ThunderstoreClient(api_token="test_token")
    assert client.api_token == "test_token"


def test_list_packages(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test listing packages."""
    mock_response = [
        {
            "namespace": "TestTeam",
            "name": "TestMod",
            "full_name": "TestTeam-TestMod",
            "owner": "TestUser",
            "package_url": "https://thunderstore.io/package/TestTeam/TestMod/",
            "date_created": "2024-01-01T12:00:00Z",
            "date_updated": "2024-01-02T12:00:00Z",
            "rating_score": 100,
            "is_pinned": False,
            "is_deprecated": False,
            "has_nsfw_content": False,
            "categories": ["mods"],
            "latest_version_number": "1.0.0",
            "total_downloads": 500,
        }
    ]
    httpx_mock.add_response(json=mock_response)

    packages = client.list_packages()
    assert len(packages) == 1
    assert packages[0].namespace == "TestTeam"
    assert packages[0].name == "TestMod"


def test_list_packages_paginated(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test listing packages with pagination."""
    mock_response = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "namespace": "TestTeam",
                "name": "TestMod",
                "full_name": "TestTeam-TestMod",
                "owner": "TestUser",
                "package_url": "https://thunderstore.io/package/TestTeam/TestMod/",
                "date_created": "2024-01-01T12:00:00Z",
                "date_updated": "2024-01-02T12:00:00Z",
                "rating_score": 100,
                "is_pinned": False,
                "is_deprecated": False,
                "has_nsfw_content": False,
                "categories": ["mods"],
                "latest_version_number": "1.0.0",
                "total_downloads": 500,
            }
        ],
    }
    httpx_mock.add_response(json=mock_response)

    packages = client.list_packages(page=2)
    assert len(packages) == 1


def test_get_package(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test getting a specific package."""
    mock_response = {
        "namespace": "TestTeam",
        "name": "TestMod",
        "full_name": "TestTeam-TestMod",
        "owner": "TestUser",
        "package_url": "https://thunderstore.io/package/TestTeam/TestMod/",
        "date_created": "2024-01-01T12:00:00Z",
        "date_updated": "2024-01-02T12:00:00Z",
        "rating_score": 100,
        "is_pinned": False,
        "is_deprecated": False,
        "has_nsfw_content": False,
        "categories": ["mods"],
        "versions": [
            {
                "namespace": "TestTeam",
                "name": "TestMod",
                "version_number": "1.0.0",
                "full_name": "TestTeam-TestMod-1.0.0",
                "description": "A test mod",
                "icon": "https://example.com/icon.png",
                "dependencies": [],
                "download_url": "https://example.com/download.zip",
                "downloads": 100,
                "date_created": "2024-01-01T12:00:00Z",
                "website_url": "https://example.com",
                "is_active": True,
                "file_size": 1024,
            }
        ],
    }
    httpx_mock.add_response(json=mock_response)

    package = client.get_package("TestTeam", "TestMod")
    assert package.namespace == "TestTeam"
    assert package.name == "TestMod"
    assert len(package.versions) == 1


def test_search_packages(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test searching packages."""
    mock_response = [
        {
            "namespace": "TestTeam",
            "name": "TestMod",
            "full_name": "TestTeam-TestMod",
            "owner": "TestUser",
            "package_url": "https://thunderstore.io/package/TestTeam/TestMod/",
            "date_created": "2024-01-01T12:00:00Z",
            "date_updated": "2024-01-02T12:00:00Z",
            "rating_score": 100,
            "is_pinned": False,
            "is_deprecated": False,
            "has_nsfw_content": False,
            "categories": ["mods"],
            "latest_version_number": "1.0.0",
            "total_downloads": 500,
        }
    ]
    httpx_mock.add_response(json=mock_response)

    results = client.search_packages("test")
    assert len(results) == 1
    assert results[0].name == "TestMod"


def test_list_communities(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test listing communities."""
    mock_response = [
        {
            "identifier": "riskofrain2",
            "name": "Risk of Rain 2",
            "discord_url": "https://discord.gg/example",
            "wiki_url": "https://wiki.example.com",
            "require_package_category_choice": True,
        }
    ]
    httpx_mock.add_response(json=mock_response)

    communities = client.list_communities()
    assert len(communities) == 1
    assert communities[0].identifier == "riskofrain2"


def test_get_community(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test getting a specific community."""
    mock_response = {
        "identifier": "riskofrain2",
        "name": "Risk of Rain 2",
        "discord_url": "https://discord.gg/example",
        "wiki_url": "https://wiki.example.com",
        "require_package_category_choice": True,
    }
    httpx_mock.add_response(json=mock_response)

    community = client.get_community("riskofrain2")
    assert community.identifier == "riskofrain2"
    assert community.name == "Risk of Rain 2"


def test_not_found_error(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test handling 404 errors."""
    httpx_mock.add_response(status_code=404, text="Not found")

    with pytest.raises(NotFoundError) as exc_info:
        client.get_package("NonExistent", "Package")
    assert exc_info.value.status_code == 404


def test_authentication_error(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test handling 401 errors."""
    httpx_mock.add_response(status_code=401, text="Unauthorized")

    with pytest.raises(AuthenticationError) as exc_info:
        client.list_packages()
    assert exc_info.value.status_code == 401


def test_rate_limit_error(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test handling 429 errors."""
    httpx_mock.add_response(status_code=429, text="Rate limit exceeded")

    with pytest.raises(RateLimitError) as exc_info:
        client.list_packages()
    assert exc_info.value.status_code == 429


def test_generic_api_error(client: ThunderstoreClient, httpx_mock: HTTPXMock) -> None:
    """Test handling other API errors."""
    httpx_mock.add_response(status_code=500, text="Internal server error")

    with pytest.raises(APIError) as exc_info:
        client.list_packages()
    assert exc_info.value.status_code == 500


def test_context_manager() -> None:
    """Test using client as context manager."""
    with ThunderstoreClient() as client:
        assert client._client is None  # Not created until first use
    # Client should be closed after context exit
    assert client._client is None
