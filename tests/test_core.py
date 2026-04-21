"""Tests for imgbatch core processor."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from imgbatch.core import ImageProcessor, ProcessResult


def _make_image(path: Path, size: tuple[int, int] = (100, 80), fmt: str = "PNG") -> None:
    img = Image.new("RGB", size, color=(255, 0, 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format=fmt)


def _make_image_with_exif(path: Path, date_str: str = "2026:04:21 12:00:00") -> None:
    img = Image.new("RGB", (100, 80), color=(0, 255, 0))
    exif = img.getexif()
    exif[36867] = date_str
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "JPEG", exif=exif)


class TestImageProcessorResize:
    def test_resize_width(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png", (200, 100))
        processor = ImageProcessor(dry_run=False)
        results = processor.resize(src, width=100)
        assert len(results) == 1
        assert results[0].success
        with Image.open(results[0].destination) as img:
            assert img.width == 100
            assert img.height == 50

    def test_resize_height(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png", (200, 100))
        processor = ImageProcessor(dry_run=False)
        results = processor.resize(src, height=50)
        assert results[0].success
        with Image.open(results[0].destination) as img:
            assert img.height == 50
            assert img.width == 100

    def test_resize_scale(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png", (100, 100))
        processor = ImageProcessor(dry_run=False)
        results = processor.resize(src, scale=0.5)
        assert results[0].success
        with Image.open(results[0].destination) as img:
            assert img.width == 50
            assert img.height == 50

    def test_dry_run(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        out = tmp_path / "out"
        _make_image(src / "a.png")
        processor = ImageProcessor(dry_run=True)
        results = processor.resize(src, width=50, output_dir=out)
        assert results[0].success
        assert not results[0].destination.exists()

    def test_output_dir(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        out = tmp_path / "out"
        _make_image(src / "a.png")
        processor = ImageProcessor(dry_run=False)
        results = processor.resize(src, width=50, output_dir=out)
        assert results[0].destination.parent == out


class TestImageProcessorConvert:
    def test_convert_png_to_webp(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        processor = ImageProcessor(dry_run=False)
        results = processor.convert(src, fmt="webp")
        assert len(results) == 1
        assert results[0].success
        assert results[0].destination.suffix == ".webp"
        with Image.open(results[0].destination) as img:
            assert img.format == "WEBP"

    def test_convert_jpg_to_png(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.jpg", fmt="JPEG")
        processor = ImageProcessor(dry_run=False)
        results = processor.convert(src, fmt="png")
        assert results[0].destination.suffix == ".png"


class TestImageProcessorCrop:
    def test_crop_center(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png", (200, 100))
        processor = ImageProcessor(dry_run=False)
        results = processor.crop(src, width=100, height=50)
        assert results[0].success
        with Image.open(results[0].destination) as img:
            assert img.width == 100
            assert img.height == 50

    def test_crop_north(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png", (100, 100))
        processor = ImageProcessor(dry_run=False)
        results = processor.crop(src, width=50, height=50, gravity="north")
        assert results[0].success


class TestImageProcessorRename:
    def test_rename_pattern(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "old.png")
        processor = ImageProcessor(dry_run=False)
        results = processor.rename(src, pattern="new_{seq}{ext}")
        assert len(results) == 1
        assert results[0].success
        assert results[0].destination.name == "new_1.png"

    def test_rename_with_exif_date(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image_with_exif(src / "photo.jpg", "2024:01:15 10:00:00")
        processor = ImageProcessor(dry_run=False)
        results = processor.rename(src, pattern="{date}{ext}")
        assert results[0].destination.name == "2024-01-15.jpg"

    def test_rename_collision(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        _make_image(src / "a_1.png")
        processor = ImageProcessor(dry_run=False)
        results = processor.rename(src, pattern="a{ext}")
        # One should collide and get a suffix
        names = [r.destination.name for r in results]
        assert "a.png" in names
        assert any("a_" in n for n in names)

    def test_dry_run_rename(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        processor = ImageProcessor(dry_run=True)
        results = processor.rename(src, pattern="b{ext}")
        assert results[0].success
        assert (src / "a.png").exists()


class TestImageProcessorPipeline:
    def test_resize_then_convert(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        out = tmp_path / "out"
        _make_image(src / "a.png", (200, 100))
        processor = ImageProcessor(dry_run=False)
        results = processor.process_pipeline(
            source_dir=src,
            steps=["resize", "convert"],
            output_dir=out,
            options={"width": 100, "format": "webp", "quality": 90},
        )
        assert any(r.success for r in results)
        webp_files = list(out.rglob("*.webp"))
        assert len(webp_files) == 1

    def test_invalid_step(self, tmp_path: Path, capsys):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        processor = ImageProcessor(dry_run=False)
        results = processor.process_pipeline(
            source_dir=src,
            steps=["nonexistent"],
            options={},
        )
        # Should break early with no results for the bad step
        assert len(results) == 0
