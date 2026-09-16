#!/usr/bin/env python3
"""
Deterministic Markdown -> static HTML tree builder for the solar-eclipse computation research site.

    python tools/build.py            # build content/ -> site/
    python tools/build.py --clean    # wipe site/ first
    python tools/build.py --serve    # build, then serve site/ on :8000

Design rules:
  * Output mirrors the content/ tree one-for-one. content/a/b.md -> site/a/b.html
  * A directory becomes site/<dir>/index.html, seeded from its _index.md if present.
  * Every link is relative, so the tree opens directly from file:// with no server.
  * No timestamps or randomness in output: same input bytes -> same output bytes.
  * Markdown -> HTML conversion is delegated to pandoc; this script only assembles
    chrome (nav, breadcrumbs, TOC, child listings) around pandoc's fragment.

Front matter (optional, YAML-ish, flat) understood per file:
    title:       page title           (else first H1, else filename)
    description: one-line summary     (shown on parent index cards)
    status:      draft | working | final
    tags:        [a, b] or block list
    order:       integer, sorts within its directory
    toc:         true | false         (default: auto -- on if >=4 headings)
    sources:     block list of URLs   (rendered as a Sources section)
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "site"
TEMPLATES = ROOT / "templates"
STATIC = TEMPLATES / "static"

SITE_TITLE = "Computing Solar Eclipses — Research"

# Open Graph needs absolute URLs, which a relative-link static site otherwise
# never forms. This is where the built tree is published; a build served from
# anywhere else still works, and only its social previews point here.
BASE_URL = "https://sankara.net/astro/solar-eclipses/"
SOCIAL_IMAGE = "img/social-card.jpg"
SOCIAL_IMAGE_ALT = (
    "Totality: the solar corona around the black disc of the Moon, with pink "
    "prominences at the limb."
)
SOURCE_NOTE = (
    "Built from Markdown in <code>content/</code> by <code>tools/build.py</code>. "
    "Edit the Markdown, not this page."
)

PANDOC_FROM = (
    "markdown"
    "+yaml_metadata_block"
    "+pipe_tables"
    "+footnotes"
    "+definition_lists"
    "+task_lists"
    "+strikeout"
    "+backtick_code_blocks"
    "+fenced_code_attributes"
    "+fenced_divs"
    "+auto_identifiers"
    "+tex_math_dollars"
    "+link_attributes"
    "-smart"
)

COPY_AS_IS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf", ".csv", ".json", ".txt"}

REFS_FILE = ROOT / "references.tsv"


# --------------------------------------------------------------------------- #
# references / citations
# --------------------------------------------------------------------------- #

class Ref:
    __slots__ = ("slug", "grade", "title", "url", "note")

    def __init__(self, slug, grade, title, url, note=""):
        self.slug, self.grade, self.title, self.url, self.note = slug, grade, title, url, note


# Data-file faults that must fail the build rather than warn: a duplicate slug
# silently renders the wrong source sitewide, which is as corrupting as an unknown one.
DATA_ERRORS: list[str] = []

ALLOWED_GRADES = {
    "primary", "peer-reviewed", "preprint", "company",
    "survey", "trade", "vendor", "unsourced",
}


def load_refs() -> dict[str, Ref]:
    """Load the shared bibliography: slug<TAB>grade<TAB>title<TAB>url[<TAB>note]."""
    refs: dict[str, Ref] = {}
    if not REFS_FILE.exists():
        return refs
    for lineno, raw in enumerate(REFS_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # Split positionally. Dropping empty fields first would let a stray double
        # tab shift the title into the url column with no visible symptom.
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) < 4 or not all(parts[:4]):
            DATA_ERRORS.append(
                f"references.tsv line {lineno}: expected 4 non-empty tab-separated fields")
            continue
        slug, grade, title, url = parts[0], parts[1], parts[2], parts[3]
        note = parts[4] if len(parts) > 4 else ""
        if slug in refs:
            DATA_ERRORS.append(f"references.tsv line {lineno}: duplicate slug '{slug}'")
        if grade.lower() not in ALLOWED_GRADES:
            DATA_ERRORS.append(
                f"references.tsv line {lineno}: unknown evidence grade '{grade}' for '{slug}'")
        refs[slug] = Ref(slug, grade, title, url, note)
    return refs


# Fenced blocks and inline code spans, so markup examples in documentation survive.
CODE_RE = re.compile(r"(```.*?```|~~~.*?~~~|`[^`]*?`)", re.S)


def apply_outside_code(md: str, fn):
    """Run fn over the parts of md that are not code, leaving code spans untouched."""
    return "".join(
        part if i % 2 else fn(part)
        for i, part in enumerate(CODE_RE.split(md))
    )


GLOSSARY_FILE = ROOT / "glossary.tsv"


def load_glossary() -> dict[str, tuple[str, str]]:
    """slug -> (label, definition), from glossary.tsv."""
    terms: dict[str, tuple[str, str]] = {}
    if not GLOSSARY_FILE.exists():
        return terms
    for lineno, raw in enumerate(GLOSSARY_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) < 3 or not all(parts[:3]):
            DATA_ERRORS.append(
                f"glossary.tsv line {lineno}: expected 3 non-empty tab-separated fields")
            continue
        if parts[0] in terms:
            DATA_ERRORS.append(f"glossary.tsv line {lineno}: duplicate slug '{parts[0]}'")
        terms[parts[0]] = (parts[1], parts[2])
    return terms


# --------------------------------------------------------------------------- #
# inline markup for TSV-sourced text
# --------------------------------------------------------------------------- #

# Glossary definitions and reference titles are data, not page bodies, so they
# never pass through the page renderer. Without help they would be inserted as
# escaped plain text and any `$...$` in them would show as literal TeX. These
# strings are short and numerous, so they are rendered in one batched pandoc
# call and cached by source string.

INLINE_CACHE: dict[str, str] = {}
_SENTINEL = "zzinlinesplitzz"


def render_inline_batch(strings) -> None:
    """Render every unique string to inline HTML with one pandoc invocation."""
    todo = sorted({s.strip() for s in strings if s and s.strip()
                   and s.strip() not in INLINE_CACHE})
    if not todo:
        return
    doc = ("\n\n" + _SENTINEL + "\n\n").join(todo)
    cmd = [
        "pandoc",
        f"--from={PANDOC_FROM}",
        "--to=html5",
        "--mathml",
        "--wrap=preserve",
        "--email-obfuscation=none",
    ]
    proc = subprocess.run(cmd, input=doc, capture_output=True, text=True,
                          encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"pandoc failed on inline batch:\n{proc.stderr}")
    parts = proc.stdout.split(f"<p>{_SENTINEL}</p>")
    if len(parts) != len(todo):
        raise RuntimeError(
            f"inline batch split {len(parts)} chunks for {len(todo)} strings")
    for src, chunk in zip(todo, parts):
        html_text = chunk.strip()
        # Unwrap the single paragraph pandoc puts around each string, so the
        # result can sit inside a <span> or a <dd>.
        if (html_text.startswith("<p>") and html_text.endswith("</p>")
                and "<p>" not in html_text[3:]):
            html_text = html_text[3:-4]
        # Raw inline HTML must not carry blank lines when it is fed back
        # through the Markdown reader.
        INLINE_CACHE[src] = " ".join(html_text.split())


def inline(text: str) -> str:
    """Rendered HTML for a TSV string, falling back to plain escaping."""
    if not text:
        return ""
    return INLINE_CACHE.get(text.strip(), html.escape(text))


# [?slug] or [?slug|display wording]
GLOSS_RE = re.compile(r"\[\?([A-Za-z0-9][A-Za-z0-9._-]*)(?:\|([^\]]+))?\]")


def resolve_glossary(md: str, terms: dict, missing: set, used: set) -> str:
    """Replace [?slug] with an inline term carrying a hover/focus explainer panel."""
    def repl(m):
        slug, override = m.group(1), m.group(2)
        entry = terms.get(slug)
        if entry is None:
            missing.add(slug)
            return f'<span class="gloss gloss-missing">{html.escape(override or slug)}</span>'
        label, definition = entry
        used.add(slug)
        text = override if override else label
        return (
            f'<span class="gloss" tabindex="0" role="button" aria-describedby="g-{slug}">'
            f'<span class="gloss-t">{html.escape(text)}</span>'
            f'<span class="gloss-pop" id="g-{slug}" role="tooltip">'
            f'<span class="gloss-h">{inline(label)}</span>'
            f'<span class="gloss-d">{inline(definition)}</span>'
            f"</span></span>"
        )

    return apply_outside_code(md, lambda s: GLOSS_RE.sub(repl, s))


def render_glossary_list(terms: dict) -> str:
    """Full A-Z listing, injected wherever a page contains <!--GLOSSARY-->."""
    if not terms:
        return ""
    rows = sorted(terms.items(), key=lambda kv: kv[1][0].lower())
    out = ['<dl class="glossary-list">']
    for slug, (label, definition) in rows:
        out.append(
            f'<dt id="term-{slug}">{inline(label)}</dt>'
            f"<dd>{inline(definition)}</dd>"
        )
    out.append("</dl>")
    return "".join(out)


CITE_RE = re.compile(r"\[@([A-Za-z0-9][A-Za-z0-9._-]*)\]")

GRADE_CLASS = {
    "primary": "g-primary",
    "peer-reviewed": "g-peer",
    "preprint": "g-peer",
    "company": "g-company",
    "survey": "g-survey",
    "trade": "g-trade",
    "vendor": "g-vendor",
    "unsourced": "g-unsourced",
}


def resolve_citations(md: str, refs: dict[str, Ref], missing: set) -> tuple[str, list[Ref]]:
    """Replace [@slug] with numbered superscript links; return the page's cited list."""
    order: list[str] = []

    def repl(m):
        slug = m.group(1)
        ref = refs.get(slug)
        if ref is None:
            missing.add(slug)
            return f'<sup class="cite cite-missing" title="unknown reference: {html.escape(slug)}">[?]</sup>'
        if slug not in order:
            order.append(slug)
        n = order.index(slug) + 1
        cls = GRADE_CLASS.get(ref.grade.lower(), "g-other")
        tip = f"{ref.grade}: {ref.title}"
        return (
            f'<sup class="cite {cls}"><a href="#ref-{n}" '
            f'title="{html.escape(tip)}">{n}</a></sup>'
        )

    out = apply_outside_code(md, lambda s: CITE_RE.sub(repl, s))
    return out, [refs[s] for s in order]


