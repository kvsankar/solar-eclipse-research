# Specifications

This is the master specification for what the research site shows and how
its interactive parts behave. The build invariants in [AGENTS.md](../AGENTS.md)
(citations, grades, glossary, determinism, figure rules) apply throughout and
are not repeated here. Acceptance tests for each requirement are in
[acceptance-tests.md](acceptance-tests.md).

Requirement IDs are stable. A changed requirement keeps its ID; a removed one
is marked removed rather than renumbered.

## The organising idea

Every event on the site is one body casting a shadow in some light. The
light is either emitted (the Sun, a star) or reflected (the Moon, a planet,
a satellite). There are two cases, set by who stands in the shadow:

- **Hidden:** the observer is in the shadow. The observer sees the source of
  that light hidden behind the blocking body, and the timing depends on
  where they stand. Solar eclipses, transits and every occultation are this
  case: a solar eclipse is the Moon hiding the Sun, seen from inside the
  Moon's shadow.
- **Darkened:** another body is in the shadow. The sunlight reaching it is
  cut off, so it goes dark for everyone who can see it, at one instant
  apart from light-time.

Within the hidden case, two properties of the hidden source set the
computation: whether it is a point (a star: a cylindrical shadow, so it
vanishes at once) or a disc (the Sun, a planet, a satellite: a cone with an
umbra, a penumbra and an antumbra), and whether it shines itself or is lit
by the Sun (then its phase shapes the hidden outline).

## PRI: the primer

- **PRI-1** The Primer's first page, "How eclipses, occultations and transits
  are computed", explains every event as a body casting a shadow, with the
  two cases above and the two properties of the hidden source, in plain
  words before any formula.
- **PRI-2** It classifies every kind of event the research notes cover into
  one of the two cases, in one table that also says whether the hidden or
  darkened source is a point or a disc, and links each row to the research
  group or topic that covers it.
- **PRI-3** It explains the shape of a shadow. An extended source gives a cone
  with an umbra, a penumbra and an antumbra, and an observer in each sees a
  total, partial or annular event. A transit is the annular case with a body
  too small to cover the source. A point source gives a cylinder with no
  penumbra.
- **PRI-4** It relates the Explanatory Supplement's terms (eclipse,
  occultation, transit, shadow transit) to the two cases, with the
  Supplement cited: its eclipse is the darkened case, its occultation and
  transit are the hidden case.
- **PRI-5** It ends by pointing to the worked example, the glossary, the
  research groups and the reports.
- **PRI-6** The solar walkthrough is titled "Worked example: a solar eclipse".
  It is the Primer's second page. It ends with a section that says, for a
  lunar eclipse, an occultation and a transit, which of its steps change and
  how, with links to the topics.

## FIG: 2D figures and animations

- **FIG-1** The general primer page has at least these figures:
  1. one diagram per case, each a separate figure at the head of its
     section, in which every body carries two labels: its role (light
     source, blocking body, darkened body, observer) and its name (the Sun,
     a star, the Moon, the Earth). The hidden case's diagram is a lunar
     occultation of a star; the darkened case's is a lunar eclipse;
  2. the shape of the shadow: a cone with umbra, penumbra and antumbra, with
     what an observer in each sees, beside the cylinder of a point source;
  3. further examples, each a separate diagram in the same style with the
     same two labels per body: a solar eclipse, a transit of Venus, a
     satellite hidden by its planet and a star hidden by an asteroid
     (hidden); the eclipse of a satellite and a shadow transit (darkened).
     Wherever an observer stands in a shadow, the observer's marker sits
     clearly inside the stated part of it, and an inset of what they see
     matches that part: a total eclipse in the umbra, a dot on the Sun in
     the antumbra.
- **FIG-2** Every primer figure says on its face that it is a schematic and
  not to scale. Its still frame carries its whole point with no interaction.
- **FIG-3** Three primer figures are animated: the Moon's shadow crossing the
  Earth, with one observer's view of the Sun; the Moon passing through the
  Earth's shadow; one orbit of Io showing its eclipse, occultation, transit
  and shadow transit.
- **FIG-4** An animated figure never moves by itself. It has a play and
  pause button that is reachable by keyboard and has an accessible name.
  When the reader has asked for reduced motion, there is no button and no
  motion. Without JavaScript the still frame is shown.
