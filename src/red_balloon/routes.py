"""API routes for photo gallery."""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from red_balloon.config import settings
from red_balloon.models import GalleryStats, PhotoMetadata
from red_balloon.photo_service import PhotoService

router = APIRouter(prefix="/api", tags=["photos"])

# Initialize photo service with configured data file
photo_service = PhotoService(Path(settings.data_file))


@router.get("/stats", response_model=GalleryStats)
async def get_gallery_stats() -> GalleryStats:
    """Get overall gallery statistics."""
    try:
        return photo_service.get_stats()
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"Data file not found: {settings.data_file}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading statistics: {str(e)}"
        ) from e


@router.get("/photos/year/{year}", response_model=list[PhotoMetadata])
async def get_photos_by_year(year: int) -> list[PhotoMetadata]:
    """Get all photos from a specific year."""
    try:
        photos = photo_service.get_photos_by_year(year)
        if not photos:
            raise HTTPException(
                status_code=404, detail=f"No photos found for year {year}"
            )
        return photos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching photos: {str(e)}"
        ) from e


@router.get("/photos/camera/{camera}")
async def get_photos_by_camera(camera: str) -> list[PhotoMetadata]:
    """Get all photos taken with a specific camera model."""
    try:
        photos = photo_service.get_photos_by_camera(camera)
        if not photos:
            raise HTTPException(
                status_code=404, detail=f"No photos found for camera: {camera}"
            )
        return photos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching photos: {str(e)}"
        ) from e


@router.get("/years")
async def get_available_years() -> list[int]:
    """Get list of all available years in the gallery."""
    try:
        photos = photo_service.load_photos()
        years = sorted({p.get_year() for p in photos if p.get_year()})
        return years
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching years: {str(e)}"
        ) from e


@router.get("/cameras")
async def get_available_cameras() -> dict[str, int]:
    """Get list of all cameras with photo counts."""
    try:
        photos = photo_service.load_photos()
        cameras: dict[str, int] = {}
        for photo in photos:
            if photo.make or photo.model:
                camera_name = f"{photo.make} {photo.model}".strip()
                cameras[camera_name] = cameras.get(camera_name, 0) + 1

        # Sort by count (descending)
        return dict(sorted(cameras.items(), key=lambda x: x[1], reverse=True))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching cameras: {str(e)}"
        ) from e


@router.get("/info")
async def get_data_info() -> dict[str, str]:
    """Get information about the loaded dataset."""
    data_path = Path(settings.data_file)
    return {
        "data_file": settings.data_file,
        "exists": str(data_path.exists()),
        "size_mb": (
            f"{data_path.stat().st_size / (1024 * 1024):.2f}"
            if data_path.exists()
            else "N/A"
        ),
        "description": (
            "2019 photos only (dev/testing)"
            if "2019" in settings.data_file
            else "All photos"
        ),
    }
