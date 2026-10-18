# Specifications

This is the master specification for what the research site shows and how
its interactive parts behave. The build invariants in [AGENTS.md](../AGENTS.md)
(citations, grades, glossary, determinism, figure rules) apply throughout and
are not repeated here. Acceptance tests for each requirement are in
[acceptance-tests.md](acceptance-tests.md).

Requirement IDs are stable. A changed requirement keeps its ID; a removed one
is marked removed rather than renumbered.

## The organising idea

Every event on the site is one body cutting the light path from a source to
an observer. The light either travels straight to the observer (the Sun, a
star) or reflects off a body first (the Moon, a planet, a satellite). There
are three cases:

- **Darkened:** the body cuts the light reaching another body. That body goes
  dark for everyone who can see it, at one instant apart from light-time.
- **Hidden:** the body cuts the light reaching the observer. Something
  disappears for that observer, and the timing depends on where they stand.
- **Both:** the body cuts the observer's view of the light source itself. The
  observer stands in the body's shadow and sees the source hidden. Solar
  eclipses and transits are this case.

## PRI: the primer

- **PRI-1** The Primer's first page, "How eclipses, occultations and transits
  are computed", explains every event as a body cutting the light path, with
  the three cases above, in plain words before any formula.
- **PRI-2** It classifies every kind of event the research notes cover into
  one of the three cases, in one table, and links each row to the research
  group or topic that covers it.
- **PRI-3** It explains the shape of a shadow. An extended source gives a cone
  with an umbra, a penumbra and an antumbra, and an observer in each sees a
  total, partial or annular event. A transit is the annular case with a body
  too small to cover the source. A point source gives a cylinder with no
  penumbra.
- **PRI-4** It relates the Explanatory Supplement's terms (eclipse,
  occultation, transit, shadow transit) to the three cases, with the
  Supplement cited.
- **PRI-5** It ends by pointing to the worked example, the glossary, the
  research groups and the reports.
- **PRI-6** The solar walkthrough is titled "Worked example: a solar eclipse".
  It is the Primer's second page. It ends with a section that says, for a
  lunar eclipse, an occultation and a transit, which of its steps change and
  how, with links to the topics.

## FIG: 2D figures and animations

- **FIG-1** The general primer page has at least these figures:
  1. the light path, with the three places a body can cut it;
  2. the shape of the shadow: a cone with umbra, penumbra and antumbra, with
     what an observer in each sees, beside the cylinder of a point source;
  3. one gallery figure per case, with one small panel per kind of event.
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

## S3D: 3D guided scenes

Status: outline. This section is completed before the scenes are built.

- **S3D-1** One 3D viewer offers a scene for each case, chosen from chips.
- **S3D-2** The viewer's existing gates and controls apply unchanged.
- **S3D-3** Scenes take positions and shadows from the geometry module.

## SBX: the explorer

Status: outline. This section is completed before the explorer is built.

- **SBX-1** A Primer page, "Explorer", shows a side view of the light path
  and the observer's view, linked.
- **SBX-2** The reader picks the source (the Sun or a star), moves the bodies
  and the observer, and can play the motion.
- **SBX-3** Every control works by keyboard, and the page works at phone
  width.
- **SBX-4** Each primer section links to the explorer with its own preset.
