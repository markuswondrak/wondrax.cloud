#!/usr/bin/env python3
"""Build blog articles from markdown sources into wondrax.cloud HTML pages."""

import glob
import os
import re
import html
import json
import shutil
from datetime import datetime
from pathlib import Path

import yaml
import markdown

SITE_ROOT = Path(__file__).parent
ARTICLES_SOURCE = SITE_ROOT / "article-sources"
TEMPLATE_PATH = SITE_ROOT / "article_template.html"
BLOG_PATH = SITE_ROOT / "blog.html"
INDEX_PATH = SITE_ROOT / "index.html"
OUTPUT_DIR = SITE_ROOT / "articles"

# Canonical site identity, used for sitemap, feed, JSON-LD and llms.txt.
SITE_URL = "https://markus.wondrax.cloud"
SITE_TITLE = "Markus Wondrak"
SITE_AUTHOR = "Markus Wondrak"
SITE_DESCRIPTION = (
    "Writing on agentic coding, software architecture, "
    "and building meaningful tools."
)
FEED_TITLE = f"{SITE_TITLE} — Articles"
LLMS_PATH = SITE_ROOT / "llms.txt"
LLMS_FULL_PATH = SITE_ROOT / "llms-full.txt"
SITEMAP_PATH = SITE_ROOT / "sitemap.xml"
FEED_PATH = SITE_ROOT / "feed.xml"
ROBOTS_PATH = SITE_ROOT / "robots.txt"

# AI crawlers we explicitly welcome (see robots.txt).
AI_CRAWLERS = [
    "GPTBot",
    "OAI-SearchBot",
    "ChatGPT-User",
    "ClaudeBot",
    "Claude-User",
    "anthropic-ai",
    "PerplexityBot",
    "Google-Extended",
    "Applebot-Extended",
    "CCBot",
    "meta-externalagent",
]

_RFC822_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_RFC822_MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

MARKER_START = "<!-- ARTICLES:START -->"
MARKER_END = "<!-- ARTICLES:END -->"

MD_EXTENSIONS = ["extra", "footnotes", "smarty", "toc", "codehilite", "tables"]
MD_CONFIG = {
    "footnotes": {"BACKLINK_TEXT": "&#8617;"},
    "toc": {"permalink": False},
    "codehilite": {
        "guess_lang": False,
        "css_class": "codehilite",
    },
}

MERMAID_FENCE_RE = re.compile(r"```mermaid\s*\r?\n([\s\S]*?)\r?\n```", re.IGNORECASE)
MATH_INLINE_RE = re.compile(r"\$\$[\s\S]+?\$\$|\$.+?\$", re.DOTALL)
_math_store: list[str] = []


def preprocess_math(text: str) -> str:
    """Replace $...$ and $$...$$ with placeholders before markdown conversion."""
    _math_store.clear()

    def _replace(m: re.Match) -> str:
        _math_store.append(m.group(0))
        return f"MATHPLACEHOLDER{len(_math_store) - 1}ENDMATH"

    return MATH_INLINE_RE.sub(_replace, text)


def postprocess_math(html_text: str) -> str:
    """Restore math placeholders after markdown conversion."""
    for i, expr in enumerate(_math_store):
        html_text = html_text.replace(f"MATHPLACEHOLDER{i}ENDMATH", expr)
    return html_text


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
            print(
                f"  Warning: unparseable date '{date_str}' in {filepath}, using epoch"
            )
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
    text = preprocess_math(text)
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    result = md.convert(text)
    return postprocess_math(result)


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

    slug = article["slug"]
    namespaced_name = f"{slug}_{src.name}"
    images_dir.mkdir(parents=True, exist_ok=True)
    dest = images_dir / namespaced_name
    shutil.copy2(src, dest)
    # Rewrite to path relative to the output HTML file (articles/<slug>.html)
    article["image"] = f"images/{namespaced_name}"
    print(f"  Copied image: {namespaced_name}")


