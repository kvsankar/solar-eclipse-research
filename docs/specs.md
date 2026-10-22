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
- **PRI-7** The same section explains the site's name. The site uses the
  Supplement's two broad terms: an eclipse is the darkened case, and an
  occultation is the hidden case. A transit is an occultation in which the
  nearer body looks smaller than the source. The section also says that the
  Supplement's own section heading names all three: eclipses, occultations
  and transits.
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
     clearly inside the stated part of it, and the picture of what they
     see matches that part: a total eclipse in the umbra, a dot on the Sun
     in the antumbra.
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
- **FIG-10** Totality is drawn as the dark disc with a faint, diffuse
  corona that fades outwards, in a theme token colour. No bright ring of
  the Sun is drawn around the disc at totality, because a ring reads as an
  annular eclipse. This holds in the 2D figures and in the 3D view panel.
- **FIG-11** No observer floats in space. In every 2D figure an observer's
  marker sits on a drawn world: on its edge, or inside its disc where the
  world is seen face-on. Two kinds of figure have no marker: one whose
  observer is off the drawing and shown by a direction arrow, such as the
  Io orbit animation, whose view panel shows what they see; and one drawn
  as the observer's own view, such as the lunar eclipse animation.
- **FIG-12** The Io orbit animation has a framed "What the observer sees"
  panel that moves in step with the orbit. It shows Jupiter as seen from
  the Earth, with Io beside it, crossing in front of it (transit), its
  shadow on the cloud tops (shadow transit), hidden behind it
  (occultation) and dark in its shadow (eclipse), and names the event.
- **FIG-13** Every picture on every page, diagram, photograph or
  animation, opens in a zoom view that fills the window, with zoom in,
  zoom out, reset and close, and with drag and pinch to pan and zoom. Each
  picture shows a small maximize icon in its corner at all times, not only
  on hover, so the zoom view can be found on a touch screen.
- **FIG-14** An animated picture can be played and paused in the zoom view
  as well as on the page.
- **FIG-15** Every control on a picture, in the zoom view and in the 3D
  viewer is subtle: an icon or a short word in muted colour, with no fill
  and no border until it is hovered or focused, and a target at least
  24 px square. A pressed control is marked by its text colour and an
  underline, not by a filled shape.
- **FIG-16** A "Figure index" page under Meta lists every picture on the
  site in one table, one row per picture: the picture itself, drawn as on
  its page (theme colours, Play for an animation, the zoom view), the
  first words of its caption, its kind (diagram, animation or
  photograph), a link to the page it appears on, and its provenance (drawn
  here or third-party, with the licence of a third-party picture).
  Pictures that only the build uses, such as the social preview card, are
  listed in a second table. The build generates both tables from the
  pages and `images.tsv`, so a new picture appears without editing the
  index.
- **FIG-17** The zoom view steps through the page's pictures in page order:
  subtle previous and next controls, a faint ‹ and › at the left and
  right edges of the picture and again either side of the counter in the
  zoom view's bar, and the keys PageUp and PageDown. The counter shows the
  position, such as "12 / 43". There is no previous control on the first
  picture and no next control on the last; a hidden control keeps its
  space, so neither the picture nor the bar shifts. Closing the zoom view
  returns focus to the picture last shown.
- **FIG-21** The zoom view has a faint close control, ✕, at its top right
  corner, where readers expect it, as well as Close in the bar.
- **FIG-18** Every picture has a short title of at most six words, unique
  on the site, recorded in the sixth column of its `images.tsv` row. The
  build refuses a picture without one. The zoom view shows the title above
  the caption, and the figure index shows it at the top of each row.
- **FIG-19** A long caption shows its first lines, two in the zoom view and
  three in the figure index, with a subtle "Read more" link that shows the
  whole text and then reads "Show less". A caption that fits has no link.
  The figure index carries each picture's whole caption, formatted as on
  its page.
- **FIG-20** The zoom view has a subtle "Show on page" link to the place
  where the picture appears, like a media browser's "show in chat". From
  the figure index it opens the picture's page at the picture; on the
  picture's own page it closes the zoom view and scrolls to the picture.
  Every picture has a stable anchor on its page, `#fig-` followed by its
  file name without the extension.
