"""Data models for photo metadata."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class PhotoMetadata(BaseModel):
    """Photo metadata from ExifTool."""

    source_file: str = Field(alias="SourceFile")
    file_name: str = Field(alias="FileName")
    directory: str = Field(alias="Directory")
    file_size: str | None = Field(default=None, alias="FileSize")
    file_type: str | None = Field(default=None, alias="FileType")
    mime_type: str | None = Field(default=None, alias="MIMEType")

    # Camera info
    make: str | None = Field(default=None, alias="Make")
    model: str | None = Field(default=None, alias="Model")
    lens_type: str | None = Field(default=None, alias="LensType")

    # Date/time
    date_time_original: str | None = Field(default=None, alias="DateTimeOriginal")
    create_date: str | None = Field(default=None, alias="CreateDate")

    # Exposure settings (can be int, float, or string)
    exposure_time: str | int | float | None = Field(default=None, alias="ExposureTime")
    f_number: float | int | None = Field(default=None, alias="FNumber")
    iso: int | None = Field(default=None, alias="ISO")
    focal_length: str | float | None = Field(default=None, alias="FocalLength")

    # Additional metadata (store as dict for flexibility)
    raw_metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}

    @field_validator("raw_metadata", mode="before")
    @classmethod
    def collect_raw_metadata(cls, v: Any, info: Any) -> dict[str, Any]:
        """Collect all raw metadata during initialization."""
        if hasattr(info, "data") and isinstance(info.data, dict):
            return dict(info.data)
        return v if isinstance(v, dict) else {}

    def get_year(self) -> int | None:
        """Extract year from DateTimeOriginal."""
        if not self.date_time_original:
            return None
        try:
            # Format: "2019:09:22 06:30:14"
            return int(self.date_time_original.split(":")[0])
        except (ValueError, IndexError):
            return None

    def get_datetime(self) -> datetime | None:
        """Parse DateTimeOriginal into datetime object."""
        if not self.date_time_original:
            return None
        try:
            # Format: "2019:09:22 06:30:14"
            return datetime.strptime(self.date_time_original, "%Y:%m:%d %H:%M:%S")
        except ValueError:
            return None


class GalleryStats(BaseModel):
    """Overall statistics for photo gallery."""

    total_photos: int
    date_range: dict[str, str | None] = Field(
        description="Earliest and latest photo dates"
    )
    years: list[int] = Field(description="Years with photos")
    cameras: dict[str, int] = Field(description="Camera models and counts")
    file_types: dict[str, int] = Field(description="File types distribution")
    total_size_mb: float = Field(description="Total size in megabytes")

    # Exposure statistics
    iso_range: dict[str, int | None] = Field(description="ISO range (min/max)")
    focal_lengths: list[str] = Field(description="Unique focal lengths used")
    most_used_camera: str | None = Field(description="Most frequently used camera")
