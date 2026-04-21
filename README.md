# imgbatch

<p align="center">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 320" width="100%">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="800" y2="320" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0b1220"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="c1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5eead4"/>
      <stop offset="100%" stop-color="#0d9488"/>
    </linearGradient>
    <linearGradient id="c2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fdba74"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </linearGradient>
    <linearGradient id="c3" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f1f5f9"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>
    <filter id="sh" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="40" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <rect width="800" height="320" fill="url(#bg)"/>
  <circle cx="400" cy="160" r="220" fill="#0f172a" filter="url(#glow)" opacity="0.6"/>

  <!-- Card 1 -->
  <g transform="translate(170, 65) rotate(-8)" filter="url(#sh)">
    <rect width="190" height="150" rx="18" fill="url(#c1)"/>
    <rect x="2" y="2" width="186" height="146" rx="16" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
    <path d="M0 150 L65 85 L115 125 L190 65 L190 150 Z" fill="rgba(0,0,0,0.12)"/>
    <circle cx="145" cy="45" r="18" fill="rgba(255,255,255,0.25)"/>
    <rect x="14" y="14" width="28" height="20" rx="4" fill="rgba(255,255,255,0.2)"/>
    <circle cx="22" cy="22" r="4" fill="rgba(255,255,255,0.5)"/>
  </g>

  <!-- Card 2 -->
  <g transform="translate(290, 95) rotate(5)" filter="url(#sh)">
    <rect width="190" height="150" rx="18" fill="url(#c2)"/>
    <rect x="2" y="2" width="186" height="146" rx="16" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
    <path d="M0 150 L55 95 L105 135 L190 75 L190 150 Z" fill="rgba(0,0,0,0.12)"/>
    <circle cx="135" cy="50" r="16" fill="rgba(255,255,255,0.25)"/>
    <rect x="14" y="14" width="28" height="20" rx="4" fill="rgba(255,255,255,0.2)"/>
    <circle cx="22" cy="22" r="4" fill="rgba(255,255,255,0.5)"/>
  </g>

  <!-- Card 3 -->
  <g transform="translate(410, 55) rotate(-3)" filter="url(#sh)">
    <rect width="190" height="150" rx="18" fill="url(#c3)"/>
    <rect x="2" y="2" width="186" height="146" rx="16" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
    <path d="M0 150 L75 90 L125 120 L190 60 L190 150 Z" fill="rgba(0,0,0,0.1)"/>
    <circle cx="150" cy="42" r="17" fill="rgba(0,0,0,0.08)"/>
    <rect x="14" y="14" width="28" height="20" rx="4" fill="rgba(0,0,0,0.06)"/>
    <circle cx="22" cy="22" r="4" fill="rgba(0,0,0,0.15)"/>
  </g>

  <!-- Decorative particles -->
  <circle cx="120" cy="80" r="5" fill="#334155"/>
  <circle cx="660" cy="240" r="7" fill="#334155"/>
  <circle cx="700" cy="100" r="4" fill="#475569"/>
  <circle cx="95" cy="260" r="6" fill="#475569"/>
  <circle cx="680" cy="70" r="3" fill="#334155"/>
  <circle cx="130" cy="250" r="4" fill="#334155"/>
</svg>
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
