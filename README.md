# eclipse-research: computing solar eclipse products

![Totality: the solar corona around the black disc of the Moon, with pink prominences at the limb.](content/img/totality-1999-viatour.jpg)

<sub>Totality of 1999 August 11, from France. Luc Viatour /
[lucnix.be](https://lucnix.be), [CC BY-SA
3.0](https://creativecommons.org/licenses/by-sa/3.0/), via
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Solar_eclipse_1999_4.jpg).</sub>

Deep research into how solar eclipse computational products are computed,
from enumerating the eclipses in a period to the contact times and Baily's
beads at a single observer. Markdown in `content/`, deterministically
compiled to a self-contained HTML tree in `site/`. No backend, no build-time
network access; the output opens directly from `file://`.

| Read | For |
|---|---|
| **[AGENTS.md](AGENTS.md)** | Conventions, invariants, the note shape, the research method. Start here. |
| This file | The machinery: build, front matter, citations, glossary, math. |
| `content/00-meta/` | The research plan and the source policy. |
| `content/20-reports/` | The synthesised report. |

The build machinery is ported from `Essence-10/astrophotography-rental`
(itself from `kvsankar-private/finance-ai`) and keeps its conventions
identical, so anything learned in one repo transfers.

## Build

```
python tools/merge_refs.py         # content/**/refs.tsv -> references.tsv, terms.tsv -> glossary.tsv
python tools/build.py --clean      # content/ -> site/
python tools/build.py --serve      # build, then http://localhost:8000
python tools/check_notes.py        # raw notes against the shape AGENTS.md prescribes
python tools/extract_sections.py content/10-raw/<topic>   # summaries and recommendations of a topic
python tools/fix_math.py           # rewrite TeX that pandoc's math parser rejects (\rm, °, \cosec)
python tools/normalise_prose.py    # house-style spelling and notation, outside quotations and code
python tools/prose_check.py        # prose tics and long sentences
python tools/jargon_check.py       # terms used before they are explained
python tools/make_og_image.py      # recompose content/img/social-card-v2.jpg (needs Pillow)
```

Requires **pandoc** on PATH (3.x) and Python 3.10+. No pip or npm dependencies
for the build itself; `make_og_image.py` needs Pillow and is run by hand when
the card changes, not on every build.

## Social previews

Every page carries Open Graph and Twitter card tags, so a shared link previews
as a card. They are the one part of the output that cannot be relative:
`BASE_URL` in `tools/build.py` says where the tree is published, and only the
previews depend on it. One image serves the whole site —
`content/img/social-card-v2.jpg`, composed by `tools/make_og_image.py` from the
totality photograph. The credit is drawn into the image because a card is
shown without the page around it, and the licence asks for the credit beside
the image.

## Deployment

The public source repository is
[`kvsankar/solar-eclipse-research`](https://github.com/kvsankar/solar-eclipse-research).
The manual **Deploy to Sankara.net** workflow builds the site and publishes the
owned subtree to:

```text
https://sankara.net/astro/solar-eclipses/computing.html
```

The workflow copies the built home page to `computing.html` and deploys the
complete generated site so its relative links and assets remain available.
Deployment credentials live in the `sankara-net-production` GitHub environment.

`tools/deploy.py` performs the same deploy from an authorized workstation. It
mirrors the workflow step for step — same build, same payload checks, same
guarded remote path, same rsync flags, same post-deploy check — so a local run
and an Actions run put the same bytes in the same place.

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
  05-primer/        background: the eclipse computation pipeline for newcomers
  10-raw/           per-topic research notes, one folder per topic
  20-reports/       the synthesised report and the reference matrix
references.tsv      GENERATED bibliography, merged from content/**/refs.tsv
glossary.tsv        GENERATED glossary, merged from content/**/terms.tsv
templates/
  page.html         the HTML shell ({{placeholders}})
  pandoc-fragment.html   pandoc template: emits TOC + body around a split marker
  static/           site.css, site.js -> copied to site/assets/
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
path <TAB> kind <TAB> licence <TAB> source <TAB> note
```

`kind` is `own` or `third-party`. An `own` figure names its generating script;
a third-party image names its licence and the page that states it. Rows live
in per-folder `images.tsv` fragments and are merged to the root `images.tsv`
by `tools/merge_refs.py`, so several people can add figures at once. An image
with no provenance is the same defect as an uncited claim.

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
uses the numbers the tables print. Scene colours are read from the same
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
slug <TAB> label <TAB> definition
```

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

## Determinism

Same input bytes produce the same output bytes: no build timestamps, sorted
traversal, fixed pandoc flags.
