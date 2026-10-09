#!/usr/bin/env python3
"""Fetch RHP/DRHP PDF from any source (SEBI filing HTML page, exchange ZIP archive, or direct PDF link).

Cleans up all intermediate files, caches, and archives, preserving only the final RHP PDF
(or converting it to Markdown and deleting the PDF if --to-markdown is set).
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Callable

# Ensure analysis repository root is on sys.path for internal imports
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.common.scripts.pdf_to_markdown import convert_pdf_to_markdown

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("fetch_rhp")

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,application/pdf,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def slugify(text: str) -> str:
    """Convert text into a clean URL/filesystem friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def classify_url(url: str) -> str:
    """Determine URL type: 'sebi_html', 'zip', or 'pdf'."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    netloc = parsed.netloc.lower()

    if path.endswith(".zip"):
        return "zip"
    if path.endswith(".pdf"):
        return "pdf"
    if "sebi.gov.in" in netloc:
        if path.endswith(".pdf"):
            return "pdf"
        if path.endswith(".zip"):
            return "zip"
        return "sebi_html"

    # Fallback: Header sniff via HTTP GET
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        content_type = resp.headers.get("Content-Type", "").lower()
        if "pdf" in content_type:
            return "pdf"
        if "zip" in content_type:
            return "zip"
        if "html" in content_type and "sebi.gov.in" in netloc:
            return "sebi_html"

    raise ValueError(f"Unrecognized asset type for URL: {url} (Content-Type: {content_type})")


def fetch_html(url: str) -> str:
    """Fetch HTML content from a URL."""
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_sebi_rhp_info(html: str, page_url: str) -> str:
    """Extract RHP PDF URL from a SEBI filing HTML page."""
    # 1. Main RHP document embedded in viewer iframe (web/?file=...)
    iframe_match = re.search(r"<iframe[^>]+src=['\"][^'\"]*file=([^'\"&]+)", html, re.IGNORECASE)
    pdf_url: str | None = None
    if iframe_match:
        pdf_url = urllib.parse.unquote(iframe_match.group(1).strip())
    else:
        # 2. Fallback: find attachdocs PDF link (skips commondocs abridged prospectus)
        attach_matches = re.findall(
            r"https?://[^\s'\"<>]*(?:sebi_data/attachdocs/)[^\s'\"<>]+\.pdf",
            html,
            re.IGNORECASE,
        )
        if attach_matches:
            pdf_url = attach_matches[0]
        else:
            # 3. Generic fallback: any non-commondocs PDF link
            all_pdfs = re.findall(r"https?://[^\s'\"<>]+\.pdf", html, re.IGNORECASE)
            full_docs = [m for m in all_pdfs if "commondocs" not in m.lower()]
            if full_docs:
                pdf_url = full_docs[0]
            elif all_pdfs:
                pdf_url = all_pdfs[0]

    if not pdf_url:
        raise ValueError("Could not locate RHP PDF URL on the provided SEBI page")

    return urllib.parse.urljoin(page_url, pdf_url)


def safe_extract(zip_path: Path, dest: Path) -> None:
    """Extract zip_path into dest, preventing directory traversal (zip-slip)."""
    dest = dest.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            target = (dest / name).resolve()
            if target != dest and dest not in target.parents:
                raise ValueError(f"Unsafe path in zip: {name!r}")
        zf.extractall(dest)


def find_rhp_pdf(root: Path) -> Path:
    """Pick the RHP PDF from extracted files: prefer final RHP over DRHP, else largest PDF."""
    pdfs = [p for p in root.rglob("*.pdf") if p.is_file()]
    if not pdfs:
        raise FileNotFoundError("No PDF found in extracted archive")

    # Priority 1: Files with 'rhp' but NOT 'drhp'
    rhp_only = [p for p in pdfs if "rhp" in p.name.lower() and "drhp" not in p.name.lower()]
    if rhp_only:
        return max(rhp_only, key=lambda p: p.stat().st_size)

    # Priority 2: Files containing 'rhp', 'drhp', or 'prospectus'
    prospectus_matches = [
        p for p in pdfs
        if any(kw in p.name.lower() for kw in ("rhp", "drhp", "prospectus"))
    ]
    if prospectus_matches:
        return max(prospectus_matches, key=lambda p: p.stat().st_size)

    # Priority 3: Largest PDF
    return max(pdfs, key=lambda p: p.stat().st_size)


def download_file(
    url: str,
    dest: Path,
    max_retries: int = 3,
    progress_callback: Callable[[str], None] | None = None,
) -> None:
    """Download binary file from url to dest with chunking, retries, and progress updates."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")
    dest.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
            with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as out:
                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                chunk_size = 1 << 20  # 1 MB
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    out.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        if total > 0:
                            pct = downloaded / total * 100
                            progress_callback(
                                f"Downloading: {downloaded / 1e6:.1f} / {total / 1e6:.1f} MB ({pct:.0f}%)"
                            )
                        else:
                            progress_callback(f"Downloading: {downloaded / 1e6:.1f} MB")

                if total > 0 and downloaded < total:
                    raise IOError(f"Incomplete download: received {downloaded}/{total} bytes")

            return
        except Exception as exc:
            dest.unlink(missing_ok=True)
            if attempt < max_retries:
                logger.warning("Download attempt %d failed (%s). Retrying...", attempt, exc)
                if progress_callback:
                    progress_callback(f"Download attempt {attempt} failed ({exc}). Retrying...")
            else:
                raise


