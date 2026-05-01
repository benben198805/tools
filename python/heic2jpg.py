# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "Pillow>=10.0.0",
#     "pillow-heif>=0.16.0",
# ]
# ///

"""
HEIC to compressed JPEG converter.

Opens HEIC/HEIF photos (commonly from iPhones) and saves them as
smaller JPEG files with adjustable quality and optional downscaling.
Supports single-file and batch (directory) modes.
"""

from __future__ import annotations

import argparse
import os
import sys

from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIC support with Pillow
register_heif_opener()


def heic_to_compressed_jpg(
    heic_path: str,
    output_path: str | None = None,
    quality: int = 50,
    resize_scale: float = 1.0,
) -> None:
    """Convert a single HEIC file to a compressed JPEG.

    Args:
        heic_path: Path to the source .heic file.
        output_path: Destination .jpg path; auto-derived if None.
        quality: JPEG quality 1-100 (lower = smaller, more lossy).
        resize_scale: 1.0 = original size, 0.8 = 20 % smaller.
    """
    if output_path is None:
        output_path = os.path.splitext(heic_path)[0] + ".jpg"

    try:
        with Image.open(heic_path) as img:
            if resize_scale != 1.0:
                new_width = int(img.width * resize_scale)
                new_height = int(img.height * resize_scale)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            img.save(output_path, "JPEG", quality=quality, optimize=True)

        original_size = os.path.getsize(heic_path) / 1024 / 1024
        new_size = os.path.getsize(output_path) / 1024 / 1024
        ratio = (1 - new_size / original_size) * 100
        print(f"  {os.path.basename(heic_path)}")
        print(
            f"    {original_size:.2f} MB -> {new_size:.2f} MB"
            f"  ({ratio:.0f}% reduction)"
        )

    except Exception as e:
        print(f"  FAILED: {heic_path} — {e}")


def batch_convert(
    folder_path: str,
    quality: int = 50,
    resize_scale: float = 1.0,
) -> int:
    """Convert all .heic files in a directory.

    Returns the number of files successfully converted.
    """
    if not os.path.isdir(folder_path):
        print(f"Directory not found: {folder_path}")
        return 0

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".heic")]
    if not files:
        print(f"No .heic files found in {folder_path}")
        return 0

    print(f"Converting {len(files)} file(s) in {folder_path} ...\n")
    ok = 0
    for filename in sorted(files):
        heic_to_compressed_jpg(
            os.path.join(folder_path, filename),
            quality=quality,
            resize_scale=resize_scale,
        )
        ok += 1
    print(f"\nDone — {ok}/{len(files)} converted.")
    return ok


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert HEIC/HEIF photos to compressed JPEG files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  uv run python/heic2jpg.py photo.heic\n"
            "  uv run python/heic2jpg.py photo.heic -o out.jpg -q 80\n"
            "  uv run python/heic2jpg.py ./photos/ --scale 0.8 -q 40\n"
        ),
    )
    parser.add_argument(
        "target",
        help="Path to a .heic file or a directory containing .heic files",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output .jpg path (single-file mode only; defaults to input name with .jpg)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=50,
        help="JPEG quality 1-100 (default: 50; higher = larger, better quality)",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Resize scale factor (default: 1.0; 0.8 = 20%% smaller dimensions)",
    )

    args = parser.parse_args()

    if os.path.isdir(args.target):
        batch_convert(args.target, quality=args.quality, resize_scale=args.scale)
    else:
        if args.output and os.path.isdir(args.output):
            print("Use -o to specify a filename, not a directory")
            sys.exit(1)
        print(f"Converting {args.target} ...\n")
        heic_to_compressed_jpg(
            args.target,
            output_path=args.output,
            quality=args.quality,
            resize_scale=args.scale,
        )


if __name__ == "__main__":
    main()
