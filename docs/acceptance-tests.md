# Acceptance tests

Each test checks one requirement in [specs.md](specs.md). Automated tests run
in CI. Browser tests run headless against the built site through a local web
server, with caching off, by `python tools/check_browser.py`.

| Test | Requirement | How it is checked |
|---|---|---|
| AT-PRI-1 | PRI-1 | `test_primer.py`: the Primer's first page has that title and a section for each case, named "Hidden" and "Darkened", and no "Both" section. |
| AT-PRI-2 | PRI-2 | `test_primer.py`: the classification table has one row per kind of event below, each in one case with its source marked point or disc, and every link in it resolves to a page in the build. Kinds: solar eclipse, transit of Mercury or Venus, lunar eclipse, eclipse of a satellite, shadow transit, mutual eclipse, lunar occultation of a star, lunar occultation of a planet, occultation by an asteroid or TNO, occultation of a satellite by its planet, transit of a satellite, mutual occultation, occultation of one planet by another. |
| AT-PRI-3 | PRI-3 | `test_primer.py`: the page names umbra, penumbra and antumbra with total, partial and annular, and names the cylinder of a point source. |
| AT-PRI-4 | PRI-4 | `test_primer.py`: the page cites the 1992 Explanatory Supplement next to the four terms. |
| AT-PRI-5 | PRI-5 | `test_primer.py`: the last section links to the worked example, the glossary, the research notes and the reports. |
| AT-PRI-7 | PRI-7 | `test_primer.py`: the terminology section names the site, says that a transit is an occultation, and quotes the Supplement's section heading. |
| AT-PRI-6 | PRI-6 | `test_primer.py`: the worked example has that title and order 2, and its last section names a lunar eclipse, an occultation and a transit with a link for each. |
| AT-FIG-1 | FIG-1 | `test_primer.py`: the primer embeds the three case diagrams, the shadow-shape figure and the five example diagrams, each with a provenance row and no gallery figure; each case diagram is the first figure in its case section; each example sits in its case's section; and every case and example diagram's visible text has a role label and a name label for every body. |
| AT-FIG-2 | FIG-2 | `test_primer.py`: each primer figure's SVG contains the word "Schematic" in its visible text. |
| AT-FIG-3 | FIG-3 | `test_primer.py`: three primer figures carry the `anim` class and SMIL animation elements that wait for a play event (`begin="indefinite"`). |
| AT-FIG-4 | FIG-4 | `check_browser.py`: with normal motion, each animated figure has one labelled play button and is still until it is pressed; pressing it starts the animation, and pressing again pauses it. With reduced motion, there is no button. |
| AT-FIG-5 | FIG-5 | `check_browser.py`: pressing a play button leaves the lightbox closed. |
| AT-FIG-7 | FIG-7 | `test_primer.py`: `site.css` defines `--fig-sun` and `--fig-silhouette` in every theme block, with `sun-fill` and `silhouette-fill` classes; no primer figure script fills the Sun with `accent-fill`, and none uses `sky-fill`. |
| AT-FIG-8 | FIG-1 | `test_primer.py`: in the solar eclipse and Venus transit diagrams the observer's marker lies inside the drawn umbra or antumbra polygon at least 4 units from its edges, and the solar inset draws a silhouette covering the whole Sun. |
| AT-FIG-10 | FIG-10 | `test_primer.py`: in the solar eclipse example, the shadow-shape figure and the solar eclipse animation, each total view has a circle of class `corona-fill`, filled by a radial gradient, larger than its dark disc and centred on it, and no Sun-coloured circle larger than that disc at the same centre; `site.css` defines `--fig-corona` in every theme block. `check_browser.py`: the 3D view panel shows a corona at totality and none in a partial phase. |
| AT-FIG-11 | FIG-11 | `test_primer.py`: in every primer SVG, each circle of class `observer` lies on the edge of, or inside, a circle of class `body`; every figure that labels an observer has such a marker, except `anim-io-orbit.svg`, whose observer is a direction arrow, and `anim-lunar-eclipse.svg`, drawn as the observer's view. |
| AT-FIG-12 | FIG-12 | `test_primer.py`: `anim-io-orbit.svg` has a panel titled "What the observer sees" holding Jupiter and Io, with Io's and the shadow's motion animated by SMIL elements that wait for Play and share the orbit's duration, and the four event names shown in turn. |
| AT-FIG-13 | FIG-13 | `check_browser.py`: on every built page, every picture in the page body sits in a zoom button; on the primer page each zoom button shows its icon without hover (opacity at least 0.4), clicking it opens the zoom view, and the zoom view's zoom in, zoom out, reset and close work. |
| AT-FIG-14 | FIG-14 | `check_browser.py`: opening an animated figure in the zoom view shows a play button, and pressing it starts every SMIL element of the copy in the zoom view. |
| AT-FIG-15 | FIG-15 | `check_browser.py`: the zoom view's buttons, the play buttons, the "View in 3D" button and the 3D viewer's buttons have a transparent background and no border at rest, and are at least 24 px in each direction. |
| AT-FIG-9 | FIG-9 | `test_primer.py`: the solar eclipse, Venus transit and shadow-shape figures each have a rectangle of class `panel` containing the text "What the observer sees" and every view of the source; no body of the main drawing and no line end from the drawing lies inside the panel. |
| AT-FIG-6 | FIG-6 | Review: the primer figure scripts import only `figlib`. |
| AT-GEO-1 | GEO-1 | `tools/js/geometry.test.js`: Sun and Moon at mean distances give the umbral cone length and penumbral radius from the corpus formulas, and a point beyond the vertex reports the antumbra. |
| AT-GEO-2 | GEO-2 | `geometry.test.js`: points on, inside and outside each boundary classify correctly. |
| AT-GEO-3 | GEO-3 | `geometry.test.js`: coincident discs give total or annular by size; separated discs give none; the covered fraction is 0 and 1 at the extremes and matches the lens-area formula at one tabulated case. |
| AT-GEO-4 | GEO-4 | `geometry.test.js`: separations just inside and outside the radius. |
| AT-GEO-5 | GEO-5 | `geometry.test.js`: a constructed straight-line pass gives the contact times found by stepping, and a miss gives none. |
| AT-GEO-6 | GEO-6 | `geometry.test.js` loads the module with Node's `require`; `check_browser.py` loads a page that uses it from a `file://` URL. |
| AT-S3D-1 | S3D-1 | `test_primer.py`: the hidden and darkened case diagrams carry `{.fig3d scene="hidden-cases"}` and `{.fig3d scene="darkened-cases"}`, and the built page wraps each in a `fig3d-host` with that scene. `check_browser.py`: each host shows "View in 3D", opens a canvas, and "Back to diagram" restores the SVG. |
| AT-S3D-2 | S3D-2 | `check_browser.py`: with reduced motion, and at a 400 px wide window, the primer shows no "View in 3D" button; before the button is pressed, no request for `three.min.js` is made. |
| AT-S3D-3 | S3D-3 | `tools/js/scenes.test.js`: each scene lists exactly its events, in that order. `check_browser.py`: the open scene's variant row is labelled "Event" and has one button per event. |
| AT-S3D-4 | S3D-4 | `scenes.test.js`: every event's state names each body with a role and a name, and the roles are those listed. |
| AT-S3D-5 | S3D-5 | `scenes.test.js`: across the slider, the moving body is the one stated for the event, and its position changes monotonically along its path. |
| AT-S3D-6 | S3D-6 | `scenes.test.js`: the status text for sampled states names the shadow part and the view, with a percentage for a partial disc view and "hidden" or "visible" for a star. `check_browser.py`: the status line has `aria-live="polite"` and changes when the slider moves. |
| AT-S3D-7 | S3D-7 | `scenes.test.js`: sampling each event at 201 slider positions and collapsing repeats gives exactly the stated sequence; the shadow transit's ground point moves from one limb to the other. |
| AT-S3D-8 | S3D-8 | `scenes.test.js`: for sampled states, the shadow part and view equal what `geometry.js` returns for the same positions and radii. `check_browser.py`: the page that opens a scene loads `geometry.js` from a `file://` URL as well as over HTTP (completes AT-GEO-6). |
| AT-S3D-9 | S3D-9 | `scenes.test.js`: each scene's note contains "not to scale". |
| AT-S3D-10 | S3D-10 | `check_browser.py`: in light and dark themes the Sun's material colour equals `--fig-sun`, and switching the theme with a scene open changes it. |
| AT-S3D-11 | S3D-11 | `check_browser.py`: focusing an event button and pressing Enter selects it and sets `aria-pressed="true"` on it only; the arrow keys move the slider. |
| AT-S3D-13 | S3D-13 | `scenes.js` tests: every state has a world for the observer (name, centre, radius) and the observer lies on its surface; darkened states include an observer on the Earth, on the Earth's surface. The drawing is checked by review of headless renders of every event. |
| AT-S3D-15 | S3D-15 | `check_browser.py`: in both scenes, for every event at the middle of its path, every label has no background or border, has a callout line from its body, and covers neither a body's disc on screen nor another label; no two callout lines cross and no line runs through another label; at least the light source's and the blocking body's labels are shown. |
| AT-S3D-16 | S3D-16 | `check_browser.py`: an open scene has a maximize button in its stage; pressing it makes the viewer fill the window (its stage at least 90% of the window's width), the slider still changes the status line, and pressing it again or Escape returns the stage to its page width. |
| AT-S3D-14 | S3D-14 | `scenes.test.js`: the view data agree with the state (apparent radii and separation for a disc source, the hidden flag for a star, the dimming for a darkened body, the shadow's place on Jupiter). `check_browser.py`: the open scene has a framed panel titled "What the observer sees" outside the canvas, and its drawing changes when the slider moves. |
| AT-S3D-12 | S3D-12 | `check_browser.py`: opening both scenes and selecting every event at three slider positions logs no console error and no failed request. |
| AT-REP-1 | REP-1 | `test_reports_home.py`: the executive summary has a section for each case, hidden and darkened, before the first heading that names solar eclipses. |
| AT-REP-2 | REP-2 | `test_reports_home.py`: the two titles, and an opening paragraph that names solar eclipses and links `other-events.md`. |
| AT-REP-3 | REP-3 | `test_reports_home.py`: titles and `order` values give the stated sequence. |
| AT-REP-4 | REP-4 | `test_reports_home.py`: the reading list and the open questions each have a `##` section per research group. |
| AT-HOME-1 | HOME-1 | `test_reports_home.py`: the home page's first image is the collage; its provenance row and each source's row name a public-domain or CC BY-SA licence; the page's credit line names every source's author. |
| AT-HOME-2 | HOME-2 | `test_reports_home.py`: running `tools/make_collage.py` twice gives identical bytes equal to the committed collage. |
| AT-HOME-3 | HOME-3 | `test_reports_home.py`: the first paragraph after the image mentions shadows and who stands in them, and says solar eclipses are covered in most depth. |
| AT-HOME-4 | HOME-4 | `test_reports_home.py`: the summary has bullets that start with each case, hidden and darkened, and one about solar eclipses. |
| AT-HOME-6 | HOME-6 | `test_reports_home.py`: the introduction links to the terminology section of the primer page. |
| AT-SEO-1 | SEO-1 | `test_seo.py`: every page has an explicit search title and description, each unique. |
| AT-SEO-2 | SEO-2 | `test_seo.py`: the home page's head title names eclipse, occultation and transit, and its description names transits. |
| AT-SEO-3 | SEO-3 | `test_seo.py`: every page under `14-transits` has "transit" in its search title. |
| AT-SEO-4 | SEO-4 | `test_seo.py`: the rendered home page has one `application/ld+json` block of type `WebSite` with the name, the alternate name, the canonical home address and the description; a deep page has none. |
| AT-HOME-5 | HOME-5 | `test_reports_home.py`: the research table has a heading per group and links every topic `_index.md`. |
