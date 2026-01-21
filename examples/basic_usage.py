"""Basic usage examples for the Thunderstore SDK."""

from thunderstore_sdk import ThunderstoreClient


def basic_usage() -> None:
    """Demonstrate basic SDK usage."""
    # Create a client using context manager
    with ThunderstoreClient() as client:
        # List packages
        print("=== Listing packages ===")
        packages = client.list_packages(page=1)
        for package in packages[:5]:
            print(
                f"{package.full_name} - "
                f"{package.total_downloads} downloads - "
                f"Rating: {package.rating_score}"
            )

        print("\n=== Searching packages ===")
        # Search for packages
        results = client.search_packages("utility")
        print(f"Found {len(results)} packages matching 'utility'")
        for pkg in results[:3]:
            print(f"  - {pkg.full_name}")

        print("\n=== Listing communities ===")
        # List communities
        communities = client.list_communities()
        for community in communities[:5]:
            print(f"{community.name} ({community.identifier})")


def get_specific_package() -> None:
    """Get detailed information about a specific package."""
    with ThunderstoreClient() as client:
        try:
            # Get a specific package
            package = client.get_package("BepInEx", "BepInExPack")
            print(f"\nPackage: {package.full_name}")
            print(f"Owner: {package.owner}")
            print(f"Rating: {package.rating_score}")
            print(f"Versions available: {len(package.versions)}")

            if package.latest:
                print(f"Latest version: {package.latest.version_number}")
                print(f"Latest version downloads: {package.latest.downloads}")
        except Exception as e:
            print(f"Error: {e}")


def filter_by_community() -> None:
    """Filter packages by community."""
    with ThunderstoreClient() as client:
        print("\n=== Packages for Risk of Rain 2 ===")
        packages = client.list_packages(community="riskofrain2", page=1)
        for package in packages[:5]:
            print(f"{package.full_name} - {package.total_downloads} downloads")


if __name__ == "__main__":
    print("Thunderstore SDK Examples\n")
    basic_usage()
    get_specific_package()
    filter_by_community()
