#!/usr/bin/env python3
"""Render an article.md to a clean HTML fragment for LinkedIn's article editor.

Usage:
    python render_linkedin.py <path/to/article.md>

The output is written to dist/<folder-name>.html as a bare HTML fragment
(no <html>/<head>/<body> wrapper) ready to paste into LinkedIn.
"""

import argparse
import re
import sys
from pathlib import Path

import markdown


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter delimited by --- blocks."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def render(article_path: Path) -> str:
    source = article_path.read_text(encoding="utf-8")
    body = strip_frontmatter(source)

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "footnotes", "attr_list"],
    )
    return md.convert(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render article.md to LinkedIn-ready HTML.")
    parser.add_argument("article", type=Path, help="Path to article.md")
    args = parser.parse_args()

    article_path: Path = args.article.resolve()
    if not article_path.exists():
        print(f"Error: file not found: {article_path}", file=sys.stderr)
        sys.exit(1)

    html = render(article_path)

    dist_dir = Path(__file__).parent / "dist"
    dist_dir.mkdir(exist_ok=True)

    output_name = article_path.parent.name + ".html"
    output_path = dist_dir / output_name
    output_path.write_text(html, encoding="utf-8")

    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