- **FIG-9** What an observer sees is drawn in a framed panel titled "What
  the observer sees", set apart from the main drawing: beside it in the
  example diagrams, and in a row between the two halves of the
  shadow-shape figure. No line runs from the drawing into the panel, and
  no body of the main drawing lies inside it.
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
- **HOME-6** The home page's introduction links to the primer's section on
  terminology, which explains the site's name.

## SEO: search metadata

- **SEO-1** Every page has its own search title and description, and no two
  pages share either.
- **SEO-2** The home page's search title names eclipses, occultations and
  transits, and its description names transits.
- **SEO-3** The search title of every page in the transits topic names
  transits.
- **SEO-4** The home page carries schema.org `WebSite` structured data with
  the site name, the alternate name "Computing Eclipses, Occultations and
  Transits", the home page address and the description. No other page
  carries it.

## LNK: links

A reader who meets a subject should be one click from the page of this site
that treats it in depth, and from the reference page that defines it.

- **LNK-1** A glossary term may name one canonical page outside the site: a
  Wikipedia article, or the page of the agency or project that owns the
  thing. It is the optional fourth column of `terms.tsv`. The explainer
  panel and the A to Z glossary show it as one quiet line, "Read on" and the
  site's name, such as "Read on Wikipedia". The link stays reachable by
  keyboard: the panel stays open while focus is inside it.
- **LNK-2** A page links the first mention in its prose of a named mission,
  instrument, dataset, institution, program, person, body or dated eclipse
  that has a canonical page to that page, once per page. Such a link is
  reading, not evidence: the claim beside it still carries its citation.
- **LNK-3** A page links the first mention in its prose of a subject that
  another page of the site treats in depth to that page, once per page. A
  page never links to itself.
- **LNK-4** Every relative link goes to a file of the site, and every anchor
  in one names an element of the built page it goes to.
- **LNK-5** Every external link uses https. A link in a research note and a
  glossary term's link go to a host in `CANONICAL_SITES` in
  `tools/build.py`. The build refuses a glossary link that does not.
- **LNK-6** Every research note links at least five other pages of the site
  and at least three canonical pages outside it, counting the glossary
  terms it marks.
- **LNK-7** The links of LNK-2 and LNK-3 never fall inside a heading, an
  image caption, a quotation, code, maths, a citation, a glossary marker or
  another link.
- **LNK-8** A link that leaves the site opens in a new browser tab, with
  `rel="noopener"`. A link within the site, including a citation marker, a
  glossary panel and the navigation, opens in the same tab.

## S3D: 3D guided scenes

The 3D scenes show each event as bodies in space, one event at a time. The
reader picks an event and moves it along its path; the scene and a line of
text say what happens. They use the site's existing 3D viewer, which already
offers a "View in 3D" button on a 2D figure, layer chips, a variant row, a
slider, Animate, Reset and Back.

- **S3D-1** On the primer page, the lead diagram of each case section offers
  a 3D view: the hidden case diagram opens the scene `hidden-cases`, and the
  darkened case diagram opens the scene `darkened-cases`. The 2D diagram
  stays the figure, and the reader can go back to it.
- **S3D-2** The viewer's gates and controls apply unchanged. There is no 3D
  offer without WebGL, when the reader asks for reduced motion, below a
  480 px wide window, or when three.js does not load. three.js loads only
  when the reader asks for a 3D view.
