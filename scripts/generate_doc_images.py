#!/usr/bin/env python3
"""Generate documentation images from markdown prompts via OpenRouter.

Uses the Nano Banana Pro (Gemini 3 Pro Image Preview) model to generate
images from prompt files stored in docs/images/prompts/.

Usage:
    # Generate all images
    python scripts/generate_doc_images.py

    # Generate a specific image
    python scripts/generate_doc_images.py 01_tile_types_overview

    # List available prompts
    python scripts/generate_doc_images.py --list

    # Force regenerate (overwrite existing)
    python scripts/generate_doc_images.py --force

Environment:
    OPENROUTER_API_KEY  — required, your OpenRouter API key
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-3-pro-image-preview"

PROMPTS_DIR = Path("docs/images/prompts")
OUTPUT_DIR = Path("docs/images/generated")

# ---------------------------------------------------------------------------
# Prompt parsing
# ---------------------------------------------------------------------------


def parse_prompt_file(path: Path) -> dict:
    """Parse a prompt markdown file into metadata + prompt text.

    Expected format:
        # Title
        > **Target:** `some/file.rst`
        > **Style:** description
        > **Aspect:** 16:9 landscape

        ## Prompt
        <the actual prompt text>
    """
    text = path.read_text()
    lines = text.strip().splitlines()

    meta: dict = {"title": "", "target": "", "style": "", "aspect": "", "prompt": ""}

    # Title from first heading
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            meta["title"] = line.lstrip("# ").strip()
            break

    # Metadata from blockquote lines
    for line in lines:
        if "**Target:**" in line:
            m = re.search(r"\*\*Target:\*\*\s*`?([^`\n]+)`?", line)
            if m:
                meta["target"] = m.group(1).strip()
        if "**Style:**" in line:
            m = re.search(r"\*\*Style:\*\*\s*(.+)", line)
            if m:
                meta["style"] = m.group(1).strip()
        if "**Aspect:**" in line:
            m = re.search(r"\*\*Aspect:\*\*\s*(.+)", line)
            if m:
                meta["aspect"] = m.group(1).strip()

    # Prompt text: everything after "## Prompt"
    prompt_started = False
    prompt_lines: list[str] = []
    for line in lines:
        if line.strip().startswith("## Prompt"):
            prompt_started = True
            continue
        if prompt_started:
            prompt_lines.append(line)

    meta["prompt"] = "\n".join(prompt_lines).strip()
    return meta


# ---------------------------------------------------------------------------
# OpenRouter API
# ---------------------------------------------------------------------------


def generate_image(prompt: str, api_key: str) -> bytes | None:
    """Call OpenRouter Nano Banana Pro and return PNG bytes, or None."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/ghiret/lanelet2od",
        "X-Title": "xodrtools-doc-images",
    }

    payload = {
        "model": MODEL,
        "modalities": ["image", "text"],
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": 4096,
    }

    print(f"  → Calling {MODEL} via OpenRouter...")
    t0 = time.time()

    with httpx.Client(timeout=120.0) as client:
        resp = client.post(OPENROUTER_URL, headers=headers, json=payload)

    elapsed = time.time() - t0
    print(f"  → Response in {elapsed:.1f}s (status {resp.status_code})")

    if resp.status_code != 200:
        print(f"  ✗ API error: {resp.text[:500]}")
        return None

    data = resp.json()

    # Debug: save raw response for troubleshooting
    debug_path = OUTPUT_DIR / "_last_response.json"
    debug_path.write_text(json.dumps(data, indent=2, default=str))

    # Extract image from response
    # The response format varies — check for inline_data, images, or
    # base64 data URLs in the content.
    choices = data.get("choices", [])
    if not choices:
        print("  ✗ No choices in response")
        return None

    message = choices[0].get("message", {})

    # Format 1: message.images[] (OpenRouter normalised format)
    images = message.get("images", [])
    if images:
        image_url = images[0].get("image_url", {}).get("url", "")
        if image_url.startswith("data:image/"):
            return _decode_data_url(image_url)

    # Format 2: base64 data URL embedded in content parts
    content = message.get("content", "")
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict):
                # inline_data format
                if "inline_data" in part:
                    b64 = part["inline_data"].get("data", "")
                    if b64:
                        return base64.b64decode(b64)
                # image_url format
                if part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:image/"):
                        return _decode_data_url(url)
    elif isinstance(content, str):
        # Check for embedded data URL in text
        m = re.search(r"data:image/[^;]+;base64,([A-Za-z0-9+/=]+)", content)
        if m:
            return base64.b64decode(m.group(1))

    print("  ✗ Could not find image in response")
    print(f"    Message keys: {list(message.keys())}")
    if isinstance(content, list):
        print(f"    Content parts: {[type(p).__name__ for p in content]}")
    elif isinstance(content, str):
        print(f"    Content (first 200 chars): {content[:200]}")
    return None


