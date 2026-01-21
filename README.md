# Thunderstore Python SDK

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A modern Python SDK for the [Thunderstore API](https://thunderstore.io/api/docs/), built with httpx and pydantic.

## Features

- 🚀 **Async-ready**: Built on httpx for modern async/await support
- 🔒 **Type-safe**: Full type hints and pydantic validation
- 🎯 **Simple API**: Clean, intuitive interface
- 📦 **Comprehensive**: Covers all major Thunderstore API endpoints
- 🧪 **Well-tested**: High test coverage with pytest
- 📚 **Well-documented**: Detailed documentation and examples

## Installation

Install using uv (recommended):

```bash
uv add thunderstore-sdk
```

Or using pip:

```bash
pip install thunderstore-sdk
```

## Quick Start

```python
from thunderstore_sdk import ThunderstoreClient

# Create a client
client = ThunderstoreClient()

# List all packages
packages = client.list_packages()
for package in packages[:5]:
    print(f"{package.full_name} - Rating: {package.rating_score}")

# Get a specific package
package = client.get_package("ebkr", "r2modman")
if package:
    print(f"Package: {package.full_name}")
    print(f"Versions: {len(package.versions)}")

# Search for packages
results = client.search_packages("utility")
print(f"Found {len(results)} packages")

# List communities
communities = client.list_communities()
for community in communities[:5]:
    print(f"{community.name} ({community.identifier})")

# Always close the client when done
client.close()
```

## Using Context Manager

The recommended way to use the client is with a context manager:

```python
from thunderstore_sdk import ThunderstoreClient

with ThunderstoreClient() as client:
    packages = client.list_packages(community="riskofrain2")
    for package in packages[:10]:
        print(f"{package.full_name}")
# Client is automatically closed
```

## Authentication

If you have an API token, you can authenticate your requests:

```python
from thunderstore_sdk import ThunderstoreClient

client = ThunderstoreClient(api_token="your_token_here")
```

## API Methods

### Packages

- `list_packages(community=None, ordering=None)` - List packages
- `get_package(owner, name)` - Get detailed package information
- `search_packages(query, community=None)` - Search for packages

### Communities

- `list_communities()` - List all game communities
- `get_community(identifier)` - Get specific community information

## Development

### Setup

Clone the repository and install dependencies using uv:

```bash
git clone https://github.com/gongfuture/thunderstore-python-sdk.git
cd thunderstore-python-sdk
uv sync
```

### Running Tests

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov=thunderstore_sdk --cov-report=html
```

### Linting and Formatting

```bash
# Check code style
uv run ruff check .

# Format code
uv run ruff format .

# Type checking
uv run mypy src/
```

## Project Structure

```
thunderstore-python-sdk/
├── src/
│   └── thunderstore_sdk/
│       ├── __init__.py      # Main exports
│       ├── client.py        # HTTP client
│       ├── models.py        # Pydantic models
│       └── exceptions.py    # Custom exceptions
├── tests/
│   ├── test_client.py       # Client tests
│   ├── test_models.py       # Model tests
│   └── test_exceptions.py   # Exception tests
├── pyproject.toml           # Project configuration
└── README.md
```

## Requirements

- Python 3.12+
- httpx >= 0.28.1
- pydantic >= 2.12.5

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Thunderstore Website](https://thunderstore.io/)
- [Thunderstore API Documentation](https://thunderstore.io/api/docs/)
- [GitHub Repository](https://github.com/gongfuture/thunderstore-python-sdk)

## Acknowledgments

- Built with [httpx](https://www.python-httpx.org/) for HTTP requests
- Uses [pydantic](https://docs.pydantic.dev/) for data validation
- Managed with [uv](https://docs.astral.sh/uv/) for fast, reliable package management
