# Working in this repo

Agent-facing guide. Read this before writing anything here.

## What this is

Deep research into **how solar eclipse computational products are computed**:
from enumerating the eclipses in a period, through global circumstances (paths,
limits, durations, timing), down to local circumstances at one observer (contact
times, magnitude, obscuration, Baily's beads). The target depth is Ernie
Wright's NASA SVS work on the 2024 eclipse: lunar limb profiles from LRO LOLA,
the solar radius question, Earth and Moon modelling, ephemerides, time scales.

The deliverable is a static research site, built from Markdown exactly the way
`Essence-10/astrophotography-rental` is built: pandoc, graded citations,
glossary explainers, deterministic output. The audience is a software
developer who wants to build or evaluate an eclipse-computation product and
needs to know which papers, formulas, datasets and repositories matter, and why.

## Layout

```
content/
  00-meta/      research plan, method and source policy
  05-primer/    background: what an eclipse computation pipeline is
  10-raw/       per-topic research notes, one folder per topic (the raw research)
  20-reports/   synthesis: the report, the pipeline design, the reference matrix
references.tsv  the bibliography: slug<TAB>grade<TAB>title<TAB>url<TAB>note
glossary.tsv    slug<TAB>label<TAB>definition
tools/build.py  the whole build; pandoc + a Python driver
templates/      HTML shell, pandoc fragment template, CSS/JS
site/           generated output, gitignored
var/            downloaded PDFs and scratch, gitignored
```

## Commands

```
python tools/build.py --clean     # content/ -> site/
python tools/build.py --serve     # build, then localhost:8000
python tools/prose_check.py       # flag prose tics and long sentences
python tools/jargon_check.py      # terms used before they are explained
python tools/merge_refs.py        # merge content/10-raw/*/refs.tsv into references.tsv
```

Requires pandoc 3.x on PATH and Python 3.10+. No pip dependencies.

## Invariants: do not break these

1. **Every substantive claim carries a citation.** `[@slug]` resolved from
   `references.tsv`. An unknown slug fails the build.
2. **Every source carries an evidence grade.** `primary`, `peer-reviewed`,
   `preprint`, `company`, `survey`, `trade`, `vendor`, `unsourced`.
   In this project: a refereed paper or an official almanac chapter is
   `peer-reviewed`; NASA, USNO, IMCCE, JPL and IERS publications and data are
   `primary`; an arXiv preprint is `preprint`; a software author's own
   documentation of their own program (Occult, Solar Eclipse Maestro, Jubier's
   pages, timeanddate) is `company`; a GitHub repository's README or code is
   `company` when it documents itself and `unsourced` when it is a third-party
   reimplementation with no documented validation; blog posts and forum threads
   are `unsourced` unless the author is a recognised practitioner writing about
   their own method, in which case `trade`.
3. **Jargon carries an explainer.** `[?slug]` or `[?slug|wording]` from
   `glossary.tsv`. Mark the first use on a page, not every use.
4. **The build is deterministic.** Same input bytes, same output bytes.
5. **The site states positions, not revisions.** Never narrate what a page used
   to say. Rewrite it.
6. **Formulas are quoted, not paraphrased, when they matter.** If a source gives
   the equation, reproduce it in `$...$` or `$$...$$` LaTeX (pandoc renders
   MathML) and say which symbols mean what. A developer must be able to
   implement from the note. State the constants a source uses (lunar radius
   ratio k, solar radius in km or arcseconds, Earth flattening, ΔT model).
7. **Distinguish the algorithm from the implementation.** Chauvenet's and
   Meeus's formulations are algorithms; Occult, SVS and Jubier are
   implementations that chose constants and data. Say which is which.

## Raw notes: the required shape

Each topic folder under `content/10-raw/` contains one or more `.md` notes, an
`_index.md`, a `refs.tsv` fragment and optionally a `terms.tsv` fragment. The
fragments are merged into the root TSVs by `tools/merge_refs.py`.

Front matter is flat YAML:

```yaml
---
title: Besselian elements
description: One sentence shown on the parent index card.
order: 1
status: working
updated: 2026-09-15
tags: [besselian, fundamental-plane]
---
```

Body structure, in this order:

1. A `::: summary` fenced div of 4 to 8 bullets a cold reader can understand.
   Bold the first few words of each bullet. This is the most-read part.
2. **The question** this note answers, in one paragraph.
3. The findings, under `##` headings. Quote formulas. Give constants. Name the
   dataset, its resolution, and where to download it. Name the paper, the year
   and what it actually showed, not what secondary coverage says it showed.
4. **Sources compared**: a table of the main sources with columns for what
   each one does that the others do not.
5. **What a developer should do**: the concrete recommendation, with the data
   files and the papers to read first.
6. **What this changes** for the overall pipeline design, explicitly saying
   "nothing" if that is the answer.
7. **Open questions**, each naming the artefact to obtain (a paper, a dataset,
   a line of code) rather than a topic to think about.

`refs.tsv` rows: `slug<TAB>grade<TAB>title<TAB>url<TAB>note`. Prefix every slug
with the topic's short prefix (given in your brief) so slugs never collide
across topics, for example `limb-watts-1963`. The note field says what the
source is good for and whether you read the artefact or only a summary of it.

`terms.tsv` rows: `slug<TAB>label<TAB>definition`. A definition may carry
`$...$` maths, which the build renders to MathML, so write a formula as LaTeX
rather than transliterating it into ASCII. Keep the label free of `$`, since
the A to Z listing sorts on it; use Unicode symbols there, as in `l₁ and l₂`. Propose the jargon a
developer new to eclipses would need: fundamental plane, gamma, umbral
magnitude, obscuration, k, ΔT, libration, Watts angle, and so on. Definitions
are one or two sentences, standalone.

## Figures

A figure we draw is a script in `tools/figures/` that imports `figlib.py` and
emits one SVG into `content/<topic>/img/`. The build inlines our SVGs, so they
follow the theme toggle; use the `figlib` classes and never a colour literal.
Read `tools/figures/fundamental_plane.py` as the worked example, and
[README.md](README.md) for the machinery.

1. **Every image needs a provenance row** in the topic's `images.tsv`, or the
   build fails. An image with no provenance is the same defect as an uncited
   claim. Third-party images must be public domain or openly licensed, with
   the licence confirmed on the file's own page and quoted in the row.
2. **A caption states the finding, not the subject.** It may carry maths and
   must carry the citation of any number it shows.
3. **A figure is a schematic or a data figure.** A schematic says so on its
   face. A data figure plots only numbers already in the corpus with a
   citation, or a curve computed from a formula the corpus quotes, and says
   which. Never fit a curve through points a source did not give.
4. **Colour never carries a distinction alone.** Add a shape, a dash pattern
   or a label, and check the figure in both themes.
5. **Deterministic**: round through `n()`, no timestamps, no randomness.
6. Give every figure a real `<title>` and `<desc>`; the `desc` describes the
   drawing rather than repeating the caption.
7. **3D is an upgrade, never the figure.** Mark an image
   `{.fig3d scene="name"}` and register a scene in `site3d.js` only where the
   subject is genuinely three-dimensional: the orientation of the fundamental
   plane, a cone meeting a sphere, the shape of the shadow on a globe. A chart
   is worse in 3D, not better. The SVG must carry the whole point on its own,
   because most readers will never press the button. See README.md for the
   runtime gates and the vendored library.

## Writing standards

- **Lead with the finding, then the evidence.** No throat-clearing.
- **One idea per sentence.** No em-dashes. No parentheticals longer than three
  words. No semicolons joining clauses.
- **British spelling, and one name per thing.** "catalogue", "centre",
  "metre", and "central line" rather than centreline. ΔT as the Unicode
  character in prose, headings and front matter, `\Delta T` only inside a
  larger formula. "arcseconds" spelled out in prose, ″ only in table
  numerals. Quotations keep their source's spelling, and
  `python tools/normalise_prose.py` enforces the rest while protecting
  quotations, code, URLs and math.
- **One symbol per quantity.** $s_0$ is the solar angular semidiameter at
  1 au and $R_\odot$ the linear radius; $S$ is the ellipsoid auxiliary and
  nothing else. $P$ is the position angle of a contact, $Q$ the shadow-edge
  angle in the limit condition, $C$ the angle from the contact point in
  Herald's limb construction. Write a program's own variables in code font,
  never as math, so they cannot be read as almanac symbols.
- **Name a product the same way every time**, expanding it once per page:
  "NASA's JavaScript Solar Eclipse Explorer (JSEX)" and "the SVS Eclipse
  Explorer web app (SVS 5169)" are different programs; "Kaguya (SELENE)";
  "The Photographer's Ephemeris (Photo Ephemeris)"; the Five Millennium
  Canon (NASA/TP-2006-214141) and the Five Millennium Catalogue
  (NASA/TP-2009-214174) with the report number on first use.
- **Never narrate the research process.** No "the brief", no "this session",
  no "search budget", no lists of queries, no tools and no account of how a
  page was fetched. The reader has none of those. A negative finding states
  its scope instead: what does not exist, and over what range that holds.
- **Name units every time.** Arcseconds versus kilometres versus lunar radii;
  UT versus TT versus TDB. Eclipse computation mixes them and errors hide in
  the mixing.
- **Date everything.** Ephemerides, ΔT predictions and limb datasets are
  versioned. Say which version a source used.
- **Record provenance.** If a fact is reported at second hand rather than
  taken from the document itself, say so in the text and in the reference
  note. Write it as evidence, "reported secondhand and unconfirmed", not as
  process, "found in a search summary".
- **Negative findings are findings.** "No open-source implementation of the
  limb-corrected path edge exists" is quotable, provided its scope is
  stated.
- **No commentary on the analysis itself.** Not "interestingly", not "it is
  worth noting", not "this is important".
- Link between notes with relative `.md` paths.

## Research method that works

- **Read the artefact, not the coverage.** Fetch the PDF. When `WebFetch`
  cannot parse a PDF it usually still saves it locally and prints the path.
  Extract it:
  ```
  pdftotext -layout <saved.pdf> out.txt
  ```
  `pdftotext` is on PATH. Put downloads in `var/` (gitignored).
- **Code is a primary source for what a program does.** When a repository is
  public, read the function that computes the quantity and cite the file.
- **Prefer the author's own description of their method** over a journalist's.
- **Search in several vocabularies.** "Besselian elements", "fundamental
  plane", "shadow cone", "umbral limit", "limb profile", "Baily's beads",
  "solar radius eclipse", "lunar limb LOLA eclipse", "Watts charts", "Kaguya
  LALT limb", "Δ T eclipse", "eclipse contact times algorithm".
- **Check arXiv, ADS, NASA SVS, NASA eclipse site (eclipse.gsfc.nasa.gov),
  IOTA, USNO/HMNAO, IMCCE, JPL, GitHub, Zenodo, the Journal of the BAA, the
  Journal for the History of Astronomy, Solar Physics, A&A, MNRAS, AJ, PASP,
  Icarus, Journal of Geodesy, Celestial Mechanics.**

## Things that cost time

- Heredocs through the Bash tool lose a level of backslash escaping and long
  ones get truncated. Write notes with the Write tool, and put any script
  longer than a couple of lines in a file before running it. This bites
  hardest where a backslash is data: a CSS rule written through a heredoc as
  `content: "\\2190"` arrives as `\2190`, which Python then reads as the
  octal escape `\21` followed by `90`, and a stray control byte lands in the
  stylesheet. Prefer literal characters, with `@charset "utf-8";` at the top
  of the CSS, over numeric escapes.
- `[@slug]` and `[?slug]` in prose examples must sit inside code spans or the
  build resolves them.
- pandoc math: use `$...$` for inline and `$$...$$` for display. Escape a
  literal dollar sign as `\$`.
- pandoc's math parser rejects `\rm`, a literal degree sign and `\cosec`,
  and silently falls back to raw TeX in a `<span class="math">`. Write
  `\mathrm{}`, `^{\circ}` and `\csc`. `python tools/fix_math.py` rewrites
  them, and a build is clean only when
  `grep -rl 'class="math' site` returns nothing.
