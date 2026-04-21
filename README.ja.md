# imgbatch

<p align="center">
  <img src="assets/header.svg" width="100%" alt="imgbatch header">
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
