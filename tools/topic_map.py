"""The topic map (spec MAP): every topic on the site as a node, its place in
the contents tree as a radial mind map, and the cross-links between topics
as bundled curves.

The layout is computed here, at build time, so the map is plain inline SVG
that works with no script, opens from file:// and builds to the same bytes
every time. Every node is a link to its page. site.js adds one upgrade:
pointing at or focusing a node lights its links and dims the rest.

A topic is a directory that holds only pages, which the map draws as one
node, or a page that sits beside directories or in a section of pages, such
as a report. Directories above the topics are the inner rings. Links between
pages are counted from the Markdown, so a new link appears on the map at
the next build without any list to maintain.
"""

from __future__ import annotations

import html
import math
import os
import re
from pathlib import Path

MARKER = "<!--TOPICMAP-->"
LINK_RE = re.compile(r"\]\(([^)\s#]+?\.md)(?:#[^)\s]*)?\)")

# Geometry, in viewBox units. The leaves sit on the outer ring and their
# labels outside it, so the box leaves room for a label on either side.
R_LEAF = 300.0
LABEL_ROOM = 290.0
LABEL_CHARS = 26          # wrap a label longer than this onto two lines
BUNDLE = 0.7              # Holten's beta: 1 follows the tree, 0 is a straight line
BRANCH_GAP = 0.6          # the gap between branches, in leaf spacings
WEDGE = math.radians(20)  # no topic within this of straight up or down
ASPECT = 1.2              # the ring is this much taller than wide, for room between names
SHOW_FROM = 3             # without a choice, curves of fewer links are hidden
CROWDED = 40              # ... once the map has more curves than this


def n(x: float) -> str:
    """Round for output, so the bytes do not depend on float noise."""
    s = f"{x:.1f}"
    return "0.0" if s == "-0.0" else s


class Item:
    """A node of the map: the root, an inner section or a topic."""

    def __init__(self, node, parent: "Item | None"):
        self.node = node
        self.parent = parent
        self.children: list[Item] = []
        self.depth = 0 if parent is None else parent.depth + 1
        self.key = node.rel.as_posix() or "."
        self.angle = 0.0
        self.radius = 0.0
        self.weight = 0       # links to and from other topics

    @property
    def leaf(self) -> bool:
        return not self.children

    @property
    def xy(self) -> tuple[float, float]:
        return (self.radius * math.cos(self.angle), ASPECT * self.radius * math.sin(self.angle))

    def ancestors(self) -> list["Item"]:
        out, p = [], self.parent
        while p is not None:
            out.append(p)
            p = p.parent
        return out


def is_topic(node) -> bool:
    """A directory of pages at least two levels down. A first-level section
    of pages, such as the reports, shows each page instead."""
    return (node.is_dir and len(node.rel.parts) >= 2
            and not any(c.is_dir for c in node.children))


def build_items(root, skip) -> tuple[Item, list[Item], dict]:
    """The map's tree, its topics in reading order, and an index from every
    source file to the item that stands for it."""
    owner: dict[Path, Item] = {}
    leaves: list[Item] = []

    def add(node, parent: Item | None) -> Item | None:
        if node.src is not None and node.src.resolve() in skip:
            return None
        item = Item(node, parent)
        if node.src is not None:
            owner[node.src.resolve()] = item
        if parent is not None and is_topic(node):
            for c in walk_nodes(node):
                if c.src is not None:
                    owner[c.src.resolve()] = item
            leaves.append(item)
            return item
        for c in node.children:
            child = add(c, item)
            if child is not None:
                item.children.append(child)
        if parent is not None and not node.is_dir:
            leaves.append(item)
        if parent is not None and node.is_dir and not item.children:
            return None
        return item

    top = add(root, None)
    return top, leaves, owner


def walk_nodes(node):
    yield node
    for c in node.children:
        yield from walk_nodes(c)


