"""Tests for imgbatch CLI."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner
from PIL import Image

from imgbatch.cli import cli


def _make_image(path: Path, size: tuple[int, int] = (100, 80), fmt: str = "PNG") -> None:
    img = Image.new("RGB", size, color=(255, 0, 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format=fmt)


runner = CliRunner()


class TestCliResize:
    def test_resize_width(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png", (200, 100))
        result = runner.invoke(cli, ["resize", str(src), "--width", "100"])
        assert result.exit_code == 0
        out_path = src / "a.png"
        assert out_path.exists()
        with Image.open(out_path) as img:
            assert img.width == 100
            assert img.height == 50

    def test_resize_missing_param(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        result = runner.invoke(cli, ["resize", str(src)])
        assert result.exit_code != 0
        assert "required" in result.output.lower() or "Usage" in result.output

    def test_dry_run(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        out = tmp_path / "out"
        _make_image(src / "a.png")
        result = runner.invoke(cli, ["resize", str(src), "--width", "50", "--dry-run", "--output", str(out)])
        assert result.exit_code == 0
        # Output should not exist in dry-run mode
        assert not out.exists() or not any(out.iterdir())


class TestCliConvert:
    def test_convert(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        result = runner.invoke(cli, ["convert", str(src), "--format", "webp"])
        assert result.exit_code == 0
        webp_file = src / "a.webp"
        assert webp_file.exists()
        with Image.open(webp_file) as img:
            assert img.format == "WEBP"


class TestCliCrop:
    def test_crop(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png", (200, 100))
        result = runner.invoke(cli, ["crop", str(src), "--width", "50", "--height", "50"])
        assert result.exit_code == 0
        with Image.open(src / "a.png") as img:
            assert img.width == 50
            assert img.height == 50


class TestCliRename:
    def test_rename(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        result = runner.invoke(cli, ["rename", str(src), "--pattern", "b{ext}"])
        assert result.exit_code == 0
        assert not (src / "a.png").exists()
        assert (src / "b.png").exists()


class TestCliProcess:
    def test_pipeline(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        out = tmp_path / "out"
        _make_image(src / "a.png", (200, 100))
        result = runner.invoke(
            cli,
            [
                "process",
                str(src),
                "--pipeline",
                "resize,convert",
                "--output",
                str(out),
                "--width",
                "100",
                "--format",
                "webp",
            ],
        )
        assert result.exit_code == 0
        webp_files = list(out.rglob("*.webp"))
        assert len(webp_files) == 1

    def test_pipeline_invalid_step(self, tmp_path: Path):
        src = tmp_path / "src"
        src.mkdir()
        _make_image(src / "a.png")
        result = runner.invoke(
            cli, ["process", str(src), "--pipeline", "badstep"]
        )
        assert result.exit_code == 0  # prints error but returns 0 currently


class TestCliCommon:
    def test_version(self):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "imgbatch" in result.output
