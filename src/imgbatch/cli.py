"""CLI entry point for imgbatch."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from imgbatch import __version__
from imgbatch.core import ImageProcessor, print_results

console = Console()


def common_options(func):
    """Decorator for common CLI options."""
    func = click.option(
        "--output", "-o", type=click.Path(path_type=Path), help="Output directory"
    )(func)
    func = click.option(
        "--dry-run", is_flag=True, help="Preview changes without writing files"
    )(func)
    func = click.option(
        "--recursive", "-r", is_flag=True, help="Process subdirectories recursively"
    )(func)
    func = click.option(
        "--quality", type=int, default=90, show_default=True, help="JPEG/WEBP quality (1-100)"
    )(func)
    func = click.argument("source", type=click.Path(exists=True, path_type=Path))(func)
    return func


@click.group(invoke_without_command=False)
@click.version_option(version=__version__, prog_name="imgbatch")
def cli():
    """imgbatch -- Image Batch Resizer & Renamer."""
    pass


@cli.command()
@common_options
@click.option("--width", type=int, help="Target width in pixels")
@click.option("--height", type=int, help="Target height in pixels")
@click.option("--scale", type=float, help="Scale factor (e.g. 0.5 for half size)")
@click.option("--suffix", default="", help="Suffix to append to filename stem")
def resize(source, output, dry_run, recursive, quality, width, height, scale, suffix):
    """Batch resize images."""
    if not width and not height and not scale:
        raise click.UsageError("At least one of --width, --height, or --scale is required.")
    processor = ImageProcessor(dry_run=dry_run)
    results = processor.resize(
        source_dir=source,
        width=width,
        height=height,
        scale=scale,
        output_dir=output,
        suffix=suffix,
        quality=quality,
        recursive=recursive,
    )
    print_results(results)


@cli.command()
@common_options
@click.option("--format", "fmt", required=True, help="Output format (png, jpg, webp, bmp, tiff)")
def convert(source, output, dry_run, recursive, quality, fmt):
    """Batch convert image formats."""
    processor = ImageProcessor(dry_run=dry_run)
    results = processor.convert(
        source_dir=source,
        fmt=fmt,
        output_dir=output,
        quality=quality,
        recursive=recursive,
    )
    print_results(results)


@cli.command()
@common_options
@click.option("--width", required=True, type=int, help="Crop width in pixels")
@click.option("--height", required=True, type=int, help="Crop height in pixels")
@click.option(
    "--gravity",
    default="center",
    type=click.Choice(["center", "north", "south", "east", "west"]),
    help="Crop gravity",
)
def crop(source, output, dry_run, recursive, quality, width, height, gravity):
    """Batch crop images."""
    processor = ImageProcessor(dry_run=dry_run)
    results = processor.crop(
        source_dir=source,
        width=width,
        height=height,
        gravity=gravity,
        output_dir=output,
        recursive=recursive,
    )
    print_results(results)


@cli.command()
@common_options
@click.option("--pattern", required=True, help="Rename pattern (e.g. '{date}_{seq:0001}')")
def rename(source, output, dry_run, recursive, quality, pattern):
    """Batch rename images with EXIF-aware patterns."""
    processor = ImageProcessor(dry_run=dry_run)
    results = processor.rename(
        source_dir=source,
        pattern=pattern,
        output_dir=output,
        recursive=recursive,
    )
    print_results(results)


@cli.command()
@common_options
@click.option(
    "--pipeline",
    required=True,
    help='Comma-separated steps: resize,crop,convert,rename (e.g. "resize,convert")',
)
@click.option("--width", type=int, help="Resize width")
@click.option("--height", type=int, help="Resize height")
@click.option("--scale", type=float, help="Resize scale factor")
@click.option("--suffix", default="", help="Resize suffix")
@click.option("--format", "fmt", help="Convert format")
@click.option("--crop-width", type=int, help="Crop width")
@click.option("--crop-height", type=int, help="Crop height")
@click.option(
    "--gravity",
    default="center",
    type=click.Choice(["center", "north", "south", "east", "west"]),
)
@click.option("--pattern", help="Rename pattern")
def process(
    source,
    output,
    dry_run,
    recursive,
    quality,
    pipeline,
    width,
    height,
    scale,
    suffix,
    fmt,
    crop_width,
    crop_height,
    gravity,
    pattern,
):
    """Run a multi-step pipeline on images."""
    steps = [s.strip() for s in pipeline.split(",") if s.strip()]
    if not steps:
        raise click.UsageError("--pipeline must contain at least one step.")

    options = {
        "width": width,
        "height": height,
        "scale": scale,
        "suffix": suffix,
        "format": fmt,
        "crop_width": crop_width,
        "crop_height": crop_height,
        "gravity": gravity,
        "pattern": pattern,
        "quality": quality,
    }

    processor = ImageProcessor(dry_run=dry_run)
    results = processor.process_pipeline(
        source_dir=source,
        steps=steps,
        output_dir=output,
        options=options,
        recursive=recursive,
    )
    print_results(results)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
