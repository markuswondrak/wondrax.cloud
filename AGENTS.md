This is a repository for all my articles about topics.

- Files are written in Markdown
- All assumptions must be evaluated and proven by sources

## Article Structure

Each article lives in its own directory: `NN_slug-name/article.md`

### Frontmatter Convention

Every `article.md` must include YAML frontmatter with the following fields:

```yaml
---
title: "Article Title"              # Required
author: "Markus Wondrak"            # Required
date: "2026-04-15"                  # Required — ISO date (YYYY-MM-DD) for sorting
excerpt: "One-liner for listings"   # Optional — auto-extracted from first paragraph if missing
tags: ["Tag1", "Tag2"]              # Optional — displayed on blog listing and article page
reading_time: "8 min read"          # Optional — displayed in article metadata
slug: "article-slug"                # Optional — derived from folder name if missing
---
```

The `date` field should use ISO format (`YYYY-MM-DD`) to enable correct chronological sorting on the blog.

## Build

After adding or editing an article, run `python3 build_blog.py`. It regenerates
the article HTML pages, the blog/index listings, and the machine-readable
artifacts (`llms.txt`, `llms-full.txt`, `sitemap.xml`, `feed.xml`, and per-article
`.md` copies). Commit the generated files — GitHub Pages serves them directly.

