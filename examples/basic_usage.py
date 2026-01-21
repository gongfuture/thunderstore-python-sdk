"""Basic usage examples for the Thunderstore SDK."""

from thunderstore_sdk import ThunderstoreClient


def basic_usage() -> None:
    """Demonstrate basic SDK usage."""
    # Create a client using context manager
    with ThunderstoreClient() as client:
        # List packages
        print("=== Listing packages ===")
        packages = client.list_packages()
        for package in packages[:5]:
            print(f"{package.full_name} - Rating: {package.rating_score}")

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
        # Get a specific package
        package = client.get_package("ebkr", "r2modman")
        if package:
            print(f"\nPackage: {package.full_name}")
            print(f"Owner: {package.owner}")
            print(f"Rating: {package.rating_score}")
            print(f"Versions available: {len(package.versions)}")
            if package.versions:
                latest = package.versions[0]
                print(f"Latest version: {latest.version_number}")
                print(f"Latest version downloads: {latest.downloads}")
        else:
            print("Package not found")


def filter_by_community() -> None:
    """Filter packages by community."""
    with ThunderstoreClient() as client:
        print("\n=== Packages for Risk of Rain 2 ===")
        packages = client.list_packages(community="riskofrain2")
        for package in packages[:5]:
            print(f"{package.full_name} - Rating: {package.rating_score}")


if __name__ == "__main__":
    print("Thunderstore SDK Examples\n")
    basic_usage()
    get_specific_package()
    filter_by_community()
