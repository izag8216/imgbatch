"""Core image processing operations for imgbatch."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image
from rich.console import Console
from rich.table import Table

from imgbatch.utils import (
    collect_images,
    ensure_extension,
    format_to_pillow_format,
    get_image_info,
    parse_rename_pattern,
)

console = Console()


@dataclass
class ProcessResult:
    """Result of a single file operation."""

    source: Path
    destination: Path | None
    success: bool
    message: str


class ImageProcessor:
    """Batch image processor with pipeline support."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.results: list[ProcessResult] = []

    def _open_image(self, path: Path) -> Image.Image:
        """Open image with orientation handling."""
        img = Image.open(path)
        # Auto-rotate based on EXIF Orientation
        try:
            exif = img.getexif()
            if exif is not None:
                orientation = exif.get(274)  # Orientation tag
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        except Exception:
            pass
        return img

    def _save_image(
        self,
        img: Image.Image,
        dest: Path,
        fmt: str,
        quality: int = 90,
    ) -> None:
        """Save image with format-specific options."""
        save_kwargs: dict = {}
        if fmt.upper() in ("JPEG", "JPG"):
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
        elif fmt.upper() == "PNG":
            save_kwargs["optimize"] = True
        elif fmt.upper() == "WEBP":
            save_kwargs["quality"] = quality
            save_kwargs["method"] = 6
        elif fmt.upper() in ("TIFF", "TIF"):
            save_kwargs["compression"] = "tiff_lzw"

        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(dest), format=format_to_pillow_format(fmt), **save_kwargs)

    def resize(
        self,
        source_dir: Path,
        width: int | None = None,
        height: int | None = None,
        scale: float | None = None,
        output_dir: Path | None = None,
        suffix: str = "",
        quality: int = 90,
        recursive: bool = False,
    ) -> list[ProcessResult]:
        """Batch resize images."""
        images = collect_images(source_dir, recursive=recursive)
        results: list[ProcessResult] = []

        for img_path in images:
            try:
                info = get_image_info(img_path)
                if info is None:
                    results.append(
                        ProcessResult(img_path, None, False, "Could not read image info")
                    )
                    continue

                dest_dir = output_dir if output_dir else img_path.parent
                dest_name = f"{img_path.stem}{suffix}{img_path.suffix}"
                dest_path = dest_dir / dest_name

                if self.dry_run:
                    results.append(
                        ProcessResult(
                            img_path,
                            dest_path,
                            True,
                            f"[dry-run] Would resize to {self._describe_resize(info, width, height, scale)}",
                        )
                    )
                    continue

                with self._open_image(img_path) as img:
                    new_size = self._compute_size(img.width, img.height, width, height, scale)
                    if new_size != (img.width, img.height):
                        img = img.resize(new_size, Image.LANCZOS)
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    self._save_image(
                        img,
                        dest_path,
                        fmt=img_path.suffix.lstrip("."),
                        quality=quality,
                    )

                results.append(
                    ProcessResult(
                        img_path,
                        dest_path,
                        True,
                        f"Resized to {new_size[0]}x{new_size[1]}",
                    )
                )
            except Exception as exc:
                results.append(ProcessResult(img_path, None, False, str(exc)))

        self.results.extend(results)
        return results

    def _describe_resize(
        self,
        info: dict,
        width: int | None,
        height: int | None,
        scale: float | None,
    ) -> str:
        w, h = info["width"], info["height"]
        new_size = self._compute_size(w, h, width, height, scale)
        return f"{new_size[0]}x{new_size[1]}"

    def _compute_size(
        self,
        orig_w: int,
        orig_h: int,
        width: int | None,
        height: int | None,
        scale: float | None,
    ) -> tuple[int, int]:
        if scale is not None:
            return (max(1, int(orig_w * scale)), max(1, int(orig_h * scale)))
        if width and height:
            return (width, height)
        if width:
            ratio = width / orig_w
            return (width, max(1, int(orig_h * ratio)))
        if height:
            ratio = height / orig_h
            return (max(1, int(orig_w * ratio)), height)
        return (orig_w, orig_h)

    def convert(
        self,
        source_dir: Path,
        fmt: str,
        output_dir: Path | None = None,
        quality: int = 90,
        recursive: bool = False,
    ) -> list[ProcessResult]:
        """Batch convert image formats."""
        images = collect_images(source_dir, recursive=recursive)
        results: list[ProcessResult] = []
        fmt = fmt.lower()

        for img_path in images:
            try:
                dest_dir = output_dir if output_dir else img_path.parent
                dest_name = ensure_extension(img_path.stem, fmt)
                dest_path = dest_dir / dest_name

                if self.dry_run:
                    results.append(
                        ProcessResult(
                            img_path,
                            dest_path,
                            True,
                            f"[dry-run] Would convert to {fmt.upper()}",
                        )
                    )
                    continue

                with self._open_image(img_path) as img:
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    self._save_image(img, dest_path, fmt, quality=quality)

                results.append(
                    ProcessResult(
                        img_path,
                        dest_path,
                        True,
                        f"Converted to {fmt.upper()}",
                    )
                )
            except Exception as exc:
                results.append(ProcessResult(img_path, None, False, str(exc)))

        self.results.extend(results)
        return results

    def crop(
        self,
        source_dir: Path,
        width: int,
        height: int,
        gravity: str = "center",
        output_dir: Path | None = None,
        recursive: bool = False,
    ) -> list[ProcessResult]:
        """Batch crop images to a target aspect ratio / size."""
        images = collect_images(source_dir, recursive=recursive)
        results: list[ProcessResult] = []

        for img_path in images:
            try:
                dest_dir = output_dir if output_dir else img_path.parent
                dest_path = dest_dir / img_path.name

                if self.dry_run:
                    results.append(
                        ProcessResult(
                            img_path,
                            dest_path,
                            True,
                            f"[dry-run] Would crop to {width}x{height} ({gravity})",
                        )
                    )
                    continue

                with self._open_image(img_path) as img:
                    left, top, right, bottom = self._compute_crop(
                        img.width, img.height, width, height, gravity
                    )
                    img = img.crop((left, top, right, bottom))
                    # Resize the cropped region to exact target dimensions
                    if (img.width, img.height) != (width, height):
                        img = img.resize((width, height), Image.LANCZOS)
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    self._save_image(
                        img,
                        dest_path,
                        fmt=img_path.suffix.lstrip("."),
                    )

                results.append(
                    ProcessResult(
                        img_path,
                        dest_path,
                        True,
                        f"Cropped to {width}x{height} ({gravity})",
                    )
                )
            except Exception as exc:
                results.append(ProcessResult(img_path, None, False, str(exc)))

        self.results.extend(results)
        return results

    def _compute_crop(
        self,
        orig_w: int,
        orig_h: int,
        target_w: int,
        target_h: int,
        gravity: str,
    ) -> tuple[int, int, int, int]:
        ratio = min(orig_w / target_w, orig_h / target_h)
        new_w = int(target_w * ratio)
        new_h = int(target_h * ratio)

        if gravity == "center":
            left = (orig_w - new_w) // 2
            top = (orig_h - new_h) // 2
        elif gravity == "north":
            left = (orig_w - new_w) // 2
            top = 0
        elif gravity == "south":
            left = (orig_w - new_w) // 2
            top = orig_h - new_h
        elif gravity == "east":
            left = orig_w - new_w
            top = (orig_h - new_h) // 2
        elif gravity == "west":
            left = 0
            top = (orig_h - new_h) // 2
        else:
            left = (orig_w - new_w) // 2
            top = (orig_h - new_h) // 2

        return (left, top, left + new_w, top + new_h)

    def rename(
        self,
        source_dir: Path,
        pattern: str,
        output_dir: Path | None = None,
        recursive: bool = False,
    ) -> list[ProcessResult]:
        """Batch rename images using pattern placeholders."""
        images = collect_images(source_dir, recursive=recursive)
        results: list[ProcessResult] = []

        for seq, img_path in enumerate(images, start=1):
            try:
                info = get_image_info(img_path)
                new_name = parse_rename_pattern(pattern, img_path, seq, info)
                # Ensure extension is preserved if not in pattern
                if "." not in new_name:
                    new_name = new_name + img_path.suffix.lower()

                dest_dir = output_dir if output_dir else img_path.parent
                dest_path = dest_dir / new_name

                if self.dry_run:
                    results.append(
                        ProcessResult(
                            img_path,
                            dest_path,
                            True,
                            f"[dry-run] Would rename to {new_name}",
                        )
                    )
                    continue

                # Handle collisions
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(img_path), str(dest_path))

                results.append(
                    ProcessResult(
                        img_path,
                        dest_path,
                        True,
                        f"Renamed to {dest_path.name}",
                    )
                )
            except Exception as exc:
                results.append(ProcessResult(img_path, None, False, str(exc)))

        self.results.extend(results)
        return results

    def process_pipeline(
        self,
        source_dir: Path,
        steps: list[str],
        output_dir: Path | None = None,
        options: dict | None = None,
        recursive: bool = False,
    ) -> list[ProcessResult]:
        """Run a multi-step pipeline on images."""
        opts = options or {}
        current_dir = source_dir
        all_results: list[ProcessResult] = []

        # Work in a temp output dir per step to avoid overwriting
        temp_base = output_dir or source_dir

        for idx, step in enumerate(steps):
            step_out = temp_base / f"_step_{idx + 1}" if len(steps) > 1 else temp_base
            if len(steps) == 1 and output_dir:
                step_out = output_dir

            if step == "resize":
                res = self.resize(
                    current_dir,
                    width=opts.get("width"),
                    height=opts.get("height"),
                    scale=opts.get("scale"),
                    output_dir=step_out,
                    suffix=opts.get("suffix", ""),
                    quality=opts.get("quality", 90),
                    recursive=recursive,
                )
            elif step == "crop":
                w = opts.get("crop_width")
                h = opts.get("crop_height")
                if not w or not h:
                    console.print("[red]crop step requires --crop-width and --crop-height[/red]")
                    break
                res = self.crop(
                    current_dir,
                    width=w,
                    height=h,
                    gravity=opts.get("gravity", "center"),
                    output_dir=step_out,
                    recursive=recursive,
                )
            elif step == "convert":
                fmt = opts.get("format")
                if not fmt:
                    console.print("[red]convert step requires --format[/red]")
                    break
                res = self.convert(
                    current_dir,
                    fmt=fmt,
                    output_dir=step_out,
                    quality=opts.get("quality", 90),
                    recursive=recursive,
                )
            elif step == "rename":
                pattern = opts.get("pattern")
                if not pattern:
                    console.print("[red]rename step requires --pattern[/red]")
                    break
                res = self.rename(
                    current_dir,
                    pattern=pattern,
                    output_dir=step_out,
                    recursive=recursive,
                )
            else:
                console.print(f"[red]Unknown pipeline step: {step}[/red]")
                break

            all_results.extend(res)
            # Next step works on output of current step
            if len(steps) > 1:
                current_dir = step_out

        return all_results


def print_results(results: list[ProcessResult]) -> None:
    """Print a rich table of results."""
    table = Table(title="imgbatch Results", show_lines=True)
    table.add_column("Source", style="cyan", no_wrap=True)
    table.add_column("Destination", style="green")
    table.add_column("Status", style="bold")
    table.add_column("Message", style="dim")

    for r in results:
        status = "[green]OK[/green]" if r.success else "[red]FAIL[/red]"
        dest = str(r.destination) if r.destination else "-"
        table.add_row(str(r.source), dest, status, r.message)

    console.print(table)
