# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "Pillow>=10.0.0",
# ]
# ///

"""
Convert PNG images to WebP.

Supports single-file and directory batch conversion. Transparency is preserved
for PNGs with alpha channels or transparent palettes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def is_png(path: Path) -> bool:
    try:
        with path.open("rb") as fp:
            return fp.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE
    except OSError:
        return False


def normalize_image(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA"):
        return img.convert("RGBA")
    if img.mode == "P" and "transparency" in img.info:
        return img.convert("RGBA")
    return img.convert("RGB")


def resize_image(
    img: Image.Image,
    scale: float = 1.0,
    max_dimension: int | None = None,
) -> Image.Image:
    width, height = img.size

    factors = [scale]
    if max_dimension and max(width, height) > max_dimension:
        factors.append(max_dimension / max(width, height))

    factor = min(factors)
    if factor == 1.0:
        return img
    if factor <= 0:
        raise ValueError("scale must be positive")

    new_size = (
        max(1, round(width * factor)),
        max(1, round(height * factor)),
    )
    return img.resize(new_size, Image.Resampling.LANCZOS)


def output_for_file(input_path: Path, output: Path | None) -> Path:
    if output is None:
        return input_path.with_suffix(".webp")
    if output.is_dir():
        return output / f"{input_path.stem}.webp"
    return output


def convert_file(
    input_path: Path,
    output_path: Path,
    quality: int,
    lossless: bool,
    method: int,
    scale: float,
    max_dimension: int | None,
    overwrite: bool,
) -> bool:
    if not input_path.is_file():
        print(f"FAILED: not a file: {input_path}", file=sys.stderr)
        return False
    if not is_png(input_path):
        print(f"FAILED: not a PNG file: {input_path}", file=sys.stderr)
        return False
    if output_path.exists() and not overwrite:
        print(f"FAILED: output exists, use --overwrite: {output_path}", file=sys.stderr)
        return False

    try:
        with Image.open(input_path) as img:
            converted = normalize_image(img)
            converted = resize_image(converted, scale=scale, max_dimension=max_dimension)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            converted.save(
                output_path,
                "WEBP",
                quality=quality,
                lossless=lossless,
                method=method,
            )
    except Exception as e:
        print(f"FAILED: {input_path}: {e}", file=sys.stderr)
        return False

    original_size = input_path.stat().st_size
    new_size = output_path.stat().st_size
    change = (1 - new_size / original_size) * 100 if original_size else 0
    print(f"{input_path} -> {output_path}")
    print(f"  {original_size:,} bytes -> {new_size:,} bytes ({change:.0f}% reduction)")
    return True


def iter_png_files(directory: Path, recursive: bool) -> list[Path]:
    pattern = "**/*.png" if recursive else "*.png"
    return sorted(path for path in directory.glob(pattern) if path.is_file())


def convert_directory(
    directory: Path,
    output_dir: Path | None,
    recursive: bool,
    quality: int,
    lossless: bool,
    method: int,
    scale: float,
    max_dimension: int | None,
    overwrite: bool,
) -> int:
    if not directory.is_dir():
        print(f"Directory not found: {directory}", file=sys.stderr)
        return 1

    files = iter_png_files(directory, recursive=recursive)
    if not files:
        print(f"No PNG files found in {directory}")
        return 0

    print(f"Converting {len(files)} PNG file(s) in {directory} ...\n")
    ok = 0
    for input_path in files:
        if output_dir:
            relative = input_path.relative_to(directory)
            output_path = (output_dir / relative).with_suffix(".webp")
        else:
            output_path = input_path.with_suffix(".webp")
        if convert_file(
            input_path,
            output_path,
            quality=quality,
            lossless=lossless,
            method=method,
            scale=scale,
            max_dimension=max_dimension,
            overwrite=overwrite,
        ):
            ok += 1

    print(f"\nDone: {ok}/{len(files)} converted.")
    return 0 if ok == len(files) else 1


def quality_arg(value: str) -> int:
    quality = int(value)
    if not 1 <= quality <= 100:
        raise argparse.ArgumentTypeError("quality must be between 1 and 100")
    return quality


def method_arg(value: str) -> int:
    method = int(value)
    if not 0 <= method <= 6:
        raise argparse.ArgumentTypeError("method must be between 0 and 6")
    return method


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert PNG images to WebP files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  uv run python/png2webp.py image.png\n"
            "  uv run python/png2webp.py image.png -o image-small.webp -q 70\n"
            "  uv run python/png2webp.py ./screenshots -o ./webp --recursive --lossless\n"
        ),
    )
    parser.add_argument("target", type=Path, help="PNG file or directory of PNG files.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file for single-file mode, or output directory for directory mode.",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=quality_arg,
        default=80,
        help="WebP quality 1-100 for lossy output (default: 80).",
    )
    parser.add_argument(
        "--lossless",
        action="store_true",
        help="Use lossless WebP compression.",
    )
    parser.add_argument(
        "--method",
        type=method_arg,
        default=6,
        help="WebP encoder effort 0-6 (default: 6, slowest/best compression).",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Resize scale factor before encoding (default: 1.0).",
    )
    parser.add_argument(
        "--max-dimension",
        type=int,
        default=None,
        help="Resize so the longest side is at most this many pixels.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="In directory mode, include PNG files in subdirectories.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .webp files.",
    )

    args = parser.parse_args()
    target = args.target.expanduser()
    output = args.output.expanduser() if args.output else None

    if args.scale <= 0:
        parser.error("--scale must be positive")
    if args.max_dimension is not None and args.max_dimension <= 0:
        parser.error("--max-dimension must be positive")

    if target.is_dir():
        return convert_directory(
            target,
            output_dir=output,
            recursive=args.recursive,
            quality=args.quality,
            lossless=args.lossless,
            method=args.method,
            scale=args.scale,
            max_dimension=args.max_dimension,
            overwrite=args.overwrite,
        )

    output_path = output_for_file(target, output)
    return 0 if convert_file(
        target,
        output_path,
        quality=args.quality,
        lossless=args.lossless,
        method=args.method,
        scale=args.scale,
        max_dimension=args.max_dimension,
        overwrite=args.overwrite,
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