def resolve_destination(
    url: str,
    output_path: Path | str | None = None,
    company: str | None = None,
) -> Path:
    """Determine the final destination PDF path."""
    if output_path:
        out = Path(output_path).resolve()
        if out.is_dir() or str(output_path).endswith("/") or str(output_path).endswith("\\"):
            return out / "rhp.pdf"
        if out.suffix.lower() != ".pdf":
            return out.with_suffix(".pdf")
        return out

    # Determine company slug
    if company:
        slug = slugify(company)
    else:
        # Fallback: derive slug from URL path
        parsed = urllib.parse.urlparse(url)
        stem = Path(parsed.path).stem
        cleaned = slugify(stem)
        slug = cleaned if len(cleaned) > 2 and cleaned not in ("download", "file", "index") else "default"

    return REPO_ROOT / "tmp" / "company" / "ipo" / slug / "rhp.pdf"


def fetch_rhp(
    url: str,
    output_path: Path | str | None = None,
    company: str | None = None,
    to_markdown: bool = False,
    progress_callback: Callable[[str], None] | None = None,
) -> Path:
    """Fetch RHP/DRHP PDF from a given URL, cleaning up all intermediate files.

    Args:
        url: URL of the filing (SEBI HTML page, exchange ZIP archive, or direct PDF link).
        output_path: Optional custom path or directory.
        company: Optional company name/slug (used for default path under tmp/company/ipo/<company_slug>/).
        to_markdown: If True, converts the downloaded PDF to Markdown and deletes the PDF.
        progress_callback: Optional status callback.

    Returns:
        Path to the saved PDF file (or Markdown file if to_markdown is True).
    """
    dest_pdf = resolve_destination(url=url, output_path=output_path, company=company)
    dest_pdf.parent.mkdir(parents=True, exist_ok=True)

    asset_type = classify_url(url)
    logger.info("Detected asset type: %s for %s", asset_type.upper(), url)
    if progress_callback:
        progress_callback(f"Detected asset type: {asset_type.upper()}")

    try:
        if asset_type == "sebi_html":
            if progress_callback:
                progress_callback("Fetching SEBI filing HTML...")
            html = fetch_html(url)
            pdf_url = extract_sebi_rhp_info(html, url)
            logger.info("Extracted SEBI PDF URL: %s", pdf_url)
            if progress_callback:
                progress_callback("Starting RHP PDF download...")
            download_file(pdf_url, dest_pdf, progress_callback=progress_callback)

        elif asset_type == "zip":
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                temp_zip = temp_path / "archive.zip"
                extract_dir = temp_path / "extracted"
                extract_dir.mkdir(parents=True, exist_ok=True)

                if progress_callback:
                    progress_callback("Downloading ZIP archive...")
                download_file(url, temp_zip, progress_callback=progress_callback)

                if progress_callback:
                    progress_callback("Extracting ZIP archive...")
                safe_extract(temp_zip, extract_dir)

                rhp_pdf_file = find_rhp_pdf(extract_dir)
                logger.info("Identified primary RHP PDF in archive: %s", rhp_pdf_file.name)
                shutil.copy2(str(rhp_pdf_file), str(dest_pdf))
                # All other extracted files and the zip are deleted automatically with temp_dir

        elif asset_type == "pdf":
            if progress_callback:
                progress_callback("Starting direct PDF download...")
            download_file(url, dest_pdf, progress_callback=progress_callback)

        else:
            raise ValueError(f"Unsupported asset type: {asset_type}")

        # Verify PDF magic bytes
        with dest_pdf.open("rb") as f:
            magic = f.read(5)
            if not magic.startswith(b"%PDF"):
                raise ValueError(
                    f"Downloaded file at {dest_pdf} does not appear to be a valid PDF (header: {magic!r}). "
                    "The server may have returned an HTML error/captcha page."
                )

        logger.info("Saved RHP PDF to: %s (%.1f MB)", dest_pdf, dest_pdf.stat().st_size / 1e6)
        if progress_callback:
            progress_callback(f"RHP PDF saved to: {dest_pdf}")

        if to_markdown:
            logger.info("Converting PDF to Markdown and deleting PDF...")
            if progress_callback:
                progress_callback("Converting PDF to Markdown...")
            md_path = convert_pdf_to_markdown(dest_pdf, delete_original=True)
            logger.info("Converted Markdown saved to: %s", md_path)
            return md_path

        return dest_pdf

    except Exception:
        # Guarantee no broken or partial PDF is left behind
        dest_pdf.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch RHP/DRHP PDF from a SEBI page, ZIP archive, or direct PDF link."
    )
    parser.add_argument("url", help="URL of the RHP (SEBI filing page, ZIP file, or direct PDF link).")
    parser.add_argument(
        "-c", "--company",
        type=str,
        default=None,
        help="Company name or slug (used for destination folder tmp/company/ipo/<company_slug>/).",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Custom output file or directory path.",
    )
    parser.add_argument(
        "--to-markdown",
        action="store_true",
        help="Convert downloaded PDF to Markdown at the same location and delete the PDF.",
    )

    args = parser.parse_args()

    try:
        fetch_rhp(
            url=args.url,
            output_path=args.output,
            company=args.company,
            to_markdown=args.to_markdown,
            progress_callback=lambda msg: print(f"-> {msg}"),
        )
    except Exception as exc:
        logger.error("Failed to fetch RHP: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
