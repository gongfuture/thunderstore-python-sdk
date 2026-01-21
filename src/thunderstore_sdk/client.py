"""HTTP client for the Thunderstore API."""

from typing import Any

import httpx

from .exceptions import APIError, AuthenticationError, NotFoundError, RateLimitError
from .models import Community, Package, PackageListing


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
            headers = {"User-Agent": "thunderstore-sdk/0.1.0"}
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
        page: int = 1,
        ordering: str = "-date_updated",
    ) -> list[PackageListing]:
        """
        List packages from the Thunderstore.

        Args:
            community: Filter by community identifier (e.g., 'riskofrain2')
            page: Page number for pagination
            ordering: Sort order (e.g., '-date_updated', 'name', '-rating_score')

        Returns:
            List of package listings
        """
        params: dict[str, Any] = {"page": page, "ordering": ordering}
        if community:
            params["community"] = community

        response = self.client.get("/api/v1/package/", params=params)
        data = self._handle_response(response)

        # Handle both paginated and non-paginated responses
        if isinstance(data, dict) and "results" in data:
            return [PackageListing(**item) for item in data["results"]]
        return [PackageListing(**item) for item in data]

    def get_package(self, namespace: str, name: str) -> Package:
        """
        Get detailed information about a specific package.

        Args:
            namespace: Package namespace (owner)
            name: Package name

        Returns:
            Package details
        """
        response = self.client.get(f"/api/v1/package/{namespace}/{name}/")
        data = self._handle_response(response)
        return Package(**data)

    def search_packages(
        self,
        query: str,
        community: str | None = None,
        page: int = 1,
    ) -> list[PackageListing]:
        """
        Search for packages.

        Args:
            query: Search query string
            community: Filter by community identifier
            page: Page number for pagination

        Returns:
            List of matching packages
        """
        params: dict[str, Any] = {"q": query, "page": page}
        if community:
            params["community"] = community

        response = self.client.get("/api/v1/package/", params=params)
        data = self._handle_response(response)

        if isinstance(data, dict) and "results" in data:
            return [PackageListing(**item) for item in data["results"]]
        return [PackageListing(**item) for item in data]

    def list_communities(self) -> list[Community]:
        """
        List all available communities.

        Returns:
            List of communities
        """
        response = self.client.get("/api/v1/community/")
        data = self._handle_response(response)

        if isinstance(data, dict) and "results" in data:
            return [Community(**item) for item in data["results"]]
        return [Community(**item) for item in data]

    def get_community(self, identifier: str) -> Community:
        """
        Get information about a specific community.

        Args:
            identifier: Community identifier

        Returns:
            Community details
        """
        response = self.client.get(f"/api/v1/community/{identifier}/")
        data = self._handle_response(response)
        return Community(**data)

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