- **S3D-3** Each scene has a variant row labelled "Event" that lists the
  events of its case:
  - hidden: solar eclipse, annular solar eclipse, transit of Venus, lunar
    occultation of a star, occultation of a star by an asteroid, the solar
    eclipse the Artemis II crew saw from the Orion spacecraft, and Phobos
    crossing the Sun seen from Mars;
  - darkened: lunar eclipse, eclipse of a satellite (Io in Jupiter's
    shadow), shadow transit (Io's shadow on Jupiter).
- **S3D-4** Every body carries two labels, its role and its name, as in the
  2D figures: light source, blocking body, observer, and for the darkened
  case the darkened body and an observer on the Earth.
- **S3D-5** The slider and Animate move the event along its path. In the
  hidden case the blocking body moves across the line from the observer to
  the source, except for Artemis II, where the spacecraft carries the
  observer behind the Moon. In the darkened case the darkened body moves through the
  shadow, or for a shadow transit, the shadow moves across the planet.
- **S3D-6** A line of text under the scene states, in plain words, where the
  observer or the darkened body is (outside the shadow, in the penumbra, the
  umbra or the antumbra) and what that means: for a disc source, no eclipse,
  partial, total or annular with the percentage of the source's area that
  is covered; for a point source, whether the star is hidden. Screen
  readers announce the line when it changes.
- **S3D-7** Along the full slider, each event passes through the same
  sequence of shadow parts as the real event:
  - solar eclipse: outside, penumbra, umbra, penumbra, outside;
  - annular solar eclipse: outside, penumbra, antumbra, penumbra, outside;
  - transit of Venus: outside, penumbra, antumbra, penumbra, outside;
  - solar eclipse from Artemis II: outside, penumbra, umbra, penumbra,
    outside;
  - Phobos from Mars: outside, penumbra, antumbra, penumbra, outside;
  - lunar occultation of a star and occultation by an asteroid: outside,
    hidden, outside, with no penumbra;
  - lunar eclipse: outside, penumbra, umbra, penumbra, outside;
  - eclipse of a satellite: outside, penumbra, umbra, penumbra, outside;
  - shadow transit: the point of Jupiter under the shadow moves from one
    limb to the other.
- **S3D-8** Positions, shadow radii, shadow parts and the observer's view
  come from the geometry module (GEO-1 to GEO-4). A pure function computes
  the state of an event at a slider position: the positions, the shadow
  radii, the shadow part and the view. The scene only draws that state, and
  the function runs under Node, where its tests run.
- **S3D-9** The scenes are not to scale. Sizes and distances are compressed
  so that every body fits in view, but the ratios that decide the event are
  kept: each event's shadow parts come in the order of S3D-7. Each scene's
  note says so.
- **S3D-10** Colours come from the theme tokens used by the 2D figures: the
  Sun is the light Sun colour, and a body seen against the Sun is the
  silhouette colour. An open scene follows a theme change.
- **S3D-11** The event buttons and the slider work from the keyboard. The
  pressed event is marked for assistive technology.
- **S3D-13** Every scene shows, the whole time, the world or craft the
  observer stands on or rides in: the Earth, the Orion spacecraft or Mars.
  In the darkened case an observer stands on the Earth: on its night side
  for a lunar eclipse, and on an Earth drawn off the shadow, at a distance
  not to scale, for Jupiter's events. No observer floats in space.
- **S3D-15** The labels are subtle: plain text in small type with no box,
  the role above the name in muted type. Each label stands away from its
  body and is joined to it by a thin callout line. A label is placed where
  it covers no body and no other label; when no such place is free, it is
  left out rather than drawn over a body. Callout lines do not cross each
  other or run through another label wherever a placement without that
  exists.
- **S3D-16** The 3D viewer has a maximize icon in the corner of the
  picture. It makes the viewer fill the screen, with the browser's full
  screen mode where the browser has one and by filling the window where
  it does not. The picture resizes to fill the space, every control keeps
  working, and the icon or Escape returns the viewer to the page.
- **S3D-14** A framed panel titled "What the observer sees" sits beside the
  status line, set apart from the 3D picture. It draws the observer's view
  from the same state: in the hidden case the source (a disc, or a star as
  a point) and the blocking body's disc at their apparent sizes and
  separation; in the darkened case the darkened body as seen from the
  Earth, dimmed by the shadow, and for a shadow transit Jupiter's disc with
  the shadow on it. It changes as the slider moves.
- **S3D-12** Opening each scene and stepping through every event writes no
  error to the browser console and makes no failed request.

## MAP: the topic map

A radial mind map of the whole site, built from the contents tree and the
links between pages. It answers "what is here and what connects to what"
before a reader opens a page.

The map follows the contents tree rather than a force-directed graph, which
tangles into a hairball once there are many links and lays out differently
on each run; bundling the cross-links along the tree keeps it legible and the
build deterministic.

- **MAP-1** A Meta page, "Topic map", draws every topic of the site as one
  node of one picture. A topic is a research-notes folder of pages, or a
  page of the meta, primer or reports sections. The home page is at the
  centre and the sections and research groups are on the rings between, as
  in a radial mind map. The map page itself is not a node.
- **MAP-2** Every node is a link that opens its page: a topic its folder's
  index or its page, and a section its index. The links work with no script.
- **MAP-3** Two topics are joined by a curve when a page in one links to a
  page in the other. A curve's thickness grows with the number of such
  links, and its tooltip names both topics and the count. The build counts
  the links from the Markdown, so a new link appears at the next build.
  Curves are bundled along the tree (hierarchical edge bundling), so links
  between two research groups run together.
- **MAP-4** Once the map has more than forty curves, curves of fewer than
  three links are hidden, and a slider shows curves from one link upwards. Pointing at or focusing a topic lights its
  own curves, whatever the slider says, and the topics at their other ends,
  and dims the rest. Moving away restores the map.
- **MAP-8** Clicking a topic, or pressing Enter on it, keeps it lit after the
  pointer or focus moves away, and marks it. Clicking it again opens its
  page, as does a click asking for a new tab. Esc, a click on empty map or
  a click on another topic changes or clears the kept topic.
- **MAP-5** Under the map, a table lists every topic with its section, its
  pages as links, and the topics it is joined to with their counts. It is
  the map's text equivalent.
- **MAP-6** The build draws the map as inline SVG in the site's figure
  colours, so it follows the theme, opens from `file://` and builds to the
  same bytes every time. Every node is reachable by keyboard. At phone width
  the map keeps a legible size and scrolls sideways.
- **MAP-7** The home page links to the topic map.

## LAY: the page layout

Every page has three columns on a desktop: the navigation, the text and the
page's contents. The reader can size them to fit a wide table without
scrolling sideways.

- **LAY-1** On a desktop the Menu button hides and shows the navigation, and
  the text and contents move over to use the room. On a phone it opens and
  closes the navigation as before. Its `aria-expanded` says whether the
  navigation shows.
- **LAY-2** A handle on the line between the navigation and the text drags
  that line. The navigation keeps between 160 and 520 px; dragged nearly
  shut, it hides as LAY-1.
- **LAY-3** A handle on the line between the text and the contents drags
  that line, so the text column can grow past its reading measure to the
  room the window has. On a page with no contents rail the text keeps the
  width the reader chose.
- **LAY-4** Each handle is a focusable separator: the arrow keys move it by
  16 px (64 with Shift), Home and a double click put the column back to its
  default. The widths and the hidden navigation are kept in the browser
  (localStorage) and apply on every page. With no script the page lays out
  at the defaults.
- **LAY-5** On a window wider than the columns, the columns sit in the
  middle of it rather than at its left edge.
- **LAY-6** An in-page link (a citation, a contents entry) brings its target
  to rest below the sticky top bar and breadcrumbs, not under them; a cited
  reference is marked.
- **LAY-7** Below 861 px wide there are no handles, and the page does not
  scroll sideways.
- **LAY-8** On a desktop the breadcrumbs stay in view under the top bar as
  the page scrolls, on one line, with the current page's title cut short if
  it does not fit; the text scrolls out of sight under them. On a phone they
  scroll away with the page.
- **LAY-9** On a phone the top bar grows to hold every row it wraps onto
  (the title and buttons, then the search box); no control sits on or past
  its edge.
- **LAY-10** Every page, with or without pictures, has the search box in
  the top bar when scripts run.
- **LAY-11** The Menu and theme buttons show icons, not words: three lines
  for the menu, a half-filled circle for the theme. Both icons are drawn for
  the site as inline SVG in the same size and stroke, in the button's text
  colour. Each button keeps its name ("Menu", "Theme") for screen readers and
  as a tooltip.

## URL: page addresses

- **URL-1** Each folder under `content/` appears in page addresses under its
  URL name: the name `url-names.tsv` gives it, or else its folder name
  without a leading two-digit prefix (`01-foundations` becomes
  `foundations`). The prefix only identifies a topic; the reader never sees
  it. File names do not change.
- **URL-2** The research notes are under `research-notes/`; the meta pages,
  the primer and the reports are under `meta/`, `primer/` and `reports/`.
- **URL-3** Every relative link in a page points at its target's address.
  The build fails if two folders get the same address, or if a URL name is
  also the name of a source folder.

## SBX: the explorer

Status: outline. This section is completed before the explorer is built.

- **SBX-1** A Primer page, "Explorer", shows a side view of the bodies and their shadows
  and the observer's view, linked.
- **SBX-2** The reader picks the source (the Sun or a star), moves the bodies
  and the observer, and can play the motion.
- **SBX-3** Every control works by keyboard, and the page works at phone
  width.
- **SBX-4** Each primer section links to the explorer with its own preset.