def count_links(root, owner: dict) -> dict[tuple[str, str], int]:
    """Links between two different topics, in either direction, counted per
    link. A link to a section above the topics, or within a topic, is part of
    the tree, not a cross-link."""
    counts: dict[tuple[str, str], int] = {}
    for node in walk_nodes(root):
        if node.src is None or not node.body_md:
            continue
        a = owner.get(node.src.resolve())
        if a is None or not a.leaf:
            continue
        for m in LINK_RE.finditer(node.body_md):
            target = m.group(1)
            if re.match(r"^[a-z]+:", target):
                continue
            b = owner.get((node.src.parent / target).resolve())
            if b is None or not b.leaf or b is a:
                continue
            key = tuple(sorted((a.key, b.key)))
            counts[key] = counts.get(key, 0) + 1
    return counts


def layout(top: Item, leaves: list[Item]) -> None:
    """A radial cluster: topics evenly round the outer ring in reading order,
    with a gap between branches, and each inner section at the mean angle of
    its children on a ring set by its depth."""
    depth = max(l.depth for l in leaves)
    slots, prev = [], None
    for leaf in leaves:
        if prev is not None and leaf.parent is not prev.parent:
            slots.append(None)
        slots.append(leaf)
        prev = leaf
    span = sum(1 if s is not None else BRANCH_GAP for s in slots)
    # Two arcs, right and left, with an empty wedge at the top and the
    # bottom, where horizontal names would run into each other.
    arc = math.pi - 2 * WEDGE
    pos = 0.5
    for s in slots:
        if s is None:
            pos += BRANCH_GAP
            continue
        a = 2 * arc * pos / span
        s.angle = (-math.pi / 2 + WEDGE + a) if a < arc else (math.pi / 2 + WEDGE + a - arc)
        s.radius = R_LEAF
        pos += 1

    def place(item: Item) -> None:
        for c in item.children:
            place(c)
        if item.leaf:
            return
        item.angle = sum(c.angle for c in item.children) / len(item.children)
        item.radius = 0.0 if item.parent is None else R_LEAF * item.depth / (depth + 0.6)

    place(top)


def bspline_path(points: list[tuple[float, float]]) -> str:
    """A clamped uniform cubic B-spline through the control points, written
    as SVG Bezier segments."""
    pts = [points[0]] * 2 + points + [points[-1]] * 2
    x0, y0 = points[0]
    d = [f"M{n(x0)},{n(y0)}"]
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i:i + 4]
        c1 = ((2 * p1[0] + p2[0]) / 3, (2 * p1[1] + p2[1]) / 3)
        c2 = ((p1[0] + 2 * p2[0]) / 3, (p1[1] + 2 * p2[1]) / 3)
        e = ((p1[0] + 4 * p2[0] + p3[0]) / 6, (p1[1] + 4 * p2[1] + p3[1]) / 6)
        d.append(f"C{n(c1[0])},{n(c1[1])} {n(c2[0])},{n(c2[1])} {n(e[0])},{n(e[1])}")
    return "".join(d)


def bundled(a: Item, b: Item) -> str:
    """Hierarchical edge bundling (Holten 2006): the curve's control points
    are the tree path from one topic up to their nearest common section and
    down to the other, pulled towards the straight line by BUNDLE."""
    up = [a] + a.ancestors()
    down = [b] + b.ancestors()
    common = next(x for x in up if x in down)
    path = up[:up.index(common) + 1] + list(reversed(down[:down.index(common)]))
    raw = [p.xy for p in path]
    (x0, y0), (x1, y1) = raw[0], raw[-1]
    k = len(raw) - 1
    pts = [(BUNDLE * x + (1 - BUNDLE) * (x0 + (x1 - x0) * i / k),
            BUNDLE * y + (1 - BUNDLE) * (y0 + (y1 - y0) * i / k))
           for i, (x, y) in enumerate(raw)]
    return bspline_path(pts)


def wrap(text: str) -> list[str]:
    if len(text) <= LABEL_CHARS:
        return [text]
    words, line1 = text.split(), ""
    while words and len((line1 + " " + words[0]).strip()) <= LABEL_CHARS:
        line1 = (line1 + " " + words.pop(0)).strip()
    return [line1, " ".join(words)] if words else [line1]


LINE = 22.0               # label line height, in viewBox units


def leaf_radius(item: Item) -> float:
    return 3.5 + 1.1 * math.sqrt(item.weight)


