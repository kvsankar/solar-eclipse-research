"""URL names of the content folders (docs/specs.md URL-1 to URL-3).

A folder under content/ appears in URLs under the name url-names.tsv
gives it, or else under its own name without a leading two-digit prefix. The
prefix only identifies a topic; the reader never sees it. File names do not
change.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import posixpath
import re

PREFIX_RE = re.compile(r"^\d{2}-")
# Links that leave the site's relative tree: a scheme, a fragment, an
# absolute path or a protocol-relative URL.
EXTERNAL_RE = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#|/)")


class UrlNames:
    def __init__(self, dirs: set[str], names: dict[str, str]):
        self.dirs = set(dirs)
        unknown = sorted(set(names) - self.dirs)
        if unknown:
            raise ValueError(f"url-names.tsv names folders that do not exist: {unknown}")
        self.map: dict[str, str] = {}
        for d in sorted(self.dirs, key=lambda p: p.count("/")):
            parent, _, name = d.rpartition("/")
            own = names.get(d) or PREFIX_RE.sub("", name)
            self.map[d] = (self.map[parent] + "/" + own) if parent else own
        seen: dict[str, str] = {}
        for d, url in self.map.items():
            if url in seen:
                raise ValueError(f"folders {seen[url]} and {d} both have the URL {url}/")
            seen[url] = d
            if url in self.dirs and url != d:
                raise ValueError(f"the URL {url}/ of {d} is also a source folder")

    def url(self, rel: str) -> str:
        """The URL path of a file or page given by its source path."""
        parts = PurePosixPath(rel).parts
        for i in range(len(parts) - 1, 0, -1):
            folder = "/".join(parts[:i])
            if folder in self.map:
                return "/".join((self.map[folder],) + parts[i:])
        return rel

    def link(self, href: str, page: str) -> str:
        """A relative link written in the source page `page` (its source path
        without extension), pointed at its target's URL."""
        if not href or EXTERNAL_RE.match(href):
            return href
        target, hash_, frag = href.partition("#")
        target, q, query = target.partition("?")
        if not target:
            return href
        src_dir = posixpath.dirname(page)
        resolved = posixpath.normpath(posixpath.join(src_dir, target))
        if resolved.startswith(".."):
            return href
        url_dir = posixpath.dirname(self.url(page + ".html"))
        new = posixpath.relpath(self.url(resolved), url_dir or ".")
        if target.endswith("/") and not new.endswith("/"):
            new += "/"
        return new + (q + query if q else "") + (hash_ + frag if hash_ else "")


def read_names(path: Path) -> dict[str, str]:
    names: dict[str, str] = {}
    if not path.exists():
        return names
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        folder, url = (c.strip() for c in line.split("\t")[:2])
        if folder == "folder":
            continue
        names[folder] = url
    return names


def load(content: Path, names_file: Path) -> UrlNames:
    dirs = {p.relative_to(content).as_posix() for p in content.rglob("*")
            if p.is_dir() and not p.name.startswith(".")}
    return UrlNames(dirs, read_names(names_file))
