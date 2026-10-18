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
| AT-PRI-6 | PRI-6 | `test_primer.py`: the worked example has that title and order 2, and its last section names a lunar eclipse, an occultation and a transit with a link for each. |
| AT-FIG-1 | FIG-1 | `test_primer.py`: the primer embeds the three case diagrams, the shadow-shape figure and the five example diagrams, each with a provenance row and no gallery figure; each case diagram is the first figure in its case section; each example sits in its case's section; and every case and example diagram's visible text has a role label and a name label for every body. |
| AT-FIG-2 | FIG-2 | `test_primer.py`: each primer figure's SVG contains the word "Schematic" in its visible text. |
| AT-FIG-3 | FIG-3 | `test_primer.py`: three primer figures carry the `anim` class and SMIL animation elements that wait for a play event (`begin="indefinite"`). |
| AT-FIG-4 | FIG-4 | `check_browser.py`: with normal motion, each animated figure has one labelled play button and is still until it is pressed; pressing it starts the animation, and pressing again pauses it. With reduced motion, there is no button. |
| AT-FIG-5 | FIG-5 | `check_browser.py`: pressing a play button leaves the lightbox closed. |
| AT-FIG-7 | FIG-7 | `test_primer.py`: `site.css` defines `--fig-sun` and `--fig-silhouette` in every theme block, with `sun-fill` and `silhouette-fill` classes; no primer figure script fills the Sun with `accent-fill`, and none uses `sky-fill`. |
| AT-FIG-8 | FIG-1 | `test_primer.py`: in the solar eclipse and Venus transit diagrams the observer's marker lies inside the drawn umbra or antumbra polygon at least 4 units from its edges, and the solar inset draws a silhouette covering the whole Sun. |
| AT-FIG-6 | FIG-6 | Review: the primer figure scripts import only `figlib`. |
| AT-GEO-1 | GEO-1 | `tools/js/geometry.test.js`: Sun and Moon at mean distances give the umbral cone length and penumbral radius from the corpus formulas, and a point beyond the vertex reports the antumbra. |
| AT-GEO-2 | GEO-2 | `geometry.test.js`: points on, inside and outside each boundary classify correctly. |
| AT-GEO-3 | GEO-3 | `geometry.test.js`: coincident discs give total or annular by size; separated discs give none; the covered fraction is 0 and 1 at the extremes and matches the lens-area formula at one tabulated case. |
| AT-GEO-4 | GEO-4 | `geometry.test.js`: separations just inside and outside the radius. |
| AT-GEO-5 | GEO-5 | `geometry.test.js`: a constructed straight-line pass gives the contact times found by stepping, and a miss gives none. |
| AT-GEO-6 | GEO-6 | `geometry.test.js` loads the module with Node's `require`; `check_browser.py` loads a page that uses it from a `file://` URL. |
| AT-REP-1 | REP-1 | `test_reports_home.py`: the executive summary has a section for each case, hidden and darkened, before the first heading that names solar eclipses. |
| AT-REP-2 | REP-2 | `test_reports_home.py`: the two titles, and an opening paragraph that names solar eclipses and links `other-events.md`. |
| AT-REP-3 | REP-3 | `test_reports_home.py`: titles and `order` values give the stated sequence. |
| AT-REP-4 | REP-4 | `test_reports_home.py`: the reading list and the open questions each have a `##` section per research group. |
| AT-HOME-1 | HOME-1 | `test_reports_home.py`: the home page's first image is the collage; its provenance row and each source's row name a public-domain or CC BY-SA licence; the page's credit line names every source's author. |
| AT-HOME-2 | HOME-2 | `test_reports_home.py`: running `tools/make_collage.py` twice gives identical bytes equal to the committed collage. |
| AT-HOME-3 | HOME-3 | `test_reports_home.py`: the first paragraph after the image mentions shadows and who stands in them, and says solar eclipses are covered in most depth. |
| AT-HOME-4 | HOME-4 | `test_reports_home.py`: the summary has bullets that start with each case, hidden and darkened, and one about solar eclipses. |
| AT-HOME-5 | HOME-5 | `test_reports_home.py`: the research table has a heading per group and links every topic `_index.md`. |
