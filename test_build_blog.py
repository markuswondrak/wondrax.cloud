#!/usr/bin/env python3
"""Tests for build_blog.py image handling."""

import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from build_blog import resolve_article_image


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