def _decode_data_url(data_url: str) -> bytes:
    """Decode a data:image/...;base64,... URL to bytes."""
    _, b64_data = data_url.split(",", 1)
    return base64.b64decode(b64_data)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def get_available_prompts() -> list[Path]:
    """Return sorted list of prompt files."""
    if not PROMPTS_DIR.exists():
        return []
    return sorted(PROMPTS_DIR.glob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate documentation images from markdown prompts"
    )
    parser.add_argument(
        "prompts",
        nargs="*",
        help="Specific prompt names to generate (e.g. '01_tile_types_overview'). Omit to generate all.",
    )
    parser.add_argument(
        "--list", action="store_true", help="List available prompts and exit"
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing images"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse prompts and show what would be generated, without calling the API",
    )
    parser.add_argument(
        "--prompts-dir",
        type=Path,
        default=None,
        help="Custom prompts directory (default: docs/images/prompts)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Custom output directory (default: docs/images/generated)",
    )
    args = parser.parse_args()

    global PROMPTS_DIR, OUTPUT_DIR
    if args.prompts_dir:
        PROMPTS_DIR = args.prompts_dir
    if args.output_dir:
        OUTPUT_DIR = args.output_dir

    available = get_available_prompts()

    if args.list:
        print("Available prompts:")
        for p in available:
            meta = parse_prompt_file(p)
            stem = p.stem
            out = OUTPUT_DIR / f"{stem}.png"
            status = "✓ exists" if out.exists() else "○ not generated"
            print(f"  {stem}  [{status}]")
            print(f"    Title:  {meta['title']}")
            print(f"    Target: {meta['target']}")
        return 0

    # Filter to requested prompts
    if args.prompts:
        selected = []
        for name in args.prompts:
            # Allow with or without .md extension
            name = name.removesuffix(".md")
            path = PROMPTS_DIR / f"{name}.md"
            if not path.exists():
                print(f"✗ Prompt not found: {path}")
                return 1
            selected.append(path)
    else:
        selected = available

    if not selected:
        print("No prompts found. Create .md files in docs/images/prompts/")
        return 1

    # Check API key
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key and not args.dry_run:
        print("✗ OPENROUTER_API_KEY environment variable not set")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate
    results: list[tuple[str, bool]] = []
    for prompt_path in selected:
        stem = prompt_path.stem
        out_path = OUTPUT_DIR / f"{stem}.png"

        print(f"\n{'=' * 60}")
        print(f"Processing: {stem}")
        print(f"{'=' * 60}")

        meta = parse_prompt_file(prompt_path)
        print(f"  Title:  {meta['title']}")
        print(f"  Target: {meta['target']}")
        print(f"  Prompt: {meta['prompt'][:80]}...")

        if out_path.exists() and not args.force:
            print("  ⏭ Skipping (already exists). Use --force to regenerate.")
            results.append((stem, True))
            continue

        if args.dry_run:
            print(f"  [dry-run] Would generate → {out_path}")
            results.append((stem, True))
            continue

        image_bytes = generate_image(meta["prompt"], api_key)
        if image_bytes:
            out_path.write_bytes(image_bytes)
            size_kb = len(image_bytes) / 1024
            print(f"  ✓ Saved {out_path} ({size_kb:.0f} KB)")
            results.append((stem, True))
        else:
            print("  ✗ Failed to generate image")
            results.append((stem, False))

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary:")
    for name, ok in results:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}")
    print(f"{'=' * 60}")

    failed = sum(1 for _, ok in results if not ok)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
