#!/usr/bin/env python3
"""Create a dated Quarto post from templates/post/index.qmd."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path


def slugify(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") or "post"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Post title")
    parser.add_argument(
        "--date",
        dest="post_date",
        default=date.today().isoformat(),
        help="Publication date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()

    try:
        date.fromisoformat(args.post_date)
    except ValueError:
        parser.error("--date must use YYYY-MM-DD")

    root = Path(__file__).resolve().parents[1]
    template = root / "templates" / "post" / "index.qmd"
    destination = root / "posts" / f"{args.post_date}-{slugify(args.title)}"

    if destination.exists():
        print(f"Refusing to overwrite existing directory: {destination}", file=sys.stderr)
        return 1

    destination.mkdir(parents=True)
    text = template.read_text(encoding="utf-8")
    text = text.replace('title: "POST TITLE"', f'title: "{args.title.replace(chr(34), chr(39))}"')
    text = text.replace('date: "YYYY-MM-DD"', f'date: "{args.post_date}"')
    (destination / "index.qmd").write_text(text, encoding="utf-8")

    print(f"Created {destination.relative_to(root) / 'index.qmd'}")
    print("The post is a draft. Remove 'draft: true' when it is ready to publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