def build_article_page(article: dict, template: str) -> str:
    """Fill the article template with article data."""
    date_iso = article["date"].strftime("%Y-%m-%d")
    date_display = format_date_display(article["date"])
    content_html = render_markdown(article["body"])

    # Build optional HTML fragments
    reading_time_html = ""
    if article["reading_time"]:
        reading_time_html = f'<span class="article-header__time">{html.escape(article["reading_time"])}</span>'

    tags_html = ""
    if article["tags"]:
        tag_spans = "\n".join(
            f'                    <span class="article-header__tag">{html.escape(t)}</span>'
            for t in article["tags"]
        )
        tags_html = (
            f'<div class="article-header__tags">\n{tag_spans}\n                </div>'
        )

    hero_image_html = ""
    if article["image"]:
        safe_src = html.escape(article["image"], quote=True)
        safe_alt = html.escape(article["title"], quote=True)
        hero_image_html = (
            f'<div class="article-hero">'
            f'<img class="article-hero__img" src="{safe_src}" alt="{safe_alt}">'
            f"</div>"
        )

    page = template
    page = page.replace("{{title}}", html.escape(article["title"]))
    page = page.replace("{{excerpt}}", html.escape(article["excerpt"]))
    page = page.replace("{{date_iso}}", date_iso)
    page = page.replace("{{date_display}}", date_display)
    page = page.replace("{{slug}}", article["slug"])
    page = page.replace("{{canonical_url}}", html.escape(article_url(article), quote=True))
    page = page.replace("{{json_ld}}", build_article_json_ld(article))
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

    blog_html = (
        blog_html[:start_idx] + new_section + blog_html[end_idx + len(MARKER_END) :]
    )

    with open(BLOG_PATH, "w", encoding="utf-8") as f:
        f.write(blog_html)

    print(f"  Updated blog.html with {len(articles)} article(s)")


def build_index_teaser(article: dict) -> str:
    """Generate an article teaser for the index.html 'Latest Writing' section."""
    date_iso = article["date"].strftime("%Y-%m-%d")
    date_display = format_date_display(article["date"])
    slug = article["slug"]

    reading_time_html = ""
    if article["reading_time"]:
        reading_time_html = f'\n            <span class="reading-time">{html.escape(article["reading_time"])}</span>'

    tags_html = ""
    if article["tags"]:
        tag_spans = "\n".join(
            f'            <span class="article-tag">{html.escape(t)}</span>'
            for t in article["tags"]
        )
        tags_html = (
            f'\n          <div class="article-tags">\n{tag_spans}\n          </div>'
        )

    return f"""        <article class="article-teaser reveal">
          <div class="article-meta">
            <time datetime="{date_iso}">{date_display}</time>{reading_time_html}
          </div>
          <h3 class="article-title">
            <a href="articles/{slug}.html">{html.escape(article["title"])}</a>
          </h3>
          <p class="article-excerpt">{html.escape(article["excerpt"])}</p>{tags_html}
        </article>"""


