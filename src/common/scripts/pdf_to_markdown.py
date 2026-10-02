#!/usr/bin/env python3
"""Convert a PDF file to Markdown using PyMuPDF4LLM and remove the original PDF."""

import argparse
import sys
import time
from pathlib import Path
import pymupdf4llm


def convert_pdf_to_markdown(
    pdf_path: str | Path,
    delete_original: bool = True,
) -> Path:
    """Convert a single PDF file to Markdown in the same directory.

    Args:
        pdf_path: Path to the target PDF file.
        delete_original: If True, deletes the source PDF upon successful conversion.

    Returns:
        Path to the generated Markdown file.

    Raises:
        FileNotFoundError: If the PDF does not exist.
        ValueError: If the file is not a .pdf.
        RuntimeError: If conversion produces empty output.
    """
    path = Path(pdf_path).resolve()

    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Target is not a PDF file ({path.suffix}): {path}")

    md_path = path.with_suffix(".md")

    print(f"Converting: {path.name}")
    start_time = time.perf_counter()

    # Convert PDF to Markdown
    markdown_content = pymupdf4llm.to_markdown(str(path))

    if not markdown_content or not markdown_content.strip():
        raise RuntimeError(
            f"Conversion resulted in empty content for {path.name}. PDF was NOT deleted."
        )

    # Write Markdown file in the same directory
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    elapsed = time.perf_counter() - start_time
    md_size_kb = md_path.stat().st_size / 1024
    print(f"Saved: {md_path.name} ({md_size_kb:.1f} KB) in {elapsed:.2f}s")

    # Verify output file before deleting original PDF
    if delete_original:
        if md_path.exists() and md_path.stat().st_size > 0:
            path.unlink()
            print(f"Deleted original PDF: {path.name}")
        else:
            print(
                f"Warning: Output verification failed. Preserving original PDF: {path.name}",
                file=sys.stderr,
            )

    return md_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a PDF to Markdown via PyMuPDF4LLM and delete the original PDF."
    )
    parser.add_argument(
        "pdf_path",
        type=str,
        help="Path to the PDF file to convert.",
    )
    parser.add_argument(
        "--keep-pdf",
        action="store_true",
        help="Keep the original PDF file after conversion (default is to delete).",
    )

    args = parser.parse_args()

    try:
        convert_pdf_to_markdown(
            pdf_path=args.pdf_path,
            delete_original=not args.keep_pdf,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
