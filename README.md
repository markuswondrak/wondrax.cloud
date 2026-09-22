# wondrax.cloud

Personal homepage — single `index.html`, hosted on GitHub Pages.

## Design

Split-panel layout: linke Seite warm und menschlich (Cremeton, Serifenschrift), rechte Seite kalt und maschinenähnlich (fast schwarz, Monospace). Die Spannung zwischen den beiden Hälften ist die zentrale Idee — der Mensch links, der Entwickler rechts.

**Typografie:** Cormorant Garamond (Bio, Name), DM Sans (Fließtext), IBM Plex Mono (Code/Tags), Space Grotesk (Projekt-Karten)

**Farbpalette:** Warm Cream `#F3EFE6` × Near Black `#0D0D0F` — kein reines Schwarz oder Weiß, alles leicht getönt.

**Projekte:** Cards mit subtilen Hover-Effekten, Tech-Tags als Chips, Links öffnen in neuem Tab.

## Building

Articles live in `article-sources/NN_slug-name/article.md` (Markdown + YAML
frontmatter). To regenerate the whole site, including the machine-readable
outputs below, run:

```sh
python3 build_blog.py
```

Generated files are committed to the repository and served directly by GitHub
Pages:

| File | Purpose |
| --- | --- |
| `articles/<slug>.html` | Rendered article page |
| `articles/<slug>.md` | Raw Markdown copy, advertised via `<link rel="alternate" type="text/markdown">` |
| `llms.txt` | Curated index for LLMs, following [llmstxt.org](https://llmstxt.org) |
| `llms-full.txt` | The entire article corpus as plain Markdown |
| `sitemap.xml` | Home, blog listing and every article, with `lastmod` |
| `feed.xml` | RSS 2.0 feed of the newest articles |
| `robots.txt` | Welcomes search engines and named AI crawlers, points to the sitemap |

Article pages also embed schema.org `BlogPosting` JSON-LD; the homepage embeds
`Person` and `WebSite` JSON-LD. The goal is that search engines and LLMs get
clean, structured content instead of having to scrape rendered HTML.

Tests:

```sh
python3 -m pytest
```

