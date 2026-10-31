# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Red Balloon is an AI-powered Python application for exploring and understanding large photo collections. The application uses:
- **FastAPI** for serving a searchable photo gallery API
- **ExifTool** for extracting image metadata
- **Anthropic Claude** (via OpenRouter) for image analysis and natural-language search
- **Async processing** for handling large photo collections efficiently

## Development Setup

### Initial Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
make install-dev
```

### Environment Configuration
The project uses `.env` for configuration. Required variables:
- `ANTHROPIC_BASE_URL` - API endpoint (default: OpenRouter)
- `ANTHROPIC_AUTH_TOKEN` - API authentication token
- `ANTHROPIC_MODEL` - Model identifier (e.g., anthropic/claude-sonnet-4.5)

Optional variables in `src/red_balloon/config.py`:
- `DEBUG` - Enable debug mode
- `HOST`/`PORT` - Server configuration
- `PHOTOS_DIR` - Photo storage location
- `MAX_UPLOAD_SIZE` - Maximum file upload size

## Common Commands

### Development
- `make run` - Start development server with auto-reload
- `make test` - Run test suite
- `make test-cov` - Run tests with coverage report (generates htmlcov/)
- `make lint` - Check code style and linting issues
- `make format` - Auto-format code with ruff
- `make type-check` - Run mypy type checking

### Running Single Tests
```bash
# Run specific test file
pytest tests/test_main.py

# Run specific test function
pytest tests/test_main.py::test_root_endpoint

# Run with verbose output
pytest -v tests/test_main.py
```

## Architecture

### Project Structure
```
src/red_balloon/          # Main application package
├── __init__.py          # Package initialization
├── main.py              # FastAPI application entry point
├── config.py            # Settings management (pydantic-settings)
└── [future modules]     # API routes, LLM integration, metadata extraction

tests/                   # Test suite
└── test_main.py        # API endpoint tests
```

### Key Design Patterns

**Configuration Management**: Uses `pydantic-settings` for type-safe environment variable loading. All settings centralized in `Settings` class in `config.py`.

**API Structure**: FastAPI application in `main.py` with CORS enabled for cross-origin requests. Application follows async/await patterns throughout for concurrent photo processing.

**Testing**: Async tests using `pytest-asyncio` with ASGI transport for testing FastAPI endpoints without running a server.

### Planned Architecture
- **Photo metadata extraction**: Integrate ExifTool subprocess calls with async processing
- **LLM integration**: Anthropic SDK for image analysis and description generation
- **Vector search**: For natural-language photo search (implementation TBD)
- **Storage**: File-based photo storage with metadata caching

## Code Quality Standards

### Type Checking
- Strict mypy configuration enabled
- All functions must have type annotations
- Tests can omit return type annotations for simplicity

### Linting
- Ruff configured with pycodestyle, pyflakes, isort, pep8-naming, pyupgrade
- 100 character line length limit
- Follow Python 3.11+ idioms

### Testing
- Write async tests for async code
- Maintain test coverage above 80%
- Use descriptive test names following pattern: `test_<functionality>_<scenario>`
- Mock external services (LLM API, ExifTool) in unit tests

## Dependencies

### Core Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `anthropic` - Claude API client
- `pydantic-settings` - Configuration management
- `pillow` - Image processing

### Development Dependencies
- `pytest` with `pytest-asyncio` for testing
- `ruff` for linting and formatting
- `mypy` for type checking
- `httpx` for testing HTTP endpoints

## Notes for Future Development

When implementing new features:
- Add API routes as separate router modules, register in `main.py`
- Keep async/await pattern consistent across codebase
- Extract configuration to `config.py` Settings class
- Write tests before implementation when possible
- Use structured logging for observability (when logger is added)
