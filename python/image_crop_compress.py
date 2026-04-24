# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow",
# ]
# ///
"""
Smart center-crop and resize images (port of Azure ImageCropFunction + EnvironmentConfig).

Supports JPEG, PNG, and WebP (by magic bytes and/or extension). Converts to RGB/RGBA,
applies the same crop rules as the Java version, then scales by COMPRESSION_RATIO.
"""

from __future__ import annotations

import argparse
import io
import logging
import math
import os
import sys
from enum import Enum
from pathlib import Path

from PIL import Image, ImageOps


class Environment(str, Enum):
    UAT = "uat"
    PRODUCTION = "production"


def get_current_environment() -> Environment:
    env = (os.environ.get("ENVIRONMENT") or "uat").lower()
    if env == "production":
        return Environment.PRODUCTION
    return Environment.UAT


def get_log_level() -> str:
    default = "WARN" if get_current_environment() == Environment.PRODUCTION else "INFO"
    return os.environ.get("LOG_LEVEL", default)


def get_compression_ratio() -> float:
    raw = os.environ.get("COMPRESSION_RATIO", "").strip()
    if raw:
        try:
            return float(raw)
        except ValueError:
            print(f"Invalid COMPRESSION_RATIO: {raw!r}, using default 0.3", file=sys.stderr)
    return 0.3


def get_max_dimension() -> int:
    raw = os.environ.get("MAX_DIMENSION", "").strip()
    if raw:
        try:
            return int(raw)
        except ValueError:
            print(f"Invalid MAX_DIMENSION: {raw!r}, using default 4096", file=sys.stderr)
    return 4096


def log_environment_info(log: logging.Logger) -> None:
    log.info("=== Environment Configuration ===")
    log.info("Environment: %s", get_current_environment().value)
    log.info("Log Level: %s", get_log_level())
    log.info("Max Dimension: %s", get_max_dimension())
    log.info("Compression Ratio: %s", get_compression_ratio())
    log.info("==================================")


def detect_image_format(image_bytes: bytes) -> str | None:
    if len(image_bytes) < 3:
        return None
    if len(image_bytes) >= 4 and image_bytes[:4] == b"\x89PNG":
        return "PNG"
    if len(image_bytes) >= 2 and image_bytes[:2] == b"\xff\xd8":
        return "JPEG"
    if len(image_bytes) >= 12 and image_bytes[:4] == b"RIFF":
        if image_bytes[8:12] == b"WEBP":
            return "WEBP"
        return "RIFF"
    return None


def file_extension(name: str) -> str:
    if "." not in name:
        return ""
    return name.rsplit(".", 1)[-1].lower()


def is_supported_format(ext: str, detected: str | None) -> bool:
    if detected:
        if detected in ("PNG", "JPEG", "WEBP"):
            return True
        return False
    if ext:
        return ext in ("jpg", "jpeg", "png", "webp")
    return False


def normalize_format_name(detected: str | None) -> str | None:
    if detected == "JPEG":
        return "JPEG"
    if detected == "PNG":
        return "PNG"
    if detected == "WEBP":
        return "WEBP"
    return None


def compute_crop_rect(
    w: int, h: int, max_dimension: int
) -> tuple[int, int, int, int]:
    if w > 1.25 * h:
        crop_w = int(math.ceil(1.25 * h))
        crop_h = h
        x = int(math.ceil((w - crop_w) / 2.0))
        y = 0
    else:
        crop_w = w
        crop_h = int(math.ceil(0.8 * w))
        x = 0
        y = int(math.ceil((h - crop_h) / 2.0))

    if crop_w > max_dimension or crop_h > max_dimension:
        scale = min(max_dimension / crop_w, max_dimension / crop_h)
        crop_w = int(math.floor(crop_w * scale))
        crop_h = int(math.floor(crop_h * scale))
        x = int(math.ceil((w - crop_w) / 2.0))
        y = int(math.ceil((h - crop_h) / 2.0))

    return x, y, crop_w, crop_h


