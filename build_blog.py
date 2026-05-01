#!/usr/bin/env python3
"""Build blog articles from markdown sources into wondrax.cloud HTML pages."""

import glob
import os
import re
import html
import shutil
from datetime import datetime
from pathlib import Path

import yaml
import markdown

ARTICLES_SOURCE = os.path.expanduser("~/workspace/articles")
SITE_ROOT = Path(__file__).parent
TEMPLATE_PATH = SITE_ROOT / "article_template.html"
BLOG_PATH = SITE_ROOT / "blog.html"
OUTPUT_DIR = SITE_ROOT / "articles"

MARKER_START = "<!-- ARTICLES:START -->"
MARKER_END = "<!-- ARTICLES:END -->"

MD_EXTENSIONS = ["extra", "footnotes", "smarty", "toc", "codehilite", "tables"]
MD_CONFIG = {
    "footnotes": {"BACKLINK_TEXT": "&#8617;"},
    "toc": {"permalink": False},
}

MERMAID_FENCE_RE = re.compile(r"```mermaid\s*\r?\n([\s\S]*?)\r?\n```", re.IGNORECASE)


def preprocess_mermaid_fences(markdown_text: str) -> str:
    """Convert ```mermaid fenced blocks into Mermaid HTML containers.

    We do this before markdown conversion so `codehilite` won't wrap/escape the
    diagram source, and so the template's Mermaid runtime can render it.
    """

    def _replace(match: re.Match) -> str:
        source = match.group(1).strip("\n")
        # Mermaid reads the element text; HTML escaping is safe and prevents
        # accidental HTML injection inside the diagram container.
        safe = html.escape(source, quote=False)
        return f'\n<div class="mermaid">\n{safe}\n</div>\n'

    return MERMAID_FENCE_RE.sub(_replace, markdown_text)