def render_reference_list(cited: list[Ref]) -> str:
    if not cited:
        return ""
    items = []
    for i, r in enumerate(cited, 1):
        cls = GRADE_CLASS.get(r.grade.lower(), "g-other")
        note = f' <span class="refnote">{inline(r.note)}</span>' if r.note else ""
        link = (
            f'<a href="{html.escape(r.url)}" rel="noreferrer">{inline(r.title)}</a>'
            if r.url and r.url != "-"
            else inline(r.title)
        )
        items.append(
            f'<li id="ref-{i}"><span class="refnum">{i}</span>'
            f'<span class="grade {cls}">{html.escape(r.grade)}</span> {link}{note}</li>'
        )
    return (
        '<section class="references"><h2 id="references">References</h2>'
        '<ol class="reflist">' + "".join(items) + "</ol></section>"
    )


# --------------------------------------------------------------------------- #
# figures
# --------------------------------------------------------------------------- #

IMAGES_FILE = ROOT / "images.tsv"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def load_images() -> dict[str, list[str]]:
    """Provenance for every image under content/: path, kind, licence, source, note.

    An image with no provenance is the same defect as an uncited claim, so the
    build refuses to publish one.
    """
    rows: dict[str, list[str]] = {}
    if not IMAGES_FILE.exists():
        return rows
    for lineno, raw in enumerate(IMAGES_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [c.strip() for c in line.split("\t")]
        if len(parts) < 4 or not all(parts[:4]):
            DATA_ERRORS.append(
                f"images.tsv line {lineno}: expected 4 non-empty tab-separated fields")
            continue
        if parts[0] in rows:
            DATA_ERRORS.append(f"images.tsv line {lineno}: duplicate path '{parts[0]}'")
        rows[parts[0]] = parts
    return rows


def check_images(images: dict[str, list[str]]) -> int:
    """Every image on disk must be declared, and every declaration must exist."""
    on_disk = {
        q.relative_to(CONTENT).as_posix()
        for q in CONTENT.rglob("*")
        if q.is_file() and q.suffix.lower() in IMAGE_SUFFIXES
    }
    for path in sorted(on_disk - set(images)):
        DATA_ERRORS.append(f"image '{path}' has no row in content/images.tsv")
    for path in sorted(set(images) - on_disk):
        DATA_ERRORS.append(f"images.tsv lists '{path}', which does not exist")
    return len(on_disk)


MATH_BLOCK_RE = re.compile(r'<math display="block".*?</math>', re.S)


def wrap_display_math(body: str) -> str:
    """Put each display equation in its own scrollable box.

    `overflow-x` set on a <math> element is not honoured reliably, so a long
    equation escapes its column and runs under whatever sits beside it. A
    plain div around it scrolls predictably.
    """
    return MATH_BLOCK_RE.sub(
        lambda m: '<div class="mathblock">' + m.group(0) + "</div>", body)


IMG_RE = re.compile(r'<img src="([^"]+\.svg)"([^>]*?)/?>')
ID_RE = re.compile(r'id="([A-Za-z_][\w.-]*)"')
URL_RE = re.compile(r"url\(#([A-Za-z_][\w.-]*)\)")
SVG_OPEN_RE = re.compile(r"<svg\b")


def inline_svgs(body: str, node: "Node") -> str:
    """Replace <img src="*.svg"> with the file's markup.

    Inlining is what makes a figure theme-aware: the site has a manual theme
    toggle, and an SVG loaded through <img> is an independent document that
    cannot see the page's custom properties. Inlined, `var(--fig-ink)`
    resolves against whatever theme the reader has chosen.
    """
    base = node.src.parent if node.src else (CONTENT / node.rel)

    def repl(m: re.Match) -> str:
        src, attrs = m.group(1), m.group(2)
        if re.match(r"^(https?:|/)", src):
            return m.group(0)
        target = (base / src).resolve()
        if not target.exists() or not target.is_file():
            return m.group(0)
        markup = target.read_text(encoding="utf-8").strip()
        if not markup.startswith("<svg"):
            return m.group(0)
        # Scope ids so two figures on one page cannot collide.
        prefix = re.sub(r"[^a-z0-9]+", "-", target.stem.lower()).strip("-") + "-"
        markup = ID_RE.sub(lambda k: f'id="{prefix}{k.group(1)}"', markup)
        markup = URL_RE.sub(lambda k: f"url(#{prefix}{k.group(1)})", markup)
        # Carry the alt text through as the accessible name.
        alt = re.search(r'alt="([^"]*)"', attrs)
        if alt and alt.group(1):
            # A function replacement, not a string: a caption may contain a
            # backslash (LaTeX in a caption is normal here), and re.sub would
            # read it as an escape in a replacement template.
            label = f'<svg aria-label="{html.escape(alt.group(1), quote=True)}"'
            markup = SVG_OPEN_RE.sub(lambda _m: label, markup, count=1)

        # An image marked {.fig3d scene="name"} keeps its SVG as the figure a
        # reader always gets. The wrapper carries the scene name so the script
        # can offer a 3D view, but only where the runtime supports one.
        cls = re.search(r'class="([^"]*)"', attrs)
        scene = re.search(r'data-scene="([^"]*)"', attrs)
        if cls and "fig3d" in cls.group(1).split() and scene:
            return (
                f'<div class="fig3d-host" data-scene="'
                f'{html.escape(scene.group(1), quote=True)}">{markup}</div>'
            )
        return markup

    return IMG_RE.sub(repl, body)


# --------------------------------------------------------------------------- #
# front matter
# --------------------------------------------------------------------------- #

def split_front_matter(text: str) -> tuple[dict, str]:
    """Return (meta, body). Only a leading '---' block is treated as front matter."""
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            return parse_flat_yaml(lines[1:i]), "\n".join(lines[i + 1:]).lstrip("\n")
    return {}, text


def parse_flat_yaml(lines: list[str]) -> dict:
    """Tiny YAML subset: flat scalars, inline lists, and '- ' block lists."""
    meta: dict = {}
    key: str | None = None
    for raw in lines:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- ") and key is not None:
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(unquote(stripped[2:].strip()))
            continue
        m = re.match(r"^([A-Za-z_][\w.-]*)\s*:\s*(.*)$", stripped)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            meta[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [unquote(p.strip()) for p in inner.split(",") if p.strip()]
        else:
            meta[key] = unquote(value)
    return meta


def unquote(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


# --------------------------------------------------------------------------- #
# node tree
# --------------------------------------------------------------------------- #

class Node:
    """A page in the output tree (a Markdown file, or a directory index)."""

    def __init__(self, src: Path | None, rel: Path, is_dir: bool):
        self.src = src                  # source .md (None for a dir with no _index.md)
        self.rel = rel                  # path relative to content/, without extension
        self.is_dir = is_dir
        self.meta: dict = {}
        self.body_md: str = ""
        self.children: list[Node] = []
        self.parent: Node | None = None
        self.title: str = ""
        self.load()

    def load(self) -> None:
        if self.src and self.src.exists():
            text = self.src.read_text(encoding="utf-8")
            self.meta, self.body_md = split_front_matter(text)
        self.title = str(self.meta.get("title") or "").strip() or self.derive_title()

    def derive_title(self) -> str:
        m = re.search(r"^#\s+(.+)$", self.body_md, re.M)
        if m:
            return m.group(1).strip()
        name = self.rel.name or "Home"
        name = re.sub(r"^\d+[-_]", "", name)
        return name.replace("-", " ").replace("_", " ").strip().capitalize() or "Home"

    @property
    def out_path(self) -> Path:
        return OUT / (self.rel / "index.html" if self.is_dir else self.rel.with_suffix(".html"))

    @property
    def url_from_root(self) -> str:
        rel = self.rel.as_posix()
        if self.is_dir:
            return "index.html" if rel in ("", ".") else f"{rel}/index.html"
        return f"{rel}.html"

    @property
    def depth(self) -> int:
        """Directory depth of the output file, for building '../' prefixes."""
        n = len(self.rel.parts)
        return n if self.is_dir else max(0, n - 1)

    @property
    def description(self) -> str:
        return str(self.meta.get("description") or "").strip()

    def sort_key(self):
        order = self.meta.get("order")
        try:
            o = int(str(order))
        except (TypeError, ValueError):
            o = 500
        # directories before files at equal order, then by path
        return (o, 0 if self.is_dir else 1, self.rel.as_posix())


def sort_key_for_missing(path: Path):
    return (500, 0, path.as_posix())


def build_tree() -> Node:
    root = Node(src=index_src(CONTENT), rel=Path(""), is_dir=True)
    if not root.meta.get("title"):
        root.title = SITE_TITLE
    attach(root, CONTENT)
    return root


def index_src(directory: Path) -> Path | None:
    p = directory / "_index.md"
    return p if p.exists() else None


def is_section(directory: Path) -> bool:
    """A directory is a section only if it holds prose.

    Asset directories — img/, data/ — contain no .md at any depth. Treating them
    as sections built an empty page titled "Img" at every img/ URL, complete with
    breadcrumbs and no content. Their files are still copied through by the
    asset pass; they just do not get an index page of their own.
    """
    return any(directory.rglob("*.md"))


def attach(node: Node, directory: Path) -> None:
    for child_dir in sorted(p for p in directory.iterdir() if p.is_dir()):
        if child_dir.name.startswith("."):
            continue
        if not is_section(child_dir):
            continue
        rel = child_dir.relative_to(CONTENT)
        child = Node(src=index_src(child_dir), rel=rel, is_dir=True)
        child.parent = node
        node.children.append(child)
        attach(child, child_dir)

    for md in sorted(p for p in directory.glob("*.md")):
        if md.name == "_index.md" or md.name.startswith("."):
            continue
        rel = md.relative_to(CONTENT).with_suffix("")
        child = Node(src=md, rel=rel, is_dir=False)
        child.parent = node
        node.children.append(child)

    node.children.sort(key=Node.sort_key)


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #

def pandoc_render(md: str, want_toc: bool) -> tuple[str, str]:
    """Return (toc_html, body_html) for a Markdown body."""
    if not md.strip():
        return "", ""
    cmd = [
        "pandoc",
        f"--from={PANDOC_FROM}",
        "--to=html5",
        "--template", str(TEMPLATES / "pandoc-fragment.html"),
        "--wrap=preserve",
        "--email-obfuscation=none",
        "--mathml",
    ]
    if want_toc:
        cmd += ["--toc", "--toc-depth=3"]
    proc = subprocess.run(cmd, input=md, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"pandoc failed:\n{proc.stderr}")
    parts = proc.stdout.split("<!--PANDOC-SPLIT-->", 1)
    toc = parts[0].strip() if len(parts) == 2 else ""
    body = (parts[1] if len(parts) == 2 else proc.stdout).strip()
    if toc:
        # A custom pandoc template yields the bare <ul>; supply our own wrapper.
        toc = f'<nav class="toc" role="doc-toc">{toc}</nav>'
    return toc, body


HEADING_RE = re.compile(r"^#{2,3}\s+\S", re.M)


def wants_toc(node: Node) -> bool:
    flag = str(node.meta.get("toc", "")).strip().lower()
    if flag in ("true", "yes", "1"):
        return True
    if flag in ("false", "no", "0"):
        return False
    return len(HEADING_RE.findall(node.body_md)) >= 4


def strip_leading_h1(md: str, title: str) -> str:
    """The template prints the title, so drop a duplicate leading H1."""
    m = re.match(r"^\s*#\s+(.+?)\s*$", md, re.M)
    if m and m.start() == 0:
        if m.group(1).strip().lower() == title.strip().lower():
            return md[m.end():].lstrip("\n")
    return md


LINK_RE = re.compile(r'(href=")([^"]+)(")')


def rewrite_links(html_text: str) -> str:
    """Point relative *.md links at their generated *.html counterparts."""
    def repl(m):
        pre, url, post = m.groups()
        if re.match(r"^(https?:|mailto:|tel:|#|/)", url):
            return m.group(0)
        target, _, frag = url.partition("#")
        if target.endswith("_index.md"):
            target = target[: -len("_index.md")] + "index.html"
        elif target.endswith(".md"):
            target = target[:-3] + ".html"
        else:
            return m.group(0)
        return f"{pre}{target}{'#' + frag if frag else ''}{post}"

    return LINK_RE.sub(repl, html_text)


def rel_root(depth: int) -> str:
    return "../" * depth if depth else ""


def render_nav(root: Node, current: Node) -> str:
    prefix = rel_root(current.depth)

    def render(nodes: list[Node], level: int) -> str:
        if not nodes:
            return ""
        out = ["  " * level + "<ul>"]
        for n in nodes:
            cls = []
            if n is current:
                cls.append("current")
            li_cls = ' class="sec"' if n.is_dir and level == 0 else ""
            a_cls = f' class="{" ".join(cls)}"' if cls else ""
            out.append(
                "  " * level
                + f'<li{li_cls}><a{a_cls} href="{prefix}{n.url_from_root}">{html.escape(n.title)}</a>'
            )
            if n.children:
                out.append(render(n.children, level + 1))
            out.append("  " * level + "</li>")
        out.append("  " * level + "</ul>")
        return "\n".join(out)

    home_cls = ' class="current"' if current is root else ""
    home = f'<ul><li class="sec"><a{home_cls} href="{prefix}index.html">Home</a></li></ul>'
    return home + "\n" + render(root.children, 0)


def ancestry(node: Node) -> list[Node]:
    """The node's chain from the root down to itself."""
    chain: list[Node] = []
    cur: Node | None = node
    while cur is not None:
        chain.append(cur)
        cur = cur.parent
    chain.reverse()
    return chain


def render_crumbs(node: Node, root: Node) -> str:
    """Breadcrumb trail, rendered on every page so the header keeps one rhythm.

    The last item is the current page: it is not a link and carries
    aria-current, so a screen reader announces position rather than offering a
    link to the page already open.
    """
    chain = ancestry(node)
    prefix = rel_root(node.depth)
    items = []
    for n in chain[:-1]:
        label = html.escape("Home" if n is root else n.title)
        items.append(f'<li><a href="{prefix}{n.url_from_root}">{label}</a></li>')
    here = html.escape("Home" if node is root else node.title)
    items.append(f'<li><span aria-current="page">{here}</span></li>')
    return '<ol class="crumblist">' + "".join(items) + "</ol>"


def render_prevnext(node: Node, prev: Node | None, nxt: Node | None,
                    position: int, total: int) -> str:
    """Previous and next in the site's single linear reading order.

    The order is the depth-first walk that also builds the navigation, so
    "next" always means the next page down the sidebar.
    """
    prefix = rel_root(node.depth)

    def side(target: Node | None, cls: str, label: str) -> str:
        if target is None:
            return f'<span class="pn-link pn-{cls} pn-empty"></span>'
        section = ""
        if target.parent is not None and target.parent.title and target.parent.parent is not None:
            section = f'<span class="pn-sec">{html.escape(target.parent.title)}</span>'
        return (
            f'<a class="pn-link pn-{cls}" href="{prefix}{target.url_from_root}">'
            f'<span class="pn-label">{label}</span>'
            f'{section}'
            f'<span class="pn-title">{html.escape(target.title)}</span></a>'
        )

    counter = f'<span class="pn-count">{position} of {total}</span>'
    return (
        '<nav class="prevnext" aria-label="Previous and next page">'
        + side(prev, "prev", "Previous") + counter + side(nxt, "next", "Next")
        + "</nav>"
    )


def render_meta_block(node: Node) -> str:
    bits = []
    status = str(node.meta.get("status") or "").strip()
    if status:
        cls = f"status-{html.escape(status.lower())}"
        bits.append(f'<span class="{cls}">{html.escape(status)}</span>')
    updated = str(node.meta.get("updated") or "").strip()
    if updated:
        bits.append(f"<span>updated {html.escape(updated)}</span>")
    tags = node.meta.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    for t in tags:
        bits.append(f'<span class="tag">{html.escape(str(t))}</span>')
    if not bits:
        return ""
    return '<div class="metablock">' + "".join(bits) + "</div>"


def render_children(node: Node) -> str:
    if not node.children:
        return ""
    prefix = rel_root(node.depth)
    cards = []
    for c in node.children:
        desc = f'<span class="cd">{html.escape(c.description)}</span>' if c.description else ""
        sub = ""
        if c.is_dir and c.children:
            sub = f'<span class="cmeta">{len(c.children)} page{"s" if len(c.children) != 1 else ""}</span>'
        elif not c.is_dir:
            st = str(c.meta.get("status") or "").strip()
            if st:
                sub = f'<span class="cmeta">{html.escape(st)}</span>'
        cards.append(
            f'<a class="card" href="{prefix}{c.url_from_root}">'
            f'<span class="ct">{html.escape(c.title)}</span>{desc}{sub}</a>'
        )
    return (
        '<section class="children"><h2>In this section</h2>'
        '<div class="cards">' + "".join(cards) + "</div></section>"
    )


def render_sources(node: Node) -> str:
    srcs = node.meta.get("sources") or []
    if isinstance(srcs, str):
        srcs = [srcs]
    if not srcs:
        return ""
    items = []
    for s in srcs:
        s = str(s).strip()
        m = re.match(r"^\[(.+?)\]\((\S+)\)$", s)
        if m:
            label, url = m.group(1), m.group(2)
        else:
            label, url = s, s
        items.append(f'<li><a href="{html.escape(url)}" rel="noreferrer">{html.escape(label)}</a></li>')
    return "<h2 id=\"sources\">Sources</h2><ol>" + "".join(items) + "</ol>"


def fill(template: str, values: dict) -> str:
    def repl(m):
        return values.get(m.group(1), "")
    return re.sub(r"\{\{(\w+)\}\}", repl, template)


def render_social(node: Node) -> str:
    """Open Graph and Twitter tags, so a shared link previews as a card.

    The card is the same for every page: one image for the site, with the page
    title and description beside it. A per-page image would mean a card for
    each of 56 pages and no more information than this carries.
    """
    url = BASE_URL + ("" if node.parent is None else node.url_from_root)
    title = SITE_TITLE if node.parent is None else f"{node.title} · {SITE_TITLE}"
    description = node.description or SITE_TITLE
    tags = [
        ("og:type", "article" if node.parent is not None else "website"),
        ("og:site_name", SITE_TITLE),
        ("og:title", title),
        ("og:description", description),
        ("og:url", url),
        ("og:image", BASE_URL + SOCIAL_IMAGE),
        ("og:image:width", "1200"),
        ("og:image:height", "630"),
        ("og:image:alt", SOCIAL_IMAGE_ALT),
    ]
    out = [f'<meta property="{k}" content="{html.escape(v)}">' for k, v in tags]
    out.append('<meta name="twitter:card" content="summary_large_image">')
    out.append(f'<link rel="canonical" href="{html.escape(url)}">')
    return "\n".join(out)


def render_page(node: Node, root: Node, template: str, refs: dict, missing: set,
                terms: dict, gloss_missing: set, gloss_used: set,
                prev: Node | None = None, nxt: Node | None = None,
                position: int = 1, total: int = 1,
                records: list | None = None) -> str:
    md = strip_leading_h1(node.body_md, node.title)
    md = resolve_glossary(md, terms, gloss_missing, gloss_used)
    md, cited = resolve_citations(md, refs, missing)
    toc, body = pandoc_render(md, wants_toc(node))
    body = rewrite_links(body)
    body = wrap_display_math(body)
    body = inline_svgs(body, node)
    if "<!--GLOSSARY-->" in body:
        body = body.replace("<!--GLOSSARY-->", render_glossary_list(terms))
    if records is not None:
        collect_search(node, body, records)
    body = body + render_sources(node) + render_reference_list(cited)
    values = {
        "title": html.escape(node.title),
        "site_title": html.escape(SITE_TITLE),
        # The home page's own title is the site title, so pairing the two in
        # the document title says the same thing twice in the browser tab.
        "head_title": html.escape(SITE_TITLE) if node.parent is None
        else html.escape(node.title) + " &middot; " + html.escape(SITE_TITLE),
        "description": html.escape(node.description or SITE_TITLE),
        "root": rel_root(node.depth),
        "nav": render_nav(root, node),
        "crumbs": render_crumbs(node, root),
        "meta_block": render_meta_block(node),
        # The page ToC rides in a sticky rail beside the prose. A page without
        # headings gets no rail and no reserved column.
        "toc": toc,
        "toc_rail": f'<aside class="toc-rail">{toc}</aside>' if toc else "",
        "colwrap_class": "colwrap has-toc" if toc else "colwrap",
        "social": render_social(node),
        "body": body,
        "children": render_children(node) if node.is_dir else "",
        "prevnext": render_prevnext(node, prev, nxt, position, total),
        "source_note": SOURCE_NOTE,
    }
    return fill(template, values)



# --------------------------------------------------------------------------- #
# search index
# --------------------------------------------------------------------------- #

# A static site has no server to ask, and this one has to open from file://,
# where fetch() of a local file is refused. So the index ships as a script that
# assigns a global, loaded only when a reader first opens the search box, the
# same arrangement the 3D viewer uses for its library.

# Dropped from the index. Short, uninformative, and between them they account
# for a large share of the postings.
STOPWORDS = frozenset("""
a an the and or but if then than that this these those of in on at to for from
by with without into onto over under again further is are was were be been
being do does did doing have has had having it its as so such no nor not only
own same too very can will just should now which who whom what when where why
how all any both each few more most other some there here he she they them his
her their you your we our i me my one two also use used using between
""".split())

TAG_RE = re.compile(r"<[^>]+>")
ANNOTATION_RE = re.compile(r"<annotation\b.*?</annotation>", re.S)
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.S)
SCRIPT_RE = re.compile(r"<(script|style)\b.*?</\1>", re.S)
# A glossary term renders as the visible word plus a tooltip carrying the whole
# definition. Indexing both puts the definition into every excerpt that uses
# the term, so the tooltip goes and the word stays.
GLOSSPOP_RE = re.compile(
    r'<span class="gloss"[^>]*><span class="gloss-t">(.*?)</span>'
    r'.*?</span></span></span>', re.S)
# Citation markers are superscript numbers. In running text they read as
# stray digits, so they are dropped from the index and from the excerpt.
CITEMARK_RE = re.compile(r'<sup class="cite\b.*?</sup>', re.S)
HEAD_SPLIT_RE = re.compile(
    r'<h([23])\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h\1>', re.S)
WORD_RE = re.compile(r"\w+", re.UNICODE)


def plain_text(fragment: str) -> str:
    """Readable text from a rendered fragment.

    Tags become spaces rather than nothing: closing one tag and opening the
    next must not weld two words into one. MathML carries both rendered glyphs
    and its LaTeX source, so the annotation goes first or every formula is
    indexed twice, once as mathematics and once as backslashes.
    """
    t = ANNOTATION_RE.sub(" ", fragment)
    t = SCRIPT_RE.sub(" ", t)
    t = SVG_RE.sub(" ", t)
    t = CITEMARK_RE.sub("", t)
    t = GLOSSPOP_RE.sub(lambda m: m.group(1), t)
    t = TAG_RE.sub(" ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def tokens(text: str) -> list[str]:
    out = []
    for w in WORD_RE.findall(text.lower()):
        if len(w) > 1 and w not in STOPWORDS:
            out.append(w)
    return out


def collect_search(node: "Node", body: str, records: list) -> None:
    """One record per section, so a hit lands on the passage, not the page.

    The page's own lead is a record too, anchored at the top, so a page whose
    first words answer the query is not represented only by its subsections.
    """
    url = node.out_path.relative_to(OUT).as_posix()
    title = node.title

    heads = list(HEAD_SPLIT_RE.finditer(body))
    # The lead runs from the top of the page to the first heading; each
    # heading then owns everything up to the next one.
    spans = [(0, heads[0].start() if heads else len(body), None, None)]
    for i, m in enumerate(heads):
        stop = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        spans.append((m.end(), stop, m.group(2), plain_text(m.group(3))))

    for start, stop, anchor, head in spans:
        text = plain_text(body[start:stop])
        if not text and not head:
            continue
        # The page title and the heading say what the passage is about, so they
        # weigh more than a word buried in it. Repeating them folds the boost
        # into the term counts and needs no second structure.
        weighted = " ".join([title] * 4 + [head or ""] * 3 + [text])
        counts: dict[str, int] = {}
        for w in tokens(weighted):
            counts[w] = counts.get(w, 0) + 1
        if not counts:
            continue
        excerpt = text[:190].rstrip()
        if len(text) > 190:
            excerpt = excerpt.rsplit(" ", 1)[0] + "\u2026"
        records.append({
            "u": url, "p": title, "h": head or "", "a": anchor or "",
            "x": excerpt, "c": counts,
            # Length, so that ranking can normalise by it. The glossary listing
            # is one very long section; without this it outranks the prose for
            # every term it happens to define.
            "n": sum(counts.values()),
        })


def b36(n: int) -> str:
    if n == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while n:
        n, r = divmod(n, 36)
        out = digits[r] + out
    return out


def write_search_index(records: list) -> int:
    """Emit the index as a script assigning one global.

    Postings are base-36 gaps between record numbers, with the count appended
    only when it is not one, which it usually is. The saving over a JSON array
    of integers is about half the file.
    """
    terms: dict[str, list[tuple[int, int]]] = {}
    for i, rec in enumerate(records):
        for w, c in rec["c"].items():
            terms.setdefault(w, []).append((i, c))

    packed = {}
    for w in sorted(terms):
        posts, prev, out = terms[w], 0, []
        for i, c in posts:
            gap = b36(i - prev)
            prev = i
            out.append(gap if c == 1 else gap + "." + b36(c))
        packed[w] = " ".join(out)

    slim = [{k: r[k] for k in ("u", "p", "h", "a", "x", "n")} for r in records]
    avg = sum(r["n"] for r in records) / max(1, len(records))
    payload = {"r": slim, "t": packed, "avg": round(avg, 1)}
    text = ("/* Generated by tools/build.py. One global, no fetch, so the site\n"
            "   searches itself when opened from file://. */\n"
            "window.__SEARCH__ = "
            + json.dumps(payload, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"))
            + ";\n")
    dst = OUT / "assets" / "search-index.js"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8", newline="\n")
    return len(text.encode("utf-8"))

# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #

def walk(node: Node):
    yield node
    for c in node.children:
        yield from walk(c)


def copy_assets() -> int:
    n = 0
    for src in sorted(STATIC.rglob("*")):
        if src.is_file():
            dst = OUT / "assets" / src.relative_to(STATIC)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            n += 1
    for src in sorted(CONTENT.rglob("*")):
        if src.is_file() and src.suffix.lower() in COPY_AS_IS:
            dst = OUT / src.relative_to(CONTENT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the eclipse-computation research site.")
    ap.add_argument("--clean", action="store_true", help="remove site/ before building")
    ap.add_argument("--serve", action="store_true", help="serve site/ on :8000 after building")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if shutil.which("pandoc") is None:
        print("error: pandoc not found on PATH", file=sys.stderr)
        return 2
    if not CONTENT.exists():
        print(f"error: no content directory at {CONTENT}", file=sys.stderr)
        return 2

    if args.clean and OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    template = (TEMPLATES / "page.html").read_text(encoding="utf-8")
    root = build_tree()
    refs = load_refs()
    terms = load_glossary()
    images = load_images()
    n_images = check_images(images)
    render_inline_batch(
        [t for pair in terms.values() for t in pair]
        + [r.title for r in refs.values()]
        + [r.note for r in refs.values()]
    )
    missing: set = set()
    used: set = set()
    gloss_missing: set = set()
    gloss_used: set = set()

    pages = 0
    citations = 0
    search: list[dict] = []
    order = list(walk(root))
    total = len(order)
    for i, node in enumerate(order):
        before = len(CITE_RE.findall(node.body_md))
        citations += before
        used.update(CITE_RE.findall(node.body_md))
        out_html = render_page(node, root, template, refs, missing, terms,
                               gloss_missing, gloss_used,
                               prev=order[i - 1] if i > 0 else None,
                               nxt=order[i + 1] if i + 1 < total else None,
                               position=i + 1, total=total, records=search)
        node.out_path.parent.mkdir(parents=True, exist_ok=True)
        node.out_path.write_text(out_html, encoding="utf-8", newline="\n")
        pages += 1

    assets = copy_assets()
    index_bytes = write_search_index(search)
    if not args.quiet:
        print(f"built {pages} pages, {assets} assets -> {OUT}")
        print(f"search index: {len(search)} sections, "
              f"{index_bytes / 1024:.0f} KB")
        print(f"{citations} citations across {len(refs)} references in the bibliography")
        print(f"{len(gloss_used)} of {len(terms)} glossary terms used")
        own = sum(1 for r in images.values() if r[1] == "own")
        print(f"{n_images} figures ({own} drawn here, {n_images - own} third-party)")
        print(f"open: {OUT / 'index.html'}")

    if missing:
        print(f"ERROR: {len(missing)} unknown citation slug(s): "
              f"{', '.join(sorted(missing))}", file=sys.stderr)
    if gloss_missing:
        print(f"ERROR: {len(gloss_missing)} unknown glossary slug(s): "
              f"{', '.join(sorted(gloss_missing))}", file=sys.stderr)
    unused = sorted(set(refs) - used)
    if unused and not args.quiet:
        print(f"note: {len(unused)} reference(s) defined but never cited: "
              f"{', '.join(unused)}", file=sys.stderr)
    gloss_unused = sorted(set(terms) - gloss_used)
    if gloss_unused and not args.quiet:
        print(f"note: {len(gloss_unused)} glossary term(s) defined but never used: "
              f"{', '.join(gloss_unused)}", file=sys.stderr)
    for problem in DATA_ERRORS:
        print(f"ERROR: {problem}", file=sys.stderr)
    if missing or gloss_missing or DATA_ERRORS:
        return 1

    if args.serve:
        import http.server
        import functools
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("serving http://localhost:8000  (ctrl-c to stop)")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8000), handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
