"""HTTP client for the Thunderstore API."""

from typing import Any

import httpx

from .exceptions import APIError, AuthenticationError, NotFoundError, RateLimitError
from .models import (
    Community,
    CyberstormCommunity,
    Package,
    PackageCategory,
    PackageExperimental,
    PackageMetrics,
    PackageVersionExperimental,
    PackageVersionMetrics,
)


class ThunderstoreClient:
    """Client for interacting with the Thunderstore API."""

    def __init__(
        self,
        base_url: str = "https://thunderstore.io",
        api_token: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize the Thunderstore client.

        Args:
            base_url: Base URL for the Thunderstore API
            api_token: Optional API token for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        """Get or create the HTTP client."""
        if self._client is None:
            from . import __version__

            headers = {"User-Agent": f"thunderstore-sdk/{__version__}"}
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._client

    def _handle_response(self, response: httpx.Response) -> Any:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            raise AuthenticationError("Authentication failed", status_code=401)
        if response.status_code == 404:
            raise NotFoundError("Resource not found", status_code=404)
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded", status_code=429)
        raise APIError(
            f"API request failed: {response.status_code} {response.text}",
            status_code=response.status_code,
        )

    def list_packages(
        self,
        community: str | None = None,
        ordering: str | None = None,
    ) -> list[Package]:
        """
        List packages from the Thunderstore.

        Args:
            community: Filter by community identifier (e.g., 'riskofrain2')
            ordering: Sort order (e.g., '-date_updated', 'name', '-rating_score')

        Returns:
            List of packages
        """
        params: dict[str, Any] = {}
        if community:
            params["community"] = community
        if ordering:
            params["ordering"] = ordering

        response = self.client.get("/api/v1/package/", params=params)
        data = self._handle_response(response)

        # API returns a list directly
        if isinstance(data, list):
            return [Package(**item) for item in data]
        return []

    def get_package(self, owner: str, name: str) -> Package | None:
        """
        Get detailed information about a specific package.

        Args:
            owner: Package owner
            name: Package name

        Returns:
            Package details or None if not found
        """
        # Since API returns all packages, we search for the one we want
        packages = self.list_packages()
        full_name = f"{owner}-{name}"
        for package in packages:
            if package.full_name == full_name:
                return package
        return None

    def search_packages(
        self,
        query: str,
        community: str | None = None,
    ) -> list[Package]:
        """
        Search for packages.

        Args:
            query: Search query string
            community: Filter by community identifier

        Returns:
            List of matching packages
        """
        packages = self.list_packages(community=community)
        # Simple client-side search
        query_lower = query.lower()
        return [
            pkg
            for pkg in packages
            if query_lower in pkg.name.lower()
            or query_lower in pkg.full_name.lower()
            or query_lower in pkg.owner.lower()
            or any(query_lower in cat.lower() for cat in pkg.categories)
        ]

    def list_communities(self) -> list[Community]:
        """
        List all available communities (experimental API).

        Returns:
            List of communities
        """
        response = self.client.get("/api/experimental/community/")
        data = self._handle_response(response)

        if isinstance(data, dict) and "results" in data:
            return [Community(**item) for item in data["results"]]
        return [Community(**item) for item in data] if isinstance(data, list) else []

    def get_community(self, identifier: str) -> Community:
        """
        Get information about a specific community (experimental API).

        Args:
            identifier: Community identifier

        Returns:
            Community details
        """
        response = self.client.get(f"/api/experimental/community/{identifier}/")
        data = self._handle_response(response)
        return Community(**data)

    def get_cyberstorm_community(self, community_id: str) -> CyberstormCommunity:
        """
        Get detailed community information (Cyberstorm API).

        Args:
            community_id: Community identifier

        Returns:
            Detailed community information including stats and images
        """
        response = self.client.get(f"/api/cyberstorm/community/{community_id}/")
        data = self._handle_response(response)
        return CyberstormCommunity(**data)

    # Experimental API methods
    def list_packages_experimental(
        self,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """
        List packages using experimental API with proper pagination.

        Args:
            cursor: Pagination cursor for next/previous page

        Returns:
            Dictionary with 'results', 'next', and 'previous' keys
        """
        params: dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor

        response = self.client.get("/api/experimental/package/", params=params)
        data = self._handle_response(response)

        if isinstance(data, dict) and "results" in data:
            results = [PackageExperimental(**item) for item in data["results"]]
            return {
                "results": results,
                "next": data.get("next"),
                "previous": data.get("previous"),
            }
        return {"results": [], "next": None, "previous": None}

    def get_package_experimental(self, namespace: str, name: str) -> PackageExperimental | None:
        """
        Get a single package using experimental API.

        Args:
            namespace: Package namespace (owner)
            name: Package name

        Returns:
            Package details or None if not found
        """
        try:
            response = self.client.get(f"/api/experimental/package/{namespace}/{name}/")
            data = self._handle_response(response)
            return PackageExperimental(**data)
        except NotFoundError:
            return None

    def get_package_version_experimental(
        self, namespace: str, name: str, version: str
    ) -> PackageVersionExperimental | None:
        """
        Get a specific package version using experimental API.

        Args:
            namespace: Package namespace
            name: Package name
            version: Version number

        Returns:
            Package version details or None if not found
        """
        try:
            response = self.client.get(f"/api/experimental/package/{namespace}/{name}/{version}/")
            data = self._handle_response(response)
            return PackageVersionExperimental(**data)
        except NotFoundError:
            return None

    def list_community_categories(
        self, community: str, cursor: str | None = None
    ) -> dict[str, Any]:
        """
        List categories for a specific community.

        Args:
            community: Community identifier
            cursor: Pagination cursor

        Returns:
            Dictionary with 'results', 'next', and 'previous' keys
        """
        params: dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor

        response = self.client.get(
            f"/api/experimental/community/{community}/category/", params=params
        )
        data = self._handle_response(response)

        if isinstance(data, dict) and "results" in data:
            results = [PackageCategory(**item) for item in data["results"]]
            return {
                "results": results,
                "next": data.get("next"),
                "previous": data.get("previous"),
            }
        return {"results": [], "next": None, "previous": None}

    def get_package_metrics(self, namespace: str, name: str) -> PackageMetrics | None:
        """
        Get package metrics including downloads and rating.

        Args:
            namespace: Package namespace
            name: Package name

        Returns:
            Package metrics or None if not found
        """
        try:
            response = self.client.get(f"/api/v1/package-metrics/{namespace}/{name}/")
            data = self._handle_response(response)
            return PackageMetrics(**data)
        except NotFoundError:
            return None

    def get_package_version_metrics(
        self, namespace: str, name: str, version: str
    ) -> PackageVersionMetrics | None:
        """
        Get download metrics for a specific package version.

        Args:
            namespace: Package namespace
            name: Package name
            version: Version number

        Returns:
            Version metrics or None if not found
        """
        try:
            response = self.client.get(f"/api/v1/package-metrics/{namespace}/{name}/{version}/")
            data = self._handle_response(response)
            return PackageVersionMetrics(**data)
        except NotFoundError:
            return None

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "ThunderstoreClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()