def parse_article(filepath: str) -> dict | None:
    """Parse a markdown file with YAML frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        print(f"  Skipping {filepath}: no frontmatter")
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  Skipping {filepath}: malformed frontmatter")
        return None

    meta = yaml.safe_load(parts[1])
    body = parts[2].strip()

    # Derive slug from folder name if not in frontmatter
    folder = os.path.basename(os.path.dirname(filepath))
    slug = meta.get("slug") or re.sub(r"^\d+_", "", folder)

    # Parse date
    date_str = meta.get("date", "")
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        # Try other formats
        for fmt in ["%B %Y", "%d %B %Y", "%Y-%m-%dT%H:%M:%S"]:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        else:
            print(f"  Warning: unparseable date '{date_str}' in {filepath}, using epoch")
            date_obj = datetime(1970, 1, 1)

    # Auto-extract excerpt from first paragraph if missing
    excerpt = meta.get("excerpt", "")
    if not excerpt:
        first_para = body.split("\n\n")[0] if body else ""
        # Strip markdown formatting for excerpt
        excerpt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", first_para)
        excerpt = re.sub(r"[*_`#]", "", excerpt)
        if len(excerpt) > 200:
            excerpt = excerpt[:197] + "..."

    return {
        "title": meta.get("title", "Untitled"),
        "author": meta.get("author", ""),
        "date": date_obj,
        "date_str": date_str,
        "excerpt": excerpt,
        "tags": meta.get("tags", []),
        "reading_time": meta.get("reading_time", ""),
        "image": meta.get("image", ""),
        "slug": slug,
        "body": body,
        "source": filepath,
    }


def render_markdown(text: str) -> str:
    """Convert markdown to HTML."""
    text = preprocess_mermaid_fences(text)
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    return md.convert(text)


def format_date_display(date_obj: datetime) -> str:
    """Format date as '15 Apr 2026'."""
    return date_obj.strftime("%d %b %Y")


def resolve_article_image(article: dict, images_dir: Path) -> None:
    """Copy the article's image into the site's images dir and update the path in-place."""
    raw = article.get("image", "")
    if not raw:
        return

    source_dir = Path(article["source"]).parent
    src = (source_dir / raw).resolve()

    if not src.exists():
        print(f"  Warning: image not found: {src}")
        article["image"] = ""
        return

    images_dir.mkdir(parents=True, exist_ok=True)
    dest = images_dir / src.name
    shutil.copy2(src, dest)
    # Rewrite to path relative to the output HTML file (articles/<slug>.html)
    article["image"] = f"images/{src.name}"
    print(f"  Copied image: {src.name}")


def build_article_page(article: dict, template: str) -> str:
    """Fill the article template with article data."""
    date_iso = article["date"].strftime("%Y-%m-%d")
    date_display = format_date_display(article["date"])
    content_html = render_markdown(article["body"])

    # Build optional HTML fragments
    reading_time_html = ""
    if article["reading_time"]:
        reading_time_html = (
            f'<span class="article-header__time">{html.escape(article["reading_time"])}</span>'
        )

    tags_html = ""
    if article["tags"]:
        tag_spans = "\n".join(
            f'                    <span class="article-header__tag">{html.escape(t)}</span>'
            for t in article["tags"]
        )
        tags_html = f'<div class="article-header__tags">\n{tag_spans}\n                </div>'

    hero_image_html = ""
    if article["image"]:
        safe_src = html.escape(article["image"], quote=True)
        safe_alt = html.escape(article["title"], quote=True)
        hero_image_html = (
            f'<div class="article-hero">'
            f'<img class="article-hero__img" src="{safe_src}" alt="{safe_alt}">'
            f'</div>'
        )

    page = template
    page = page.replace("{{title}}", html.escape(article["title"]))
    page = page.replace("{{excerpt}}", html.escape(article["excerpt"]))
    page = page.replace("{{date_iso}}", date_iso)
    page = page.replace("{{date_display}}", date_display)
    page = page.replace("{{reading_time_html}}", reading_time_html)
    page = page.replace("{{tags_html}}", tags_html)
    page = page.replace("{{hero_image_html}}", hero_image_html)
    page = page.replace("{{content}}", content_html)

    return page


def build_listing_entry(article: dict) -> str:
    """Generate an article card for the blog listing."""
    date_iso = article["date"].strftime("%Y-%m-%d")
    date_display = format_date_display(article["date"])
    slug = article["slug"]

    reading_time = ""
    if article["reading_time"]:
        reading_time = f'\n                        <span class="article__time">{html.escape(article["reading_time"])}</span>'

    tags_html = ""
    if article["tags"]:
        tag_spans = "\n".join(
            f'                        <span class="article__tag">{html.escape(t)}</span>'
            for t in article["tags"]
        )
        tags_html = f'\n                    <div class="article__tags">\n{tag_spans}\n                    </div>'

    return f"""                <a href="articles/{slug}.html" class="article">
                    <div class="article__meta">
                        <time class="article__date" datetime="{date_iso}">{date_display}</time>{reading_time}
                    </div>
                    <h2 class="article__title">{html.escape(article["title"])}</h2>
                    <p class="article__excerpt">{html.escape(article["excerpt"])}</p>{tags_html}
                </a>"""


def update_blog_listing(articles: list[dict]) -> None:
    """Replace the content between markers in blog.html."""
    with open(BLOG_PATH, "r", encoding="utf-8") as f:
        blog_html = f.read()

    start_idx = blog_html.find(MARKER_START)
    end_idx = blog_html.find(MARKER_END)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find ARTICLES:START/END markers in blog.html")
        return

    entries = "\n\n".join(build_listing_entry(a) for a in articles)
    new_section = f"{MARKER_START}\n\n{entries}\n\n                {MARKER_END}"

    blog_html = blog_html[:start_idx] + new_section + blog_html[end_idx + len(MARKER_END):]

    with open(BLOG_PATH, "w", encoding="utf-8") as f:
        f.write(blog_html)

    print(f"  Updated blog.html with {len(articles)} article(s)")


def main():
    print("Building blog articles...")
    print(f"  Source: {ARTICLES_SOURCE}")
    print(f"  Output: {OUTPUT_DIR}")

    # Find all articles
    pattern = os.path.join(ARTICLES_SOURCE, "*", "article.md")
    article_files = sorted(glob.glob(pattern))

    if not article_files:
        print("  No articles found!")
        return

    print(f"  Found {len(article_files)} article file(s)")

    # Parse articles
    articles = []
    for filepath in article_files:
        article = parse_article(filepath)
        if article:
            articles.append(article)
            print(f"  Parsed: {article['title']}")

    # Sort by date, newest first
    articles.sort(key=lambda a: a["date"], reverse=True)

    # Load template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate individual article pages
    images_dir = OUTPUT_DIR / "images"
    for article in articles:
        resolve_article_image(article, images_dir)
        page_html = build_article_page(article, template)
        output_path = OUTPUT_DIR / f"{article['slug']}.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  Generated: {output_path.name}")

    # Update blog listing
    update_blog_listing(articles)

    print("Done!")


if __name__ == "__main__":
    main()
