# Red Balloon

![Red Balloon Project Banner](images/project-banner-red-balloon.jpeg)

## About the Name

The red balloon symbolizes **Ruby** — a language I've loved and worked with extensively. However, I'm making the transition to **Python** because:
- **AI/ML Development**: Python is the de facto standard for AI and machine learning work
- **Industry Requirements**: Modern job interviews and positions increasingly require Python expertise

This project represents both a symbolic farewell to Ruby and a practical demonstration of Python skills in building production-ready AI applications.

## What is Red Balloon?

Red Balloon is an AI-powered **Python** application for exploring and understanding large photo collections. It uses ExifTool to extract image metadata, FastAPI to serve a searchable photo gallery, and local LLMs to analyze images, generate descriptions, and enable natural-language search.

The project demonstrates modern **Python** development, asynchronous processing, API design, and practical AI integration in a scalable, privacy-conscious application.

## Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager

Install uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

### Setup and Run

```bash
# 1. Sync dependencies (creates .venv automatically)
uv sync

# 2. Run the application
uv run python -m red_balloon.main
# Or use the shortcut
uv run red-balloon

# 3. Visit http://localhost:8000
```

### Development Commands

```bash
# Run tests
make test

# Format code
make format

# Start development server with auto-reload
make serve
```

For more details, see [CLAUDE.md](CLAUDE.md).


