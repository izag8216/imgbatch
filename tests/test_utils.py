"""Tests for imgbatch utilities."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image
from PIL.ExifTags import Base as ExifBase

from imgbatch.utils import (
    collect_images,
    ensure_extension,
    format_to_pillow_format,
    get_exif_date,
    get_image_info,
    parse_rename_pattern,
)


def _make_image(path: Path, size: tuple[int, int] = (100, 80), fmt: str = "PNG") -> None:
    """Helper to create a dummy image."""
    img = Image.new("RGB", size, color=(255, 0, 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format=fmt)


def _make_image_with_exif(path: Path, date_str: str = "2026:04:21 12:00:00") -> None:
    """Helper to create a JPEG with EXIF DateTimeOriginal."""
    img = Image.new("RGB", (100, 80), color=(0, 255, 0))
    exif = img.getexif()
    exif[36867] = date_str  # DateTimeOriginal
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "JPEG", exif=exif)


class TestCollectImages:
    def test_collect_flat(self, tmp_path: Path):
        _make_image(tmp_path / "a.png")
        _make_image(tmp_path / "b.jpg")
        (tmp_path / "c.txt").write_text("hello")
        images = collect_images(tmp_path)
        assert len(images) == 2
        assert all(i.suffix in (".png", ".jpg") for i in images)

    def test_collect_recursive(self, tmp_path: Path):
        _make_image(tmp_path / "sub" / "deep" / "a.png")
        images = collect_images(tmp_path, recursive=True)
        assert len(images) == 1

    def test_collect_empty(self, tmp_path: Path):
        assert collect_images(tmp_path) == []


class TestGetExifDate:
    def test_with_exif(self, tmp_path: Path):
        img_path = tmp_path / "exif.jpg"
        _make_image_with_exif(img_path, "2025:12:25 10:30:00")
        assert get_exif_date(img_path) == "2025-12-25"

    def test_without_exif(self, tmp_path: Path):
        img_path = tmp_path / "noexif.png"
        _make_image(img_path)
        assert get_exif_date(img_path) is None


class TestGetImageInfo:
    def test_valid(self, tmp_path: Path):
        img_path = tmp_path / "info.png"
        _make_image(img_path, (120, 90))
        info = get_image_info(img_path)
        assert info is not None
        assert info["width"] == 120
        assert info["height"] == 90

    def test_invalid(self, tmp_path: Path):
        bad = tmp_path / "bad.txt"
        bad.write_text("not an image")
        assert get_image_info(bad) is None


class TestParseRenamePattern:
    def test_name_and_ext(self, tmp_path: Path):
        path = tmp_path / "photo.png"
        result = parse_rename_pattern("{name}_backup{ext}", path, 1)
        assert result == "photo_backup.png"

    def test_seq_default(self, tmp_path: Path):
        path = tmp_path / "a.jpg"
        result = parse_rename_pattern("img_{seq}{ext}", path, 42)
        assert result == "img_42.jpg"

    def test_seq_padded(self, tmp_path: Path):
        path = tmp_path / "a.jpg"
        result = parse_rename_pattern("img_{seq:0001}{ext}", path, 7)
        assert result == "img_0007.jpg"

    def test_date_fallback_to_mtime(self, tmp_path: Path):
        path = tmp_path / "nodate.png"
        _make_image(path)
        result = parse_rename_pattern("{date}{ext}", path, 1)
        # Should produce some YYYY-MM-DD string
        assert len(result) == len("YYYY-MM-DD.png")
        assert result.endswith(".png")

    def test_width_height(self, tmp_path: Path):
        path = tmp_path / "wh.png"
        _make_image(path, (200, 150))
        result = parse_rename_pattern("{width}x{height}{ext}", path, 1)
        assert result == "200x150.png"


class TestEnsureExtension:
    def test_adds_extension(self):
        assert ensure_extension("photo", "jpg") == "photo.jpg"

    def test_keeps_existing(self):
        assert ensure_extension("photo.jpg", "jpg") == "photo.jpg"

    def test_replaces_wrong(self):
        assert ensure_extension("photo.png", "webp") == "photo.webp"


class TestFormatToPillowFormat:
    def test_jpg(self):
        assert format_to_pillow_format("jpg") == "JPEG"

    def test_tif(self):
        assert format_to_pillow_format("tif") == "TIFF"

    def test_webp(self):
        assert format_to_pillow_format("webp") == "WEBP"
