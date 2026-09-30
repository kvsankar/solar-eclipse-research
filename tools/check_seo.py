#!/usr/bin/env python3
"""Check actual built HTML titles, descriptions, canonicals and sitemap URLs."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

import build


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titles: list[str] = []
        self.descriptions: list[str] = []
        self.canonicals: list[str] = []
        self.social: dict[str, list[str]] = {}
        self.in_title = False
        self.in_head = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
            return
        if not self.in_head:
            return
        if tag == "title":
            self.in_title = True
            self.titles.append("")
        elif tag == "meta":
            name = attrs.get("property") or attrs.get("name")
            value = attrs.get("content", "")
            if name == "description":
                self.descriptions.append(value)
            elif name in {"og:title", "og:description", "og:url", "twitter:title", "twitter:description"}:
                self.social.setdefault(name, []).append(value)
        elif tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonicals.append(attrs.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
            self.in_title = False
        elif tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.titles[-1] += data


def check_site(out: Path = build.OUT) -> list[str]:
    errors: list[str] = []
    titles, descriptions, expected_urls = [], [], []
    nodes = list(build.walk(build.build_tree()))
    for node in nodes:
        rel = node.out_path.relative_to(build.OUT)
        path = out / rel
        if not path.is_file():
            errors.append(f"missing page: {rel}")
            continue
        meta = Metadata()
        meta.feed(path.read_text(encoding="utf-8"))
        expected_title = build.page_head_title(node)
        expected_url = build.public_url(node)
        expected_urls.append(expected_url)
        for label, actual, expected in (
            ("title", meta.titles, expected_title),
            ("description", meta.descriptions, node.description),
            ("canonical", meta.canonicals, expected_url),
            ("og:title", meta.social.get("og:title", []), expected_title),
            ("og:description", meta.social.get("og:description", []), node.description),
            ("og:url", meta.social.get("og:url", []), expected_url),
            ("twitter:title", meta.social.get("twitter:title", []), expected_title),
            ("twitter:description", meta.social.get("twitter:description", []), node.description),
        ):
            if not expected or actual != [expected]:
                errors.append(f"{rel}: missing, duplicate or incorrect {label}")
        titles.extend(meta.titles)
        descriptions.extend(meta.descriptions)

    if len(titles) != len(set(titles)):
        errors.append("duplicate document titles")
    if len(descriptions) != len(set(descriptions)):
        errors.append("duplicate descriptions")
    home = out / build.HOME_FILENAME
    index = out / "index.html"
    if not home.is_file() or not index.is_file() or home.read_bytes() != index.read_bytes():
        errors.append("publication home and offline index are missing or differ")
    try:
        sitemap = ET.parse(out / "sitemap.xml")
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = [element.text for element in sitemap.findall(f"{ns}url/{ns}loc")]
        if urls != sorted(expected_urls):
            errors.append("sitemap does not list exactly the canonical pages in sorted order")
    except (OSError, ET.ParseError) as exc:
        errors.append(f"invalid or missing sitemap: {exc}")
    return errors


def main() -> int:
    errors = check_site()
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("SEO checks passed: page-specific metadata, canonical URLs, home alias and sitemap.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
