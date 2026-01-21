# Contributing to Thunderstore Python SDK

Thank you for your interest in contributing to the Thunderstore Python SDK!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/gongfuture/thunderstore-python-sdk.git
cd thunderstore-python-sdk
```

2. Install uv (if not already installed):
```bash
pip install uv
```

3. Install dependencies:
```bash
uv sync --dev
```

## Running Tests

Run all tests:
```bash
uv run pytest
```

Run with coverage:
```bash
uv run pytest --cov=thunderstore_sdk --cov-report=html
```

Run specific test file:
```bash
uv run pytest tests/test_client.py -v
```

## Code Quality

### Linting

Check code style:
```bash
uv run ruff check .
```

Auto-fix issues:
```bash
uv run ruff check --fix .
```

### Formatting

Check formatting:
```bash
uv run ruff format --check .
```

Format code:
```bash
uv run ruff format .
```

### Type Checking

Run mypy:
```bash
uv run mypy src/
```

## Building the Package

Build the package:
```bash
uv build
```

This creates both source distribution and wheel in the `dist/` directory.

## Project Structure

```
thunderstore-python-sdk/
├── src/thunderstore_sdk/   # Main package code
│   ├── __init__.py         # Package exports
│   ├── client.py           # HTTP client
│   ├── models.py           # Pydantic models
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test suite
│   ├── test_client.py      # Client tests
│   ├── test_models.py      # Model tests
│   └── test_exceptions.py  # Exception tests
├── examples/               # Usage examples
└── .github/workflows/      # CI/CD configuration
```

## Making Changes

1. Create a new branch for your feature/fix
2. Make your changes
3. Add tests for new functionality
4. Run tests and ensure they pass
5. Run linting and type checking
6. Commit your changes with clear messages
7. Submit a pull request

## Code Style Guidelines

- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Follow PEP 8 style guidelines (enforced by ruff)
- Keep functions focused and single-purpose
- Add tests for all new features

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add entries to CHANGELOG if applicable
4. Ensure CI checks pass
5. Request review from maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