def to_standard_rgba_or_rgb(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        return im.convert("RGBA")
    return im.convert("RGB")


def compress_image(
    im: Image.Image, compression_ratio: float, log: logging.Logger
) -> Image.Image:
    ow, oh = im.size
    nw = max(1, int(ow * compression_ratio))
    nh = max(1, int(oh * compression_ratio))
    log.info("Compress: %sx%s -> %sx%s", ow, oh, nw, nh)
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def process_image(
    image_bytes: bytes,
    name: str,
    *,
    compression_ratio: float,
    max_dimension: int,
    log: logging.Logger,
) -> tuple[bytes, str] | tuple[None, str]:
    ext = file_extension(name)
    detected = detect_image_format(image_bytes)

    if len(image_bytes) >= 8:
        hx = " ".join(f"{b:02X}" for b in image_bytes[:8])
        log.info("File header (first 8 bytes): %s", hx)

    if not is_supported_format(ext, detected):
        parts = [f"Unsupported image format: {name!s}"]
        if ext:
            parts.append(f"(extension: {ext})")
        if detected:
            parts.append(f"(detected: {detected})")
        else:
            parts.append("(header not recognized)")
        return None, " ".join(parts) + ". Only JPG, PNG, JPEG, WebP are supported."

    if detected and ext:
        match = (
            (ext in ("jpg", "jpeg") and detected == "JPEG")
            or (ext == "png" and detected == "PNG")
            or (ext == "webp" and detected == "WEBP")
        )
        if not match:
            log.info(
                "Note: extension %r does not match detected format %r; continuing.",
                ext,
                detected,
            )

    try:
        im = Image.open(io.BytesIO(image_bytes))
        im.load()
    except OSError as e:
        return None, f"Cannot read image: {e}"

    im = to_standard_rgba_or_rgb(im)
    w, h = im.size
    log.info("Original size: %sx%s", w, h)

    out_fmt = normalize_format_name(detected)
    if not out_fmt:
        if ext in ("jpg", "jpeg"):
            out_fmt = "JPEG"
        elif ext == "png":
            out_fmt = "PNG"
        elif ext == "webp":
            out_fmt = "WEBP"
    if not out_fmt:
        return None, "Cannot determine output format."

    x, y, cw, ch = compute_crop_rect(w, h, max_dimension)
    log.info("Crop: x=%s y=%s width=%s height=%s", x, y, cw, ch)

    if x + cw > w or y + ch > h:
        return None, f"Crop region out of bounds for {name!s}"

    cropped = im.crop((x, y, x + cw, y + ch))
    cropped = to_standard_rgba_or_rgb(cropped)
    log.info("Cropped size: %sx%s", cropped.width, cropped.height)

    compressed = compress_image(cropped, compression_ratio, log)
    log.info(
        "Compressed final: %sx%s (ratio=%.1f%%)",
        compressed.width,
        compressed.height,
        compression_ratio * 100,
    )

    buf = io.BytesIO()
    save_kwargs: dict = {}
    if out_fmt == "JPEG":
        save_kwargs["quality"] = 92
        save_kwargs["optimize"] = True
        if compressed.mode == "RGBA":
            compressed = compressed.convert("RGB")
    elif out_fmt == "WEBP":
        save_kwargs["quality"] = 90
        save_kwargs["method"] = 6

    compressed.save(buf, format=out_fmt, **save_kwargs)
    data = buf.getvalue()
    log.info("Output bytes: %s", len(data))
    return data, out_fmt


def _configure_logging(level_name: str | int) -> logging.Logger:
    if isinstance(level_name, int):
        level = level_name
    else:
        name = str(level_name).strip().upper()
        if name == "WARN":
            name = "WARNING"
        level = getattr(logging, name, logging.INFO)
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")
    return logging.getLogger("image_crop_compress")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Smart crop (Java ImageCropFunction port) + compress; reads JPEG/PNG/WebP.",
    )
    p.add_argument("input", type=Path, help="Input image path.")
    p.add_argument("-o", "--output", type=Path, help="Output path (default: <stem>_cropped<ext>).")
    p.add_argument(
        "--compression-ratio",
        type=float,
        default=None,
        help="Scale factor for dimensions after crop (default: env COMPRESSION_RATIO or 0.3).",
    )
    p.add_argument(
        "--max-dimension",
        type=int,
        default=None,
        help="Max crop width/height (default: env MAX_DIMENSION or 4096).",
    )
    p.add_argument("--log-level", default=None, help="Override LOG_LEVEL for this run.")
    p.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Warnings and errors only (log level WARN).",
    )
    args = p.parse_args()

    if args.log_level is not None:
        level: str | int = args.log_level
    elif args.quiet:
        level = logging.WARNING
    else:
        level = get_log_level()
    log = _configure_logging(level)
    log_environment_info(log)

    inp = args.input.expanduser().resolve()
    if not inp.is_file():
        log.error("Input not found: %s", inp)
        return 1

    ratio = (
        args.compression_ratio
        if args.compression_ratio is not None
        else get_compression_ratio()
    )
    max_dim = args.max_dimension if args.max_dimension is not None else get_max_dimension()

    if ratio <= 0:
        log.error("compression ratio must be positive, got %s", ratio)
        return 1

    data = inp.read_bytes()
    out_bytes, fmt_or_err = process_image(data, inp.name, compression_ratio=ratio, max_dimension=max_dim, log=log)
    if out_bytes is None:
        log.error("%s", fmt_or_err)
        return 1

    if args.output:
        out_path = args.output.expanduser().resolve()
    else:
        suf = ".jpg" if fmt_or_err == "JPEG" else ".png" if fmt_or_err == "PNG" else ".webp"
        out_path = inp.with_name(f"{inp.stem}_cropped{suf}")

    out_path.write_bytes(out_bytes)
    log.info("Wrote %s (%s bytes)", out_path, len(out_bytes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