def update_index_latest_writing(articles: list[dict], max_items: int = 2) -> None:
    """Replace the content between markers in index.html (Latest Writing)."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_html = f.read()

    start_idx = index_html.find(MARKER_START)
    end_idx = index_html.find(MARKER_END)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find ARTICLES:START/END markers in index.html")
        return

    latest = articles[:max_items]
    entries = "\n\n".join(build_index_teaser(a) for a in latest)
    new_section = f"{MARKER_START}\n{entries}\n        {MARKER_END}"

    index_html = (
        index_html[:start_idx] + new_section + index_html[end_idx + len(MARKER_END) :]
    )

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"  Updated index.html with {len(latest)} latest article(s)")


def article_url(article: dict) -> str:
    """Absolute URL of the rendered article page."""
    return f"{SITE_URL}/articles/{article['slug']}.html"


def article_markdown_url(article: dict) -> str:
    """Absolute URL of the raw markdown source for an article."""
    return f"{SITE_URL}/articles/{article['slug']}.md"


def build_article_json_ld(article: dict) -> str:
    """Return a schema.org BlogPosting JSON-LD script block for an article."""
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article["title"],
        "description": article["excerpt"],
        "datePublished": article["date"].strftime("%Y-%m-%d"),
        "dateModified": article["date"].strftime("%Y-%m-%d"),
        "inLanguage": "en",
        "author": {
            "@type": "Person",
            "name": article["author"] or SITE_AUTHOR,
            "url": f"{SITE_URL}/",
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": article_url(article)},
        "url": article_url(article),
    }
    if article["tags"]:
        data["keywords"] = article["tags"]
    if article["image"]:
        data["image"] = f"{SITE_URL}/articles/{article['image']}"
    # Escape "</" so a stray sequence in the data can't close the script tag.
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{payload}\n</script>'


def build_llms_txt(articles: list[dict]) -> str:
    """Build the llms.txt index: a curated, machine-readable map of the site."""
    lines = [
        f"# {SITE_TITLE}",
        "",
        f"> {SITE_DESCRIPTION}",
        "",
        f"Articles are available as markdown; every link below points to the "
        f"raw source. The full corpus is at {SITE_URL}/llms-full.txt.",
        "",
        "## Articles",
        "",
    ]
    for article in articles:
        lines.append(
            f"- [{article['title']}]({article_markdown_url(article)}): "
            f"{article['excerpt']}"
        )
    return "\n".join(lines) + "\n"


def build_llms_full_txt(articles: list[dict]) -> str:
    """Build llms-full.txt: the entire article corpus as plain markdown."""
    parts = [
        f"# {SITE_TITLE}",
        "",
        f"> {SITE_DESCRIPTION}",
        "",
    ]
    for article in articles:
        meta = [f"Source: {article_url(article)}"]
        meta.append(f"Published: {article['date'].strftime('%Y-%m-%d')}")
        if article["tags"]:
            meta.append(f"Tags: {', '.join(article['tags'])}")
        parts.extend(
            [
                f"## {article['title']}",
                "",
                "\n".join(meta),
                "",
                article["body"],
                "",
                "---",
                "",
            ]
        )
    return "\n".join(parts).rstrip() + "\n"


def build_sitemap(articles: list[dict]) -> str:
    """Build a sitemap.xml covering the home, blog listing and every article."""
    entries = [
        (f"{SITE_URL}/", None),
        (f"{SITE_URL}/blog.html", None),
    ]
    entries += [
        (article_url(a), a["date"].strftime("%Y-%m-%d")) for a in articles
    ]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(loc)}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def _rfc822(date_obj: datetime) -> str:
    """Format a date as an RFC 822 timestamp without depending on the locale."""
    return (
        f"{_RFC822_DAYS[date_obj.weekday()]}, {date_obj.day:02d} "
        f"{_RFC822_MONTHS[date_obj.month - 1]} {date_obj.year} 00:00:00 +0000"
    )


def build_feed(articles: list[dict]) -> str:
    """Build an RSS 2.0 feed of the newest articles."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" '
        'xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/">',
        "  <channel>",
        f"    <title>{html.escape(FEED_TITLE)}</title>",
        f"    <link>{html.escape(SITE_URL)}/</link>",
        f"    <description>{html.escape(SITE_DESCRIPTION)}</description>",
        "    <language>en</language>",
        f'    <atom:link href="{SITE_URL}/feed.xml" rel="self" '
        'type="application/rss+xml"/>',
    ]
    for article in articles:
        lines.extend(
            [
                "    <item>",
                f"      <title>{html.escape(article['title'])}</title>",
                f"      <link>{html.escape(article_url(article))}</link>",
                f"      <guid isPermaLink=\"true\">{html.escape(article_url(article))}</guid>",
                f"      <pubDate>{_rfc822(article['date'])}</pubDate>",
                f"      <description>{html.escape(article['excerpt'])}</description>",
            ]
        )
        if article["author"]:
            lines.append(f"      <dc:creator>{html.escape(article['author'])}</dc:creator>")
        for tag in article["tags"]:
            lines.append(f"      <category>{html.escape(tag)}</category>")
        lines.append("    </item>")
    lines.extend(["  </channel>", "</rss>"])
    return "\n".join(lines) + "\n"


def build_robots_txt() -> str:
    """Build robots.txt that welcomes search engines and AI crawlers."""
    lines = [
        "# All crawlers are welcome.",
        "User-agent: *",
        "Allow: /",
        "",
        "# AI crawlers, explicitly named so a future blanket rule can't hide intent.",
    ]
    for bot in AI_CRAWLERS:
        lines.extend([f"User-agent: {bot}", "Allow: /", ""])
    lines.append(f"Sitemap: {SITE_URL}/sitemap.xml")
    return "\n".join(lines) + "\n"


def write_article_markdown(article: dict) -> None:
    """Copy the raw markdown source next to the rendered article page."""
    source = Path(article["source"])
    dest = OUTPUT_DIR / f"{article['slug']}.md"
    dest.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def write_machine_readable_outputs(articles: list[dict]) -> None:
    """Write the artifacts that make the site accessible to search and LLMs."""
    for article in articles:
        write_article_markdown(article)

    outputs = {
        LLMS_PATH: build_llms_txt(articles),
        LLMS_FULL_PATH: build_llms_full_txt(articles),
        SITEMAP_PATH: build_sitemap(articles),
        FEED_PATH: build_feed(articles),
        ROBOTS_PATH: build_robots_txt(),
    }
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(f"  Generated: {path.name}")


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
    update_index_latest_writing(articles, max_items=2)

    # Machine-readable outputs for search engines and LLMs
    write_machine_readable_outputs(articles)

    print("Done!")


if __name__ == "__main__":
    main()
