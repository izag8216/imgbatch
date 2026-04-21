"""Utility helpers for imgbatch."""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image
from PIL.ExifTags import Base as ExifBase

# Register HEIF opener if available
try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except Exception:  # pragma: no cover
    pass

EXIF_DATE_TAG = 36867  # DateTimeOriginal
SUPPORTED_READ_FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif", ".heic", ".heif"}
SUPPORTED_WRITE_FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}


def collect_images(directory: Path, recursive: bool = False) -> list[Path]:
    """Collect supported image files from a directory."""
    images: list[Path] = []
    pattern = "**/*" if recursive else "*"
    for path in directory.glob(pattern):
        if path.is_file() and path.suffix.lower() in SUPPORTED_READ_FORMATS:
            images.append(path)
    return sorted(images)


def get_exif_date(image_path: Path) -> str | None:
    """Extract DateTimeOriginal from EXIF as YYYY-MM-DD."""
    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            if exif is None:
                return None
            value = exif.get(EXIF_DATE_TAG)
            if not value:
                return None
            # EXIF date format: "YYYY:MM:DD HH:MM:SS"
            dt = datetime.strptime(str(value), "%Y:%m:%d %H:%M:%S")
            return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


def get_image_info(image_path: Path) -> dict[str, Any] | None:
    """Return basic image metadata dict."""
    try:
        with Image.open(image_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "format": img.format,
            }
    except Exception:
        return None


def parse_rename_pattern(
    pattern: str,
    image_path: Path,
    seq: int,
    info: dict[str, Any] | None = None,
) -> str:
    """Replace placeholders in a rename pattern.

    Supported placeholders:
        {name}      - original filename stem
        {ext}       - target extension (dot included)
        {seq}       - sequential number (default 1-based)
        {seq:NNNN}  - zero-padded sequential number
        {date}      - EXIF DateTimeOriginal (YYYY-MM-DD), or file mtime fallback
        {width}     - image width
        {height}    - image height
    """
    result = pattern
    name = image_path.stem
    ext = image_path.suffix.lower()

    # Sequence with optional zero-padding
    seq_match = re.search(r"\{seq(?::(\d+))?\}", result)
    if seq_match:
        padding = len(seq_match.group(1)) if seq_match.group(1) else 1
        seq_str = f"{seq:0{padding}d}"
        result = result.replace(seq_match.group(0), seq_str)

    # Date
    if "{date}" in result:
        date_str = get_exif_date(image_path)
        if date_str is None:
            mtime = image_path.stat().st_mtime
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        result = result.replace("{date}", date_str)

    # Width / Height
    if info is None:
        info = get_image_info(image_path) or {}
    if "{width}" in result:
        result = result.replace("{width}", str(info.get("width", 0)))
    if "{height}" in result:
        result = result.replace("{height}", str(info.get("height", 0)))

    result = result.replace("{name}", name)
    result = result.replace("{ext}", ext)

    return result


def ensure_extension(filename: str, fmt: str) -> str:
    """Ensure filename ends with the correct extension for a given format."""
    fmt = fmt.lower()
    mapping = {
        "jpeg": ".jpg",
        "jpg": ".jpg",
        "png": ".png",
        "webp": ".webp",
        "bmp": ".bmp",
        "tiff": ".tiff",
        "tif": ".tif",
    }
    expected = mapping.get(fmt, f".{fmt}")
    if not filename.lower().endswith(expected):
        # Remove conflicting known extensions
        for ext in SUPPORTED_WRITE_FORMATS:
            if filename.lower().endswith(ext):
                filename = filename[: -len(ext)]
                break
        filename = filename + expected
    return filename


def format_to_pillow_format(fmt: str) -> str:
    """Normalize format string to Pillow format name."""
    fmt = fmt.upper()
    if fmt in ("JPG", "JPEG"):
        return "JPEG"
    if fmt in ("TIF", "TIFF"):
        return "TIFF"
    return fmt
