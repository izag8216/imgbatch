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
  <strong>オフラインで動作する画像一括リサイズ・変換・トリミング・リネームツール</strong>
</p>

<p align="center">
  <a href="https://github.com/izag8216/imgbatch/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg?style=flat-square" alt="Platform">
</p>

<p align="center">
  <a href="./README.md">English</a>
</p>

---

## 機能

- **リサイズ**: 幅・高さ・倍率指定、アスペクト比自動維持
- **変換**: PNG / JPEG / WEBP / BMP / TIFF 間の一括変換
- **トリミング**: 中心・上下左右からの切り抜き、指定サイズに精密調整
- **リネーム**: EXIF日付・連番・寸法などを使った柔軟なパターン指定
- **パイプライン**: 複数処理を一度のコマンドで連続実行
- **ドライラン**: 実際に変更を加える前にプレビュー
- **HEIF/HEIC** 読み込み対応 (`pillow-heif`)
- **EXIF Orientation** 自動回転
- リッチなターミナル出力（結果テーブル）

## インストール

```bash
pip install imgbatch
```

ソースからインストールする場合:

```bash
git clone https://github.com/izag8216/imgbatch.git
cd imgbatch
pip install -e ".[dev]"
```

## 使い方

### リサイズ

```bash
# 幅指定（高さは自動計算）
imgbatch resize ./photos/ --width 1200

# 倍率指定
imgbatch resize ./photos/ --scale 0.5 --suffix _small

# 別フォルダに出力
imgbatch resize ./photos/ --width 800 --output ./resized/
```

### 変換

```bash
# 全画像を WebP に変換
imgbatch convert ./photos/ --format webp

# 品質指定
imgbatch convert ./photos/ --format jpg --quality 85
```

### トリミング

```bash
# 中心から 1:1 にトリミング
imgbatch crop ./photos/ --width 500 --height 500

# 上側からトリミング
imgbatch crop ./photos/ --width 800 --height 400 --gravity north
```

### リネーム

```bash
# 連番付与
imgbatch rename ./photos/ --pattern "img_{seq:0001}{ext}"

# EXIF日付 + 連番
imgbatch rename ./photos/ --pattern "{date}_{seq}{ext}"

# 画像寸法を含める
imgbatch rename ./photos/ --pattern "{name}_{width}x{height}{ext}"
```

### パイプライン

```bash
# リサイズ → WebP変換 を一括実行
imgbatch process ./photos/ \
  --pipeline "resize,convert" \
  --width 1200 \
  --format webp \
  --output ./output/

# フルパイプライン例
imgbatch process ./photos/ \
  --pipeline "resize,crop,convert,rename" \
  --width 1600 \
  --crop-width 800 \
  --crop-height 800 \
  --format jpg \
  --pattern "batch_{seq:0001}.jpg" \
  --output ./final/
```

### ドライラン

どのコマンドにも `--dry-run` を付けることで、変更内容を事前確認できます:

```bash
imgbatch rename ./photos/ --pattern "{date}{ext}" --dry-run
```

## パターン一覧

| プレースホルダ | 説明 |
|---------------|------|
| `{name}` | 元のファイル名（拡張子なし） |
| `{ext}` | 拡張子（例: `.jpg`） |
| `{seq}` | 連番（1, 2, 3...） |
| `{seq:0001}` | ゼロ埋め連番 |
| `{date}` | EXIF撮影日、ない場合は更新日（YYYY-MM-DD） |
| `{width}` | 画像幅（px） |
| `{height}` | 画像高さ（px） |

## 対応フォーマット

**読み込み:** PNG, JPEG, WEBP, BMP, TIFF, HEIC, HEIF  
**書き出し:** PNG, JPEG, WEBP, BMP, TIFF

## 開発

```bash
pytest
```

Python 3.9 以上が必要です。

## ライセンス

MIT License. 詳細は [LICENSE](./LICENSE) を参照。

サードパーティライセンスは [THIRD_PARTY_LICENSES.md](./THIRD_PARTY_LICENSES.md) に記載。
