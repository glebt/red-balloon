"""Service for loading and analyzing photo metadata."""

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from red_balloon.models import GalleryStats, PhotoMetadata


class PhotoService:
    """Service for managing photo metadata."""

    def __init__(self, data_path: Path) -> None:
        """Initialize with path to JSON data file."""
        self.data_path = data_path
        self._photos: list[PhotoMetadata] | None = None

    def load_photos(self) -> list[PhotoMetadata]:
        """Load photos from JSON file."""
        if self._photos is not None:
            return self._photos

        with open(self.data_path, encoding="utf-8") as f:
            data: list[dict[str, Any]] = json.load(f)

        self._photos = [PhotoMetadata.model_validate(photo) for photo in data]
        return self._photos

    def get_stats(self) -> GalleryStats:
        """Calculate gallery statistics."""
        photos = self.load_photos()

        # Date range
        dates = [p.get_datetime() for p in photos if p.get_datetime()]
        date_range = {
            "earliest": min(dates).isoformat() if dates else None,
            "latest": max(dates).isoformat() if dates else None,
        }

        # Years
        years = sorted({p.get_year() for p in photos if p.get_year()})

        # Cameras
        camera_counts: dict[str, int] = Counter(
            f"{p.make} {p.model}".strip()
            for p in photos
            if p.make or p.model
        )

        # File types
        file_type_counts: dict[str, int] = Counter(
            p.file_type for p in photos if p.file_type
        )

        # Total size (parse from strings like "612 kB")
        total_bytes = 0.0
        for photo in photos:
            if photo.file_size:
                try:
                    size_str = photo.file_size.split()[0]
                    size_val = float(size_str)
                    unit = photo.file_size.split()[1].lower()

                    if unit in ("kb", "kib"):
                        total_bytes += size_val * 1024
                    elif unit in ("mb", "mib"):
                        total_bytes += size_val * 1024 * 1024
                    elif unit in ("gb", "gib"):
                        total_bytes += size_val * 1024 * 1024 * 1024
                    else:
                        total_bytes += size_val  # Assume bytes
                except (ValueError, IndexError):
                    pass

        total_size_mb = total_bytes / (1024 * 1024)

        # ISO range
        iso_values = [p.iso for p in photos if p.iso is not None]
        iso_range = {
            "min": min(iso_values) if iso_values else None,
            "max": max(iso_values) if iso_values else None,
        }

        # Focal lengths
        focal_lengths = sorted(
            {p.focal_length for p in photos if p.focal_length}
        )

        # Most used camera
        most_used_camera = (
            camera_counts.most_common(1)[0][0] if camera_counts else None
        )

        return GalleryStats(
            total_photos=len(photos),
            date_range=date_range,
            years=years,
            cameras=dict(camera_counts),
            file_types=dict(file_type_counts),
            total_size_mb=round(total_size_mb, 2),
            iso_range=iso_range,
            focal_lengths=focal_lengths,
            most_used_camera=most_used_camera,
        )

    def get_photos_by_year(self, year: int) -> list[PhotoMetadata]:
        """Get all photos from a specific year."""
        photos = self.load_photos()
        return [p for p in photos if p.get_year() == year]

    def get_photos_by_camera(self, camera: str) -> list[PhotoMetadata]:
        """Get all photos taken with a specific camera."""
        photos = self.load_photos()
        return [
            p
            for p in photos
            if p.make and p.model and camera.lower() in f"{p.make} {p.model}".lower()
        ]
