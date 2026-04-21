# imgbatch

<p align="center">
  <img src="assets/header.svg" width="100%" alt="imgbatch header">
</p>

<p align="center">
  <strong>Batch image resizer, converter, cropper, and renamer — offline, fast, and pipeline-friendly.</strong>
</p>

<p align="center">
  <a href="https://github.com/izag8216/imgbatch/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg?style=flat-square" alt="Platform">
</p>

<p align="center">
  <a href="./README.ja.md">Japanese / 日本語</a>
</p>

---

## Features

- **Resize** by width, height, or scale factor — with aspect-ratio preservation
- **Convert** between PNG, JPEG, WEBP, BMP, TIFF
- **Crop** to exact dimensions with gravity (center, north, south, east, west)
- **Rename** with EXIF-aware patterns: `{date}`, `{seq}`, `{width}`, `{height}`, `{name}`, `{ext}`
- **Pipeline** multi-step workflows: `resize,crop,convert,rename`
- **Dry-run** mode to preview changes before applying
- **HEIF/HEIC** read support via `pillow-heif`
- **Auto-rotate** images based on EXIF Orientation
- Rich terminal output with result tables

## Installation

```bash
pip install imgbatch
```

Or install from source:

```bash
git clone https://github.com/izag8216/imgbatch.git
cd imgbatch
pip install -e ".[dev]"
```

## Usage

### Resize

```bash
# Resize by width (height auto-scales)
imgbatch resize ./photos/ --width 1200

# Resize by scale factor
imgbatch resize ./photos/ --scale 0.5 --suffix _small

# Output to a different directory
imgbatch resize ./photos/ --width 800 --output ./resized/
```

### Convert

```bash
# Convert all images to WebP
imgbatch convert ./photos/ --format webp

# With quality setting
imgbatch convert ./photos/ --format jpg --quality 85
```

### Crop

```bash
# Center-crop to 1:1 squares
imgbatch crop ./photos/ --width 500 --height 500

# Crop from top (gravity = north)
imgbatch crop ./photos/ --width 800 --height 400 --gravity north
```

### Rename

```bash
# Sequential numbering
imgbatch rename ./photos/ --pattern "img_{seq:0001}{ext}"

# EXIF date + sequence
imgbatch rename ./photos/ --pattern "{date}_{seq}{ext}"

# Include dimensions
imgbatch rename ./photos/ --pattern "{name}_{width}x{height}{ext}"
```

### Pipeline

```bash
# Resize, then convert to WebP — in one pass
imgbatch process ./photos/ \
  --pipeline "resize,convert" \
  --width 1200 \
  --format webp \
  --output ./output/

# Full pipeline: resize, crop, convert, rename
imgbatch process ./photos/ \
  --pipeline "resize,crop,convert,rename" \
  --width 1600 \
  --crop-width 800 \
  --crop-height 800 \
  --format jpg \
  --pattern "batch_{seq:0001}.jpg" \
  --output ./final/
```

### Dry-run

Add `--dry-run` to any command to preview without modifying files:

```bash
imgbatch rename ./photos/ --pattern "{date}{ext}" --dry-run
```

## Pattern Reference

| Placeholder | Description |
|-------------|-------------|
| `{name}` | Original filename (without extension) |
| `{ext}` | File extension (e.g. `.jpg`) |
| `{seq}` | Sequential number (1, 2, 3...) |
| `{seq:0001}` | Zero-padded sequential number |
| `{date}` | EXIF DateTimeOriginal or file mtime (YYYY-MM-DD) |
| `{width}` | Image width in pixels |
| `{height}` | Image height in pixels |

## Supported Formats

**Read:** PNG, JPEG, WEBP, BMP, TIFF, HEIC, HEIF  
**Write:** PNG, JPEG, WEBP, BMP, TIFF

## Development

```bash
pytest
```

Requires Python 3.9+.

## License

MIT License. See [LICENSE](./LICENSE) for details.

Third-party licenses are listed in [THIRD_PARTY_LICENSES.md](./THIRD_PARTY_LICENSES.md).
