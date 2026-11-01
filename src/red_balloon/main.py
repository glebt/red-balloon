"""FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from red_balloon.config import settings
from red_balloon.routes import router as photo_router

app = FastAPI(
    title="Red Balloon",
    description="AI-powered photo collection explorer",
    version="0.1.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include photo routes
app.include_router(photo_router)


@app.get("/")
async def root() -> dict[str, str | bool]:
    """Root endpoint."""
    data_file = Path(settings.data_file)
    return {
        "message": "Red Balloon API",
        "version": "0.1.0",
        "data_file": settings.data_file,
        "data_loaded": data_file.exists(),
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


def main() -> None:
    """Run the application server."""
    import uvicorn

    uvicorn.run(
        "red_balloon.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
