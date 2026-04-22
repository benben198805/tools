# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "PyMuPDF",
# ]
# ///

"""Rasterize PDF pages to JPEG files using PyMuPDF."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import fitz  # PyMuPDF


def find_pdfs_in_dir(directory: Path) -> list[Path]:
    seen: dict[str, Path] = {}
    for p in directory.glob("*.pdf"):
        seen[p.resolve().as_posix()] = p
    for p in directory.glob("*.PDF"):
        seen[p.resolve().as_posix()] = p
    return sorted(seen.values(), key=lambda x: x.name.lower())


def convert_pdf(
    pdf_path: Path,
    output_dir: Path,
    *,
    zoom: float,
    jpg_quality: int,
) -> int:
    """Render all pages to JPEG; returns page count."""
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = pdf_path.stem
    doc = fitz.open(pdf_path)
    try:
        matrix = fitz.Matrix(zoom, zoom)
        n = len(doc)
        for page_num in range(n):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            out_path = output_dir / f"{base_name}_{page_num + 1}.jpg"
            pix.save(out_path.as_posix(), jpg_quality=jpg_quality)
        return n
    finally:
        doc.close()


def collect_inputs(args: argparse.Namespace) -> list[Path]:
    if args.paths:
        files: list[Path] = []
        for raw in args.paths:
            p = Path(raw).expanduser().resolve()
            if not p.is_file():
                print(f"Error: not a file: {p}", file=sys.stderr)
                sys.exit(1)
            if p.suffix.lower() != ".pdf":
                print(f"Error: not a PDF: {p}", file=sys.stderr)
                sys.exit(1)
            files.append(p)
        return files
    input_dir = Path(args.input).expanduser().resolve()
    if not input_dir.is_dir():
        print(f"Error: not a directory: {input_dir}", file=sys.stderr)
        sys.exit(1)
    return find_pdfs_in_dir(input_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert each page of one or more PDFs to JPEG images "
        "(filenames: <stem>_<page>.jpg)."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        metavar="PDF",
        help="PDF files to convert; if omitted, all *.pdf under --input are used.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default=".",
        help="Directory to scan for PDFs when no PDF paths are given (default: .).",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="pdf_to_jpg",
        help="Output directory for JPEG files (default: pdf_to_jpg).",
    )
    parser.add_argument(
        "-z",
        "--zoom",
        type=float,
        default=4.0,
        help="Render scale factor; higher is sharper and larger files (default: 4).",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=95,
        metavar="1-100",
        help="JPEG quality (default: 95).",
    )
    args = parser.parse_args()
    if args.zoom <= 0:
        print("Error: --zoom must be positive.", file=sys.stderr)
        sys.exit(1)
    if not 1 <= args.quality <= 100:
        print("Error: --quality must be between 1 and 100.", file=sys.stderr)
        sys.exit(1)

    pdfs = collect_inputs(args)
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not pdfs:
        print("No PDF files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(pdfs)} PDF(s); writing JPEGs to {output_dir}\n")
    for pdf_path in pdfs:
        try:
            print(f"Converting {pdf_path.name}...")
            n = convert_pdf(pdf_path, output_dir, zoom=args.zoom, jpg_quality=args.quality)
            print(f"Done: {pdf_path.name} ({n} page(s))\n")
        except Exception as e:
            print(f"Failed {pdf_path.name}: {e}\n", file=sys.stderr)

    print(f"Finished. Output directory: {output_dir}")


if __name__ == "__main__":
    main()
