#!/usr/bin/env python3
"""Tests for build_blog.py image handling and machine-readable outputs."""

import json
import shutil
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from build_blog import (
    build_article_json_ld,
    build_feed,
    build_llms_full_txt,
    build_llms_txt,
    build_robots_txt,
    build_sitemap,
    resolve_article_image,
    write_article_markdown,
)


def make_article(**overrides):
    """A representative article dict as produced by parse_article()."""
    article = {
        "title": "The Agent is not the Pipeline",
        "author": "Markus Wondrak",
        "date": datetime(2026, 5, 14),
        "date_str": "2026-05-14",
        "excerpt": "Agents are probabilistic by design.",
        "tags": ["Agentic Coding", "Spec Kit"],
        "reading_time": "13 min read",
        "image": "images/deterministic-pipelines_infografik.png",
        "slug": "deterministic-pipelines",
        "body": "The agent had been running for forty minutes.",
        "source": "/tmp/article-sources/03_deterministic_pipelines/article.md",
    }
    article.update(overrides)
    return article


class TestResolveArticleImage:
    """Test image resolution and copying with slug-based namespacing."""

    def setup_method(self):
        """Create temporary directories for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.images_dir = Path(self.temp_dir) / "images"
        self.source_dir = Path(self.temp_dir) / "source"
        self.source_dir.mkdir()

    def teardown_method(self):
        """Clean up temporary directories."""
        shutil.rmtree(self.temp_dir)

    def test_image_copies_with_slug_prefix(self):
        """Images from different articles with same filename should not collide."""
        # Create a test image in source
        test_image = self.source_dir / "hero.jpg"
        test_image.write_bytes(b"test image content")

        article = {
            "image": "hero.jpg",
            "source": str(self.source_dir / "article.md"),
            "slug": "my-article",
        }

        resolve_article_image(article, self.images_dir)

        # Check that the image was copied with slug prefix
        expected_dest = self.images_dir / "my-article_hero.jpg"
        assert expected_dest.exists(), f"Expected {expected_dest} to exist"
        assert article["image"] == "images/my-article_hero.jpg"

    def test_different_articles_same_filename_no_collision(self):
        """Two articles with same image filename should produce different output files."""
        # Create two source directories simulating two articles
        source1 = Path(self.temp_dir) / "article1"
        source2 = Path(self.temp_dir) / "article2"
        source1.mkdir()
        source2.mkdir()

        # Both have an image named "hero.jpg" but with different content
        img1 = source1 / "hero.jpg"
        img2 = source2 / "hero.jpg"
        img1.write_bytes(b"article 1 image")
        img2.write_bytes(b"article 2 image")

        article1 = {
            "image": "hero.jpg",
            "source": str(source1 / "article.md"),
            "slug": "first-article",
        }
        article2 = {
            "image": "hero.jpg",
            "source": str(source2 / "article.md"),
            "slug": "second-article",
        }

        resolve_article_image(article1, self.images_dir)
        resolve_article_image(article2, self.images_dir)

        # Both images should exist with different names
        dest1 = self.images_dir / "first-article_hero.jpg"
        dest2 = self.images_dir / "second-article_hero.jpg"

        assert dest1.exists(), "First article image should exist"
        assert dest2.exists(), "Second article image should exist"
        assert dest1.read_bytes() == b"article 1 image"
        assert dest2.read_bytes() == b"article 2 image"
        assert article1["image"] == "images/first-article_hero.jpg"
        assert article2["image"] == "images/second-article_hero.jpg"

    def test_no_image_in_frontmatter(self):
        """Articles without image should not create any files."""
        article = {
            "image": "",
            "source": str(self.source_dir / "article.md"),
            "slug": "my-article",
        }

        resolve_article_image(article, self.images_dir)

        assert not self.images_dir.exists()
        assert article["image"] == ""

    def test_missing_image_file(self):
        """Missing image file should result in empty image path."""
        article = {
            "image": "nonexistent.jpg",
            "source": str(self.source_dir / "article.md"),
            "slug": "my-article",
        }

        resolve_article_image(article, self.images_dir)

        assert article["image"] == ""
        assert not self.images_dir.exists()


class TestArticleJsonLd:
    def test_json_ld_is_valid_and_typed(self):
        script = build_article_json_ld(make_article())
        assert script.startswith('<script type="application/ld+json">')
        payload = script.split(">", 1)[1].rsplit("</script>", 1)[0]
        data = json.loads(payload)

        assert data["@type"] == "BlogPosting"
        assert data["headline"] == "The Agent is not the Pipeline"
        assert data["datePublished"] == "2026-05-14"
        assert data["author"]["name"] == "Markus Wondrak"
        assert data["keywords"] == ["Agentic Coding", "Spec Kit"]
        assert data["url"].endswith("/articles/deterministic-pipelines.html")
        assert data["image"].endswith(
            "/articles/images/deterministic-pipelines_infografik.png"
        )

    def test_script_closing_sequence_is_escaped(self):
        article = make_article(excerpt="</script><script>alert(1)</script>")
        script = build_article_json_ld(article)
        assert "</script><script>alert" not in script
        assert "<\\/script>" in script


class TestLlmsTxt:
    def test_index_links_markdown_sources(self):
        content = build_llms_txt([make_article()])
        assert content.startswith("# Markus Wondrak")
        assert "https://markus.wondrax.cloud/articles/deterministic-pipelines.md" in content
        assert "Agents are probabilistic by design." in content

    def test_full_text_contains_every_body(self):
        articles = [
            make_article(slug="one", body="First body."),
            make_article(slug="two", body="Second body."),
        ]
        content = build_llms_full_txt(articles)
        assert content.count("## The Agent is not the Pipeline") == 2
        assert "First body." in content
        assert "Second body." in content


class TestSitemap:
    def test_sitemap_parses_and_lists_pages(self):
        root = ET.fromstring(build_sitemap([make_article()]))
        locs = [
            url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
            for url in root
        ]
        assert "https://markus.wondrax.cloud/" in locs
        assert "https://markus.wondrax.cloud/blog.html" in locs
        assert "https://markus.wondrax.cloud/articles/deterministic-pipelines.html" in locs


class TestFeed:
    def test_feed_parses_and_has_items(self):
        root = ET.fromstring(build_feed([make_article()]))
        channel = root.find("channel")
        titles = [item.find("title").text for item in channel.findall("item")]

        assert titles == ["The Agent is not the Pipeline"]
        assert channel.find("atom:link", {"atom": "http://www.w3.org/2005/Atom"}) is not None


class TestRobotsTxt:
    def test_allows_ai_crawlers_and_points_to_sitemap(self):
        content = build_robots_txt()
        assert "User-agent: GPTBot" in content
        assert "User-agent: ClaudeBot" in content
        assert "Sitemap: https://markus.wondrax.cloud/sitemap.xml" in content


class TestWriteArticleMarkdown:
    def test_copies_source_verbatim(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "article.md"
            source.write_text("---\ntitle: X\n---\n\nBody.\n", encoding="utf-8")
            output_dir = Path(tmp) / "articles"
            output_dir.mkdir()
            article = make_article(source=str(source))

            with patch("build_blog.OUTPUT_DIR", output_dir):
                write_article_markdown(article)

            dest = output_dir / "deterministic-pipelines.md"
            assert dest.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")