def place_labels(leaves: list[Item]) -> dict[str, dict]:
    """Each topic's name beside its node, horizontal, on the outside of the
    ring. Near the top and the bottom the nodes sit close in height, so the
    names on each side are swept downwards until none overlaps the one above,
    and a moved name gets a thin leader to its node."""
    out = {}
    for right in (True, False):
        side = sorted((l for l in leaves if (math.cos(l.angle) >= -1e-9) == right),
                      key=lambda l: l.xy[1])
        prev_y, prev_h = None, 0.0
        for l in side:
            x, y = l.xy
            lines = wrap(l.node.title)
            h = LINE * len(lines)
            ly = y if prev_y is None else max(y, prev_y + (prev_h + h) / 2 + 3)
            # Clear of every node beside the name, not only its own.
            lx = x + (leaf_radius(l) + 6) * (1 if right else -1)
            for o in side:
                ox, oy = o.xy
                if abs(oy - ly) < h / 2 + leaf_radius(o):
                    edge = leaf_radius(o) + 6
                    lx = max(lx, ox + edge) if right else min(lx, ox - edge)
            out[l.key] = {"x": lx, "y": ly, "lines": lines,
                          "anchor": "start" if right else "end", "moved": abs(ly - y) > 2 or abs(abs(lx - x) - leaf_radius(l) - 6) > 2}
            prev_y, prev_h = ly, h
    return out


def node_id(item: Item) -> str:
    if item.parent is None:
        return "tm-home"
    return "tm-" + re.sub(r"[^a-z0-9]+", "-", item.key.lower()).strip("-")


def href(item: Item, here) -> str:
    return "../" * here.depth + item.node.url_from_root


def topic_map(root, here) -> dict:
    """The map's data: items, topics and weighted cross-links (spec MAP-2,
    MAP-3). Pages that carry the marker are left out, since a map of the map
    page leads nowhere."""
    skip = {n_.src.resolve() for n_ in walk_nodes(root)
            if n_.src is not None and MARKER in (n_.body_md or "")}
    top, leaves, owner = build_items(root, skip)
    edges = count_links(root, owner)
    by_key = {l.key: l for l in leaves}
    for (a, b), w in edges.items():
        by_key[a].weight += w
        by_key[b].weight += w
    layout(top, leaves)
    return {"top": top, "leaves": leaves, "edges": edges, "by_key": by_key}