- **FIG-5** Pressing the play button does not open the figure lightbox.
  Opening the lightbox on an animated figure shows its still frame.
- **FIG-7** The Sun is drawn in one light, warm colour defined as a theme
  token, so it reads as bright in both themes. No figure draws the Sun in
  the dark accent colour. A body seen against the Sun is drawn as a dark
  silhouette, also a theme token, so it reads as dark in both themes.
- **FIG-6** The schematic figures are drawn at build time by scripts in
  `tools/figures/`. They illustrate the geometry and do not compute
  positions, so they do not use the geometry module.

## GEO: the geometry module

The 3D scenes and the sandbox compute positions, shadows and what the
observer sees. They share one module, so they cannot disagree.

- **GEO-1** Given the source's radius, the occulting body's radius and the
  distance between them, the module returns the radii of the umbra and the
  penumbra at any distance behind the occulting body. Beyond the umbra's
  vertex it returns the antumbra's radius as a positive number and says so.
- **GEO-2** Given a point's distance from the shadow axis and its distance
  behind the occulting body, the module says whether the point is in the
  umbra, the antumbra, the penumbra or outside the shadow.
- **GEO-3** Given the apparent radii of a source disc and an occulting disc
  and the separation of their centres, the module returns the observer's
  view: none, partial, total or annular. It also returns the fraction of
  the source disc's area that is covered.
- **GEO-4** For a point source, the module says whether the source is hidden:
  it is when the separation is less than the occulting disc's radius.
- **GEO-5** Given a relative position, a relative velocity and a limiting
  distance, the module returns the two contact times by the solution the
  corpus quotes from the 1961 Explanatory Supplement:
  $t = L\cos\psi/n - (uu' + vv')/n^2$, with $\sin\psi = (uv' - u'v)/(nL)$. It
  returns no contacts when the path misses.
- **GEO-6** The module has no dependency, touches no page, and loads both as
  a plain script from `file://` and as a module under Node, where its tests
  run.

## REP: the reports

- **REP-1** The executive summary opens with the shadow idea and gives
  one paragraph of findings for each case (hidden, darkened) before the
  solar eclipse findings. The solar findings follow under a heading
  that names solar eclipses.
- **REP-2** The pipeline report is titled "Solar eclipse pipeline" and the
  error budget "Solar eclipse error budget". Each says in its opening
  paragraph that it covers solar eclipses and links to the extension report.
- **REP-3** The cross-event report is titled "Extending the pipeline to
  other events" and comes straight after the solar eclipse pipeline. The
  order is: executive summary, solar eclipse pipeline, extension, error
  budget, reading list, open questions.
- **REP-4** The reading list and the open questions each have one section per
  research group: shared geometry and inputs, solar eclipses and transits,
  lunar eclipses, occultations, planetary satellites.

## HOME: the home page

- **HOME-1** The home page's main image is a collage with at least one
  photograph for each case, hidden and darkened, and a solar eclipse among
  the hidden ones. Every photograph is
  public domain or CC BY-SA, with its licence confirmed on the file's own
  page and recorded in `images.tsv`. The credits appear on the page under
  the collage.
- **HOME-2** The collage is built by a script from source images kept in
  the repository, so the same sources give the same bytes.
- **HOME-3** The home page's introduction starts with the shadow idea
  and says that solar eclipses are covered in most depth.
- **HOME-4** The home page's summary has one bullet per case and one on the
  depth of the solar eclipse material.
- **HOME-5** The home page's table of research notes is grouped by research
  group and links every topic.

## S3D: 3D guided scenes

Status: outline. This section is completed before the scenes are built.

- **S3D-1** One 3D viewer offers a scene for each case, chosen from chips.
- **S3D-2** The viewer's existing gates and controls apply unchanged.
- **S3D-3** Scenes take positions and shadows from the geometry module.

## SBX: the explorer

Status: outline. This section is completed before the explorer is built.

- **SBX-1** A Primer page, "Explorer", shows a side view of the bodies and their shadows
  and the observer's view, linked.
- **SBX-2** The reader picks the source (the Sun or a star), moves the bodies
  and the observer, and can play the motion.
- **SBX-3** Every control works by keyboard, and the page works at phone
  width.
- **SBX-4** Each primer section links to the explorer with its own preset.
