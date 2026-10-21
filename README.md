# Computing Eclipses and Occultations

**[Read the research site](https://sankara.net/astro/eclipses/computing.html)**

![Totality: the solar corona around the black disc of the Moon, with pink prominences at the limb.](content/img/totality-1999-viatour.jpg)

<sub>Totality of 1999 August 11, from France. Luc Viatour /
[lucnix.be](https://lucnix.be), [CC BY-SA
3.0](https://creativecommons.org/licenses/by-sa/3.0/), via
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Solar_eclipse_1999_4.jpg).</sub>

Deep research into how eclipse, occultation and transit predictions are
computed, for developers who want to build or check such a calculator. Each
event is a body casting a shadow. When the observer stands in the shadow,
the source is hidden: a solar eclipse, a transit of Mercury or Venus, a lunar
occultation, or an occultation by a planet or minor body. When another body
stands in the shadow, that body goes dark: a lunar eclipse, or an eclipse of
a satellite of Jupiter or Saturn.

Solar eclipses are covered in most depth, from enumerating the eclipses in a
period to the contact times and Baily's beads at a single observer. The
other events are covered by what each one adds to the solar pipeline. The
research is cited source by source, with formulas, constants, datasets and
validation evidence.

The site is Markdown in `content/`, deterministically compiled to a
self-contained HTML tree in `site/`. It has no backend and needs no network
access at build time. The output opens directly from `file://`.

| Read | For |
|---|---|
| **[AGENTS.md](AGENTS.md)** | Conventions, invariants, the note shape, the research method. Start here. |
| This file | The machinery: build, front matter, citations, glossary, math. |
| `content/00-meta/` | The research plan and the source policy. |
| `content/20-reports/` | The synthesised reports: the solar eclipse pipeline, its error budget, and how to extend it to the other events. |

The build machinery is ported from `Essence-10/astrophotography-rental`
(itself from `kvsankar-private/finance-ai`) and keeps its conventions
identical, so anything learned in one repo transfers.

## Build

```
python tools/merge_refs.py         # content/**/refs.tsv -> references.tsv, terms.tsv -> glossary.tsv
python tools/build.py --clean      # content/ -> site/
python tools/build.py --serve      # build, then http://localhost:8000
python tools/check_notes.py        # raw notes against the shape AGENTS.md prescribes
python tools/extract_sections.py content/10-raw/<group>/<topic>   # summaries and recommendations of a topic
python tools/fix_math.py           # rewrite TeX that pandoc's math parser rejects (\rm, °, \cosec)
python tools/normalise_prose.py    # house-style spelling and notation, outside quotations and code
python tools/prose_check.py        # prose tics and long sentences
python tools/jargon_check.py       # terms used before they are explained
python tools/autolink.py           # first mentions that links.tsv would link (--apply adds them)
python tools/link_check.py         # relative links, anchors, hosts, link floors (--report, --online)
python -m unittest discover -s tools -p test_seo.py  # search metadata regression checks
python -m unittest discover -s tools -p 'test_*.py'  # numerical and source contracts
python tools/check_seo.py          # verify rendered metadata and sitemap
node --test tools/js/geometry.test.js tools/js/scenes.test.js   # geometry (spec GEO) and 3D scene states (S3D)
python tools/check_browser.py      # headless checks of figures and scenes (needs Playwright; about 5 minutes)
python tools/make_og_image.py      # recompose content/img/social-card-v4.jpg (needs Pillow)
```

Requires **pandoc** on PATH (3.x) and Python 3.10+. No pip or npm dependencies
for the build itself; `make_og_image.py` needs Pillow and is run by hand when
the card changes, not on every build.

## Search metadata and social previews

Every Markdown page carries a unique `seo_title` and `description`. The
search title also supplies the Open Graph and Twitter title. `title` remains
the visible heading and navigation label, so a descriptive search title does
not lengthen every navigation entry. The description also appears on the
parent page's card.

The home page's canonical URL is
`https://sankara.net/astro/eclipses/computing.html`. The build emits
`computing.html` alongside the identical offline entry `index.html`. Both
identify `computing.html` as canonical. All other pages retain their existing
URLs. Internal home links use the relative `computing.html` path, which also
works offline. The deterministic `sitemap.xml` lists each canonical page once and omits
the home-page aliases. It carries no modification dates because the content
dates are not a record of every page change.

After publishing, submit
`https://sankara.net/astro/eclipses/sitemap.xml` in Google Search Console
and request inspection of `computing.html`. Compare impressions, clicks and
positions for queries containing calculation, algorithm and computation.
The sitemap can also be listed in the domain's root `robots.txt`, which is
managed outside this repository.

Google recommends descriptive page titles and unique descriptions. Search
snippets can also come from visible text, so the introduction and links use
the same terminology. Google does not use a `meta keywords` tag for ranking.
See Google's [title guidance](https://developers.google.com/search/docs/appearance/title-link),
[description guidance](https://developers.google.com/search/docs/appearance/snippet),
[sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
and [supported meta tags](https://developers.google.com/search/docs/crawling-indexing/special-tags).

Every page carries Open Graph and Twitter card tags, so a shared link previews
as a card. These tags, canonical links and sitemap entries use absolute URLs.
`BASE_URL` in `tools/build.py` says where the tree is published. Navigation
uses relative links for offline reading. One image serves the whole site —
`content/img/social-card-v4.jpg`, composed by `tools/make_og_image.py` from the
totality photograph. The credit is drawn into the image because a card is
shown without the page around it, and the licence asks for the credit beside
the image.

## Deployment

The public source repository is
[`kvsankar/solar-eclipse-research`](https://github.com/kvsankar/solar-eclipse-research).
The manual **Deploy to Sankara.net** workflow builds the site and publishes the
owned subtree to:

```text
https://sankara.net/astro/eclipses/computing.html
```

The workflow copies the built home page to `computing.html` and deploys the
complete generated site so its relative links and assets remain available.
Deployment credentials live in the `sankara-net-production` GitHub environment.

`tools/deploy.py` performs the same deploy from an authorized workstation. It
mirrors the workflow step for step — same build, same payload checks, same
guarded remote path, same rsync flags, same post-deploy check — so a local run
and an Actions run put the same bytes in the same place.

To start the workflow from the command line, then watch the run it starts:

```bash
gh workflow run deploy-hetzner.yml --ref main
```

When GitHub Actions is degraded, queued runs later replay older commits in
order; the last queued run deploys the newest commit. Pages request assets by
`?v=<hash>` URLs because Cloudflare caches un-versioned ones, so check a live
asset by the versioned URL the page uses.

```bash
python tools/deploy.py --dry-run     # build, verify, show what would transfer
python tools/deploy.py --yes         # deploy, then check the live page
```

It holds no credentials. Host, user and key come from
`~/.config/sankara-net/env/main.env`, then the surface env, then `--ssh-alias`
(read with `ssh -G`, which resolves SSH config without connecting), then
explicit `--host/--user/--key`. Missing settings are reported by name.

## Layout

```
content/            source Markdown; the output tree mirrors this exactly
  _index.md         a directory's own page; becomes <dir>/index.html
  00-meta/          research plan, method and source policy
  05-primer/        background: how eclipses, occultations and transits are computed
  10-raw/           research notes, one folder per topic, grouped by kind of
                    event: shared foundations, solar eclipses and transits,
                    lunar eclipses, occultations, planetary satellites
  20-reports/       executive summary, pipeline design, error budget,
                    reading list and reference matrix, open questions,
                    extending the pipeline to other events
  img/              images belonging to the site rather than one topic
references.tsv      GENERATED bibliography, merged from content/**/refs.tsv
glossary.tsv        GENERATED glossary, merged from content/**/terms.tsv
images.tsv          GENERATED provenance, merged from content/**/images.tsv
templates/
  page.html         the HTML shell ({{placeholders}})
  pandoc-fragment.html   pandoc template: emits TOC + body around a split marker
  static/           site.css, site.js, site3d.js -> copied to site/assets/
  static/vendor/    three.min.js, fetched only when a reader opens a 3D view
tools/build.py      the whole build
tools/merge_refs.py fragment merger
site/               generated output (gitignored)
var/                downloaded PDFs, cloned repos, scratch (gitignored)
```

## Authoring conventions

Front matter is optional and flat:

```yaml
---
title: Page title              # else first H1, else filename
seo_title: Search title         # optional; also used for social cards
description: One line.         # shown on the parent index card
status: draft | working | final
updated: 2026-09-15
tags: [a, b]
order: 1                       # sort position within its directory
toc: true | false              # default: auto, on at 4+ headings
---
```

- Link between documents with **relative `.md` paths**; the build rewrites them
  to `.html`. Link to a section index as `../20-reports/_index.md`.
- A directory needs an `_index.md` to get a title and description.
- Numeric folder prefixes (`10-raw`) control ordering; `order:` overrides within
  a directory.
- Math: `$...$` inline, `$$...$$` display. Pandoc emits MathML, which renders
  natively in current browsers with no script. Escape a literal dollar as `\$`.
- A `::: summary` fenced div renders as the highlighted summary block.

## Figures

Figures we draw are Python scripts in `tools/figures/` that import
`figlib.py` and emit one SVG into `content/<topic>/img/`. The build **inlines**
our SVGs into the page, which is what makes them theme-aware: an SVG loaded
through `<img>` is a separate document and cannot see the page's custom
properties, so it would ignore the theme toggle. Inlined, `var(--fig-ink)`
resolves against the reader's chosen theme. The build also re-prefixes ids in
each inlined figure so two figures on one page cannot collide.

Every image under `content/` needs a provenance row or the build fails:

```
path <TAB> kind <TAB> licence <TAB> source <TAB> note <TAB> title
```

`kind` is `own` or `third-party`. An `own` figure names its generating script;
a third-party image names its licence and the page that states it. Rows live
in per-folder `images.tsv` fragments and are merged to the root `images.tsv`
by `tools/merge_refs.py`, so several people can add figures at once. An image
with no provenance is the same defect as an uncited claim.

The sixth column, `title`, is required (spec FIG-18): `merge_refs.py` and the
build refuse a picture without one. The zoom view shows it over the caption,
and every picture gets an anchor `#fig-<file stem>` carrying `data-figpath`
and `data-figtitle` (FIG-20). `content/00-meta/figure-index.md` holds a
`<!--FIGURES-->` marker that the build (`figure_index`,
`render_figure_index` in `tools/build.py`) fills with every picture on the
site, from the pages and `images.tsv` (FIG-16).

Captions state the finding, not the subject. A figure is either a schematic,
which says so on its face, or a data figure whose numbers already appear in
the corpus with a citation that the caption repeats.

### Progressive 3D figures

A figure may offer a three-dimensional view of the same subject:

```
![caption](img/besselian-xy.svg){.fig3d scene="fundamental-plane"}
```

The SVG remains the figure. `site3d.js` offers a **View in 3D** button only
when the runtime can actually deliver one, and stays silent otherwise. The
gates, in order: a WebGL context can be created; the reader has not asked for
reduced motion; the viewport is at least 480px; `Promise` exists; a scene of
that name is registered; and three.js loads. If the library fails to load,
which is normal offline or behind a content policy, the button removes itself
and the reader keeps the diagram. Nothing is ever replaced, so going back is
always possible.

Scenes live in the `SCENES` registry in `templates/static/site3d.js` and draw
in Earth equatorial radii, so a scene built from published Besselian elements
uses the numbers the tables print. The guided event scenes (spec S3D) keep
their state in `templates/static/scenes.js`, a pure module that computes each
event from `geometry.js` and is tested by `tools/js/scenes.test.js`;
`site3d.js` only draws what it returns. Scene colours are read from the same
`--fig-*` custom properties the SVGs use, so 3D follows the theme.

A scene returns **layers**, not a single blob. Each layer has an id, a label,
a group, an `explode` direction and an `order`:

```js
layer("plane", "Fundamental plane", 0, 0, -1.3, /* order */ 1);
```

The viewer builds a toggle chip per layer, so a reader can strip the figure
back to the parts they want. The **Take apart** slider slides each layer along
its own `explode` direction, staggered by `order`, so the assembly comes apart
in stages the way an exploded drawing takes apart an engine rather than
everything moving at once. **Animate** runs the slider, and **Reset** restores
both the camera and the layers.

Labels are attached to layers, so they travel with their part and hide when it
is switched off. They are also culled when the globe stands in front of them,
clamped to stay inside the frame, and placed in priority order with any that
would land on an already-placed label dropped, because a label covering the
drawing is worse than a label that is not there. Each sits on a short stem
above the point it names, so it never hides that point. A **Labels** chip
turns the lot off, and **Full screen** gives the scene the whole display,
where the extra room lets more labels survive the collision test.

**three.js is vendored**, not fetched from a CDN, because the site must open
from `file://` with no network. `templates/static/vendor/three.min.js` is
r149, the last UMD build, chosen because ES module scripts are blocked under
`file://`. It is MIT licensed; the licence travels with it as
`three.LICENSE.md`. It is 608 KB and is fetched only when a reader presses the
button, so it costs nothing to anyone who does not use it.

Every figure is also a lightbox trigger. `site.js` wraps each one in a button,
so it is reachable by keyboard, and opens a larger copy with pan, zoom and
reset: drag or arrow keys to pan, wheel, pinch, the buttons or `+`/`-` to
zoom, double-click or `0` to fit, `Esc` or the backdrop to close. Focus is
trapped while it is open and returns to the figure on close.

## Citations

Sources live in per-folder `refs.tsv` fragments, merged into `references.tsv`:

```
slug <TAB> grade <TAB> title <TAB> url <TAB> optional note
```

Grades: `primary`, `peer-reviewed`, `preprint`, `company`, `survey`, `trade`,
`vendor`, `unsourced`. Cite anywhere in Markdown with `[@slug]`. The build
numbers citations per page in order of first appearance, renders them as
superscript links colour-coded by grade, and appends a References section
listing only the sources that page actually cites. An unknown slug fails the
build.

**Grading in this project:**

- A refereed paper, the Explanatory Supplement, or an almanac office
  publication is `peer-reviewed`.
- NASA, USNO, IMCCE, JPL, IERS and PDS publications, data files and technical
  reports are `primary`.
- An arXiv preprint is `preprint`.
- A program author's own documentation of their own program (Occult, Solar
  Eclipse Maestro, Jubier's pages, timeanddate, SVS pages) is `company`.
- A GitHub repository is `company` when it documents its own method and
  `unsourced` when it is an undocumented reimplementation.
- Practitioner blog posts and mailing-list threads carrying data are `trade`;
  everything else informal is `unsourced`.

## Glossary explainers

Terms live in per-folder `terms.tsv` fragments, merged into `glossary.tsv`:

```
slug <TAB> label <TAB> definition <TAB> optional canonical url
```

The fourth column, when present, names the term's canonical page outside the
site, on a host in `CANONICAL_SITES` in `tools/build.py` (spec LNK-1, LNK-5).
The explainer panel and the A to Z listing end with "Read on Wikipedia" or the
site's own name, and the build refuses any other host.

Mark a term with `[?slug]`, or `[?slug|custom wording]`. The build renders an
inline term with a panel that opens on hover, tap, click or keyboard focus. A
page containing `<!--GLOSSARY-->` gets the full A to Z listing injected.

**Maths works in the TSVs.** A definition, and a reference title or note, may
use `$...$`, and the build renders it to MathML like any page body. All such
strings go through one batched pandoc call, cached by source string, so the
cost is a single extra invocation per build. Write formulas as LaTeX rather
than transliterating them: `$\zeta_1 = \sqrt{1 - \xi^2 - \eta_1^2}$`, never
`zeta1 = sqrt(1 - xi^2 - eta1^2)`. Keep glossary **labels** free of `$`,
because the A to Z listing sorts on the label and a leading `$` would sort it
under punctuation. Use Unicode there instead, as in `l₁ and l₂`.

## Links

Relative `.md` links are rewritten to `.html` by the build. First-mention
links are kept dense by `tools/autolink.py`, driven by `links.tsv` at the
root: one row per pattern, a Python regular expression matched on word
boundaries, and a target that is a page relative to `content/` or a canonical
URL. It links each target once per page at its first prose mention, never
inside headings, captions, quotations, code, maths, citations, glossary
markers or links, and never a page to itself. It reports by default and
writes only with `--apply`, so read its proposals before applying them.

The build opens every link that leaves the site in a new tab, adding
`target="_blank"` and `rel="noopener"` to each `<a>` with an `http` or
`https` address (spec LNK-8). Links within the site keep the reader's tab.

`tools/link_check.py` fails on a relative link to a missing file, an anchor
missing from the built page, an `http:` link, a research-note link to a host
outside `CANONICAL_SITES`, and a research note below the floors of five site
pages and three canonical pages. `tools/test_links.py` runs it, so CI does
too. `--online` fetches every external URL once and needs network access.

## Determinism

Same input bytes produce the same output bytes: no build timestamps, sorted
traversal, fixed pandoc flags.

## Licence

© 2026 Sankaranarayanan Viswanathan.

| Part | Licence |
|---|---|
| Text and the author's own figures (`content/`, the TSV ledgers, the rendered site) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), see [LICENSE-CONTENT](LICENSE-CONTENT) |
| Code (`tools/`, `templates/`) | [MIT](LICENSE) |
| Third-party images | Each keeps its own licence, recorded in its `images.tsv` row and credited beside the image |
| `templates/static/vendor/three.min.js` | MIT, in `three.LICENSE.md` beside it |

CC BY rather than CC BY-SA lets anyone reuse the work as long as they credit
it. A third-party image under CC BY-SA keeps that licence on its own row and
credit, so the rest of the corpus need not take it. A new third-party image
always needs its own `images.tsv` row.

To reuse the text or figures, credit "Sankaranarayanan Viswanathan,
Computing Eclipses and Occultations, https://sankara.net/astro/eclipses/computing.html, CC BY 4.0".