def render_topic_map(root, here) -> str:
    """The inline SVG and its text equivalent, a table of every topic with
    its pages and the topics it links to."""
    data = topic_map(root, here)
    top, leaves, edges, by_key = data["top"], data["leaves"], data["edges"], data["by_key"]
    labels = place_labels(leaves)
    half = R_LEAF + LABEL_ROOM
    y_top = min(-ASPECT * R_LEAF, min(v["y"] - LINE * len(v["lines"]) / 2 for v in labels.values())) - 20
    y_end = max(ASPECT * R_LEAF, max(v["y"] + LINE * len(v["lines"]) / 2 for v in labels.values())) + 20
    vb = f"{n(-half)} {n(y_top)} {n(2 * half)} {n(y_end - y_top)}"
    top_w = max(edges.values(), default=1)
    start = min(SHOW_FROM, top_w) if len(edges) > CROWDED else 1
    out = ['<p class="tm-ctl" hidden><label for="tm-min">Show curves of at least</label> '
           f'<input type="range" id="tm-min" min="1" max="{min(top_w, 10)}" value="{start}"> '
           f'<output for="tm-min">{start}</output> links '
           '<span class="tm-hint">&middot; Click a topic to keep it lit, again to open it, '
           'Esc to clear</span></p>',
           f'<div class="topicmap"><svg class="tm" viewBox="{vb}" role="group" '
           'aria-labelledby="tm-title tm-desc" xmlns="http://www.w3.org/2000/svg">',
           '<title id="tm-title">Topic map</title>',
           '<desc id="tm-desc">Every topic on the site round a ring, grouped by section, '
           'with curves joining topics whose pages link to each other. A thicker '
           'curve carries more links. Each name is a link to its page.</desc>']

    # The tree: a thin spoke from each section to each child.
    out.append('<g class="tm-tree">')
    stack = [top]
    while stack:
        it = stack.pop()
        for c in it.children:
            (x0, y0), (x1, y1) = it.xy, c.xy
            out.append(f'<path d="M{n(x0)},{n(y0)}L{n(x1)},{n(y1)}"/>')
        stack.extend(reversed(it.children))
    out.append("</g>")

    # Cross-links, heaviest last so they draw on top.
    out.append('<g class="tm-links">')
    for (a, b), w in sorted(edges.items(), key=lambda e: (e[1], e[0])):
        ia, ib = by_key[a], by_key[b]
        width = 0.8 + 0.9 * math.log2(w)
        weak = ' class="tm-off"' if w < start else ""
        out.append(f'<path{weak} d="{bundled(ia, ib)}" data-ends="{node_id(ia)} {node_id(ib)}" '
                   f'data-w="{w}" style="stroke-width:{n(width)}"><title>'
                   f'{html.escape(ia.node.title)} and {html.escape(ib.node.title)}: '
                   f'{w} link{"s" if w != 1 else ""}</title></path>')
    out.append("</g>")

    # Nodes: sections inside, topics on the ring with their names outside.
    out.append('<g class="tm-nodes">')
    stack = [top]
    order = []
    while stack:
        it = stack.pop()
        order.append(it)
        stack.extend(reversed(it.children))
    for it in order:
        x, y = it.xy
        title = html.escape(it.node.title)
        desc = html.escape(it.node.description)
        cls = "tm-node tm-topic" if it.leaf else ("tm-node tm-root" if it.parent is None else "tm-node tm-section")
        out.append(f'<a class="{cls}" id="{node_id(it)}" href="{html.escape(href(it, here))}">'
                   f'<title>{title}{": " + desc if desc else ""}</title>')
        if it.leaf:
            r = leaf_radius(it)
            lab = labels[it.key]
            lx, ly, lines = lab["x"], lab["y"], lab["lines"]
            if lab["moved"]:
                end = lx - 3 if lab["anchor"] == "start" else lx + 3
                out.append(f'<path class="tm-leader" d="M{n(x)},{n(y)}L{n(end)},{n(ly)}"/>')
            out.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}"/>')
            dy0 = 6 - LINE / 2 * (len(lines) - 1)
            spans = "".join(f'<tspan x="{n(lx)}" dy="{n(dy0) if i == 0 else n(LINE)}">{html.escape(t)}</tspan>'
                            for i, t in enumerate(lines))
            out.append(f'<text x="{n(lx)}" y="{n(ly)}" text-anchor="{lab["anchor"]}">{spans}</text>')
        else:
            r = 9 if it.parent is None else 5.5
            out.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{r}"/>')
            label = html.escape(it.node.title if it.parent is not None else "Home")
            out.append(f'<text x="{n(x)}" y="{n(y - r - 5)}" text-anchor="middle">{label}</text>')
        out.append("</a>")
    out.append("</g></svg></div>")

    # The text equivalent: the same topics and links as a table.
    out.append('<table class="tm-table"><thead><tr><th>Topic</th><th>Pages</th>'
               '<th>Links to and from</th></tr></thead><tbody>')
    for it in leaves:
        pages = ([c for c in walk_nodes(it.node) if c is not it.node and c.src is not None]
                 if it.node.is_dir else [it.node])
        page_links = ", ".join(f'<a href="{html.escape("../" * here.depth + p.url_from_root)}">'
                               f'{html.escape(p.title)}</a>' for p in pages) or "&mdash;"
        near = sorted(((w, by_key[b if a == it.key else a]) for (a, b), w in edges.items()
                       if it.key in (a, b)), key=lambda t: (-t[0], t[1].key))
        near_links = ", ".join(f'<a href="#{node_id(o)}-row">'
                               f'{html.escape(o.node.title)}</a> ({w})' for w, o in near) or "&mdash;"
        section = it.parent.node.title if it.parent is not None and it.parent.parent is not None else ""
        out.append(f'<tr id="{node_id(it)}-row"><td><a href="{html.escape(href(it, here))}">'
                   f'{html.escape(it.node.title)}</a>'
                   + (f'<br><span class="tm-sec">{html.escape(section)}</span>' if section else "")
                   + f'</td><td>{page_links}</td><td>{near_links}</td></tr>')
    out.append("</tbody></table>")
    return "".join(out)
