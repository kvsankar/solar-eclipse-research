#!/usr/bin/env python3
"""Headless browser checks AT-FIG-4, AT-FIG-5, AT-MAP-4, AT-LAY and the AT-S3D checks (docs/acceptance-tests.md).

    python tools/check_browser.py

Serves site/ on a local port with caching off, opens the general primer in
headless Chromium, and checks the animated figures with normal and with
reduced motion. Records console errors and failed requests. Needs Playwright
for Python with Chromium installed; it is a local check, not part of CI.
"""

from __future__ import annotations

import functools
import http.server
import json
import subprocess
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PAGE = "05-primer/how-eclipses-occultations-and-transits-are-computed.html"


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


SCENES = {
    "hidden-cases": ["solar-eclipse", "annular-solar-eclipse", "venus-transit",
                     "star-occultation", "asteroid-occultation", "artemis-eclipse",
                     "phobos-transit"],
    "darkened-cases": ["lunar-eclipse", "satellite-eclipse", "shadow-transit"],
}
STEPS = (0, 50, 100)
GL_ARGS = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]


def expected_texts() -> dict:
    """The status line each event should show at each slider step, from the
    same module under Node, so the browser is checked against the tested state."""
    script = (
        "const S=require(process.argv[1]);const out={};"
        "for(const id of Object.keys(S.events)){out[id]={};"
        f"for(const v of {list(STEPS)}) out[id][v]=S.state(id,v/100).text;}}"
        "console.log(JSON.stringify(out));")
    run = subprocess.run(["node", "-e", script, str(ROOT / "templates" / "static" / "scenes.js")],
                         capture_output=True, text=True, check=True)
    return json.loads(run.stdout)


def set_slider(viewer, value):
    viewer.locator(".fig3d-slider input").evaluate(
        "(el, v) => { el.value = v; el.dispatchEvent(new Event('input', {bubbles: true})); }", value)


def check_3d(url: str) -> list[str]:
    """AT-S3D-1, -2, -3, -6, -8, -10, -11 and -12 for the primer's 3D scenes."""
    problems: list[str] = []
    want = expected_texts()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=GL_ARGS)

        # AT-S3D-2: three.js is not fetched until asked for.
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors, failed, requests = [], [], []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("requestfailed", lambda r: failed.append(r.url))
        page.on("request", lambda r: requests.append(r.url))
        page.goto(url, wait_until="networkidle")
        if any("three.min.js" in u for u in requests):
            problems.append("three.min.js requested before any 3D view was asked for")

        for scene, events in SCENES.items():
            host = page.locator(f'.fig3d-host[data-scene="{scene}"]')
            if host.count() != 1:
                problems.append(f"{scene}: {host.count()} hosts")
                continue
            open_btn = host.locator("button.fig3d-open")
            if open_btn.count() != 1 or open_btn.inner_text().strip() != "View in 3D":
                problems.append(f"{scene}: no 'View in 3D' button")
                continue
            open_btn.click()
            viewer = host.locator(".fig3d-viewer")
            try:
                viewer.locator("canvas").wait_for(timeout=15000)
            except Exception:
                problems.append(f"{scene}: no canvas after View in 3D")
                continue
            page.wait_for_timeout(300)

            # AT-S3D-3: the Event row lists the events.
            if viewer.locator(".fig3d-vlabel").inner_text().strip() != "Event":
                problems.append(f"{scene}: variant row is not labelled Event")
            buttons = viewer.locator(".fig3d-variant")
            if buttons.count() != len(events):
                problems.append(f"{scene}: {buttons.count()} event buttons, want {len(events)}")
                continue

            # AT-S3D-14: a framed view panel, outside the canvas, that changes.
            sees = viewer.locator(".fig3d-sees")
            if sees.count() != 1:
                problems.append(f"{scene}: {sees.count()} view panels")
            else:
                if sees.locator("figcaption").inner_text().strip() != "What the observer sees":
                    problems.append(f"{scene}: view panel title")
                if sees.locator("canvas").count():
                    problems.append(f"{scene}: view panel is inside the 3D picture")
                set_slider(viewer, 10)
                page.wait_for_timeout(120)
                before = sees.locator(".fig3d-sees-art").inner_html()
                set_slider(viewer, 50)
                page.wait_for_timeout(120)
                if sees.locator(".fig3d-sees-art").inner_html() == before or "<svg" not in before:
                    problems.append(f"{scene}: view panel did not change with the slider")

            # AT-FIG-10: a corona at totality, none in a partial phase.
            if scene == "hidden-cases":
                buttons.nth(0).click()
                set_slider(viewer, 50)
                page.wait_for_timeout(150)
                if "corona-fill" not in sees.locator(".fig3d-sees-art").inner_html():
                    problems.append("3D view panel: no corona at totality")
                set_slider(viewer, 30)
                page.wait_for_timeout(150)
                if "corona-fill" in sees.locator(".fig3d-sees-art").inner_html():
                    problems.append("3D view panel: a corona in a partial phase")

            # AT-S3D-15: subtle labels on callout lines, clear of the bodies.
            for n in range(buttons.count()):
                buttons.nth(n).click()
                set_slider(viewer, 50)
                page.wait_for_timeout(200)
                report = viewer.evaluate("""v => {
                    const stage = v.querySelector('.fig3d-stage');
                    const sr = stage.getBoundingClientRect();
                    const discs = JSON.parse(stage.getAttribute('data-discs') || '[]');
                    const tags = [...v.querySelectorAll('.fig3d-tag')].filter(t => t.style.display !== 'none');
                    const boxes = tags.map(t => { const r = t.getBoundingClientRect();
                        return {text: t.textContent, l: r.left - sr.left, r: r.right - sr.left,
                                t: r.top - sr.top, b: r.bottom - sr.top,
                                bg: getComputedStyle(t).backgroundColor,
                                border: getComputedStyle(t).borderTopWidth}; });
                    const segs = [...v.querySelectorAll('.fig3d-callouts line')].map(l =>
                        ['x1', 'y1', 'x2', 'y2'].map(k => +l.getAttribute(k)));
                    return {boxes, discs, lines: segs.length, segs};
                }""")
                boxes, discs = report["boxes"], report["discs"]
                label = f"{scene}/{events[n]}"
                texts = " ".join(b["text"] for b in boxes)
                if "Light source" not in texts or "Blocking body" not in texts:
                    problems.append(f"{label}: source or blocking body label missing ({texts})")
                if report["lines"] < len(boxes):
                    problems.append(f"{label}: {len(boxes)} labels but {report['lines']} callout lines")
                for b in boxes:
                    if b["bg"] not in ("rgba(0, 0, 0, 0)", "transparent") or b["border"] not in ("0px", ""):
                        problems.append(f"{label}: label '{b['text']}' has a box")
                    for d in discs:
                        nx = min(max(d["x"], b["l"]), b["r"])
                        ny = min(max(d["y"], b["t"]), b["b"])
                        if (nx - d["x"]) ** 2 + (ny - d["y"]) ** 2 < d["r"] ** 2:
                            problems.append(f"{label}: label '{b['text']}' covers a body")
                segs = report["segs"]

                def cross(p, q):
                    def orient(a, b, c):
                        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
                    a1, a2, b1, b2 = p[:2], p[2:], q[:2], q[2:]
                    return (orient(a1, a2, b1) * orient(a1, a2, b2) < 0 and
                            orient(b1, b2, a1) * orient(b1, b2, a2) < 0)

                for i, sa in enumerate(segs):
                    for sb in segs[i + 1:]:
                        if cross(sa, sb):
                            problems.append(f"{label}: two callout lines cross")

                def through(seg, b):
                    # Sample the segment and test whether it enters the box.
                    for k in range(1, 20):
                        x = seg[0] + (seg[2] - seg[0]) * k / 20
                        y = seg[1] + (seg[3] - seg[1]) * k / 20
                        if b["l"] + 1 < x < b["r"] - 1 and b["t"] + 1 < y < b["b"] - 1:
                            return True
                    return False

                for sa in segs:
                    for b in boxes:
                        if through(sa, b):
                            problems.append(f"{label}: a callout line runs through '{b['text']}'")
                for i, a in enumerate(boxes):
                    for c in boxes[i + 1:]:
                        if not (a["r"] <= c["l"] or c["r"] <= a["l"] or a["b"] <= c["t"] or c["b"] <= a["t"]):
                            problems.append(f"{label}: labels '{a['text']}' and '{c['text']}' overlap")

            # AT-S3D-6: the status line is announced.
            readout = viewer.locator(".fig3d-readout")
            if readout.get_attribute("aria-live") != "polite":
                problems.append(f"{scene}: status line is not aria-live polite")

            for n, event in enumerate(events):
                # AT-S3D-11: keyboard selection, one pressed button.
                buttons.nth(n).focus()
                page.keyboard.press("Enter")
                page.wait_for_timeout(100)
                pressed = [buttons.nth(i).get_attribute("aria-pressed") for i in range(buttons.count())]
                if pressed.count("true") != 1 or pressed[n] != "true":
                    problems.append(f"{scene}/{event}: aria-pressed is {pressed}")
                for v in STEPS:
                    set_slider(viewer, v)
                    page.wait_for_timeout(120)
                    got = readout.inner_text().strip()
                    if got != want[event][str(v)]:
                        problems.append(f"{scene}/{event} at {v}: status '{got}', want '{want[event][str(v)]}'")

            # AT-S3D-11: arrow keys move the slider.
            slider = viewer.locator(".fig3d-slider input")
            set_slider(viewer, 50)
            slider.focus()
            page.keyboard.press("ArrowRight")
            if slider.input_value() != "51":
                problems.append(f"{scene}: ArrowRight left the slider at {slider.input_value()}")

            # AT-S3D-10: the Sun follows the theme.
            for theme in ("light", "dark"):
                page.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
                page.wait_for_timeout(250)
                set_slider(viewer, 20)
                page.wait_for_timeout(150)
                token = page.evaluate(
                    "getComputedStyle(document.documentElement).getPropertyValue('--fig-sun').trim()")
                drawn = viewer.get_attribute("data-sun")
                if (drawn or "").lower() != token.lower():
                    problems.append(f"{scene} {theme}: Sun drawn {drawn}, token {token}")
            page.evaluate("document.documentElement.removeAttribute('data-theme')")

            # AT-S3D-1: back to the diagram.
            viewer.locator('[data-act="back"]').click()
            page.wait_for_timeout(200)
            if host.locator(".fig3d-viewer").count() or not host.locator("svg").first.is_visible():
                problems.append(f"{scene}: Back to diagram did not restore the SVG")

        if errors:
            problems.append(f"3D: console errors: {errors}")
        local_failed = [u for u in failed if u.startswith("http://127.0.0.1")]
        if local_failed:
            problems.append(f"3D: failed requests: {local_failed}")
        page.close()

        # AT-S3D-2: no offer when narrow or with reduced motion.
        page = browser.new_page(viewport={"width": 400, "height": 800})
        page.goto(url, wait_until="networkidle")
        if page.locator("button.fig3d-open").count():
            problems.append("narrow window: a View in 3D button is offered")
        page.close()
        ctx = browser.new_context(reduced_motion="reduce")
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        if page.locator("button.fig3d-open").count():
            problems.append("reduced motion: a View in 3D button is offered")
        ctx.close()

        # AT-S3D-8 and AT-GEO-6: the modules load from file:// too.
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto((SITE / PAGE).as_uri(), wait_until="load")
        btn = page.locator('.fig3d-host[data-scene="hidden-cases"] button.fig3d-open')
        if btn.count():
            btn.click()
            try:
                page.locator('.fig3d-host[data-scene="hidden-cases"] canvas').wait_for(timeout=15000)
            except Exception:
                problems.append("file://: the scene did not open")
            if not page.evaluate("!!(window.EclipseGeometry && window.EclipseScenes)"):
                problems.append("file://: geometry.js or scenes.js did not load")
        else:
            problems.append("file://: no View in 3D button")
        if errors:
            problems.append(f"file://: console errors: {errors}")
        page.close()
        browser.close()
    return problems


SUBTLE_JS = """els => els.filter(e => e.offsetParent !== null).map(e => {
    const c = getComputedStyle(e), r = e.getBoundingClientRect();
    return {text: (e.getAttribute('aria-label') || e.textContent).trim().slice(0, 30),
            bg: c.backgroundColor, border: c.borderTopWidth,
            w: Math.round(r.width), h: Math.round(r.height)};
})"""


def subtle_problems(where: str, buttons: list) -> list[str]:
    out = []
    for b in buttons:
        if b["bg"] not in ("rgba(0, 0, 0, 0)", "transparent") or b["border"] != "0px":
            out.append(f"{where}: button '{b['text']}' is not subtle (bg {b['bg']}, border {b['border']})")
        if b["w"] < 24 or b["h"] < 24:
            out.append(f"{where}: button '{b['text']}' is {b['w']}x{b['h']} px, under 24 px")
    return out


def check_zoom(base: str) -> list[str]:
    """AT-FIG-13, -14 and -15, and AT-S3D-16."""
    problems: list[str] = []
    url = base + PAGE
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=GL_ARGS)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)

        # AT-FIG-13: every picture on every page sits in a zoom button.
        for html in sorted(SITE.rglob("*.html")):
            rel = html.relative_to(SITE).as_posix()
            page.goto(base + rel, wait_until="load")
            loose = page.evaluate("""() => [...document.querySelectorAll('main img, main svg.figsvg')]
                .filter(e => !e.closest('.figzoom') && !e.closest('.fig3d-viewer')).length""")
            if loose:
                problems.append(f"{rel}: {loose} pictures without a zoom view")

        page.goto(url, wait_until="networkidle")
        zooms = page.locator("button.figzoom")
        hidden_icons = page.evaluate("""() => [...document.querySelectorAll('button.figzoom')]
            .filter(b => +getComputedStyle(b, '::after').opacity < 0.4).length""")
        if hidden_icons:
            problems.append(f"{hidden_icons} zoom icons are hidden until hover")
        zooms.first.click()
        box = page.locator(".lb")
        if not box.is_visible():
            problems.append("the zoom view did not open")
        else:
            label = box.locator(".lb-zoom")
            before = label.inner_text()
            box.locator('[data-act="in"]').click()
            if label.inner_text() == before:
                problems.append("zoom in did not change the scale")
            box.locator('[data-act="out"]').click()
            box.locator('[data-act="reset"]').click()
            if label.inner_text() != before:
                problems.append("reset did not return to the fitted scale")
            problems += subtle_problems("zoom view", box.locator("button").evaluate_all(SUBTLE_JS))
            box.locator('[data-act="close"]').click()
            if box.is_visible():
                problems.append("close did not close the zoom view")

        # AT-FIG-17: step through the figure index in the zoom view.
        page.goto(base + "00-meta/figure-index.html", wait_until="networkidle")
        total = page.locator("button.figzoom").count()
        page.locator("button.figzoom").first.click()
        box = page.locator(".lb")
        count = box.locator(".lb-count")
        prev, nxt = box.locator('.lb-row [data-act="prev"]'), box.locator('.lb-row [data-act="next"]')
        bprev, bnxt = box.locator('.lb-bar [data-act="bar-prev"]'), box.locator('.lb-bar [data-act="bar-next"]')
        if count.inner_text().strip() != f"1 / {total}":
            problems.append(f"zoom view counter reads '{count.inner_text()}', want '1 / {total}'")
        if prev.is_visible() or not nxt.is_visible() or bprev.is_visible() or not bnxt.is_visible():
            problems.append("first picture: want next controls and no previous controls, beside and in the bar")
        bar_x = box.locator(".lb-count").bounding_box()["x"]
        problems += subtle_problems("zoom view nav", box.locator(".lb-nav").evaluate_all(SUBTLE_JS))
        first_cap = box.locator(".lb-cap").inner_text()
        nxt.click()
        if count.inner_text().strip() != f"2 / {total}" or box.locator(".lb-cap").inner_text() == first_cap:
            problems.append("next did not show the second picture")
        prev.click()
        if count.inner_text().strip() != f"1 / {total}":
            problems.append("previous did not return to the first picture")
        bnxt.click()
        if count.inner_text().strip() != f"2 / {total}":
            problems.append("the bar's next did not move to the second picture")
        if abs(box.locator(".lb-count").bounding_box()["x"] - bar_x) > 1:
            problems.append("the bar shifted when its previous control appeared")
        bprev.click()
        if count.inner_text().strip() != f"1 / {total}":
            problems.append("the bar's previous did not return to the first picture")
        problems += subtle_problems("zoom view bar nav", box.locator(".lb-bar .lb-step").evaluate_all(SUBTLE_JS))
        page.keyboard.press("PageDown")
        if count.inner_text().strip() != f"2 / {total}":
            problems.append("PageDown did not move to the next picture")
        page.keyboard.press("PageUp")
        if count.inner_text().strip() != f"1 / {total}":
            problems.append("PageUp did not move to the previous picture")
        for _ in range(total - 1):
            page.keyboard.press("PageDown")
        if count.inner_text().strip() != f"{total} / {total}" or nxt.is_visible() or bnxt.is_visible():
            problems.append("last picture: want the counter at the end and no next controls")
        # AT-FIG-21: the top right close.
        x = box.locator(".lb-x")
        if x.count() != 1:
            problems.append("the zoom view has no top right close")
        else:
            r = x.bounding_box()
            vw = page.evaluate("innerWidth")
            if r["y"] > 72 or vw - (r["x"] + r["width"]) > 72:
                problems.append(f"the top close is not at the top right ({r})")
            problems += subtle_problems("zoom view top close", x.evaluate_all(SUBTLE_JS))
            x.click()
            if box.is_visible():
                problems.append("the top close did not close the zoom view")
        focused = page.evaluate("document.activeElement === [...document.querySelectorAll('button.figzoom')].pop()")
        if not focused:
            problems.append("closing did not focus the picture last shown")
        page.goto(url, wait_until="networkidle")

        # AT-FIG-18 and AT-FIG-19: titles, and Read more where a caption is cut.
        for where in ("05-primer/how-eclipses-occultations-and-transits-are-computed.html",
                      "00-meta/figure-index.html"):
            page.goto(base + where, wait_until="networkidle")
            zooms = page.locator("button.figzoom")
            for i in range(min(zooms.count(), 6)):
                want = zooms.nth(i).evaluate("b => (b.querySelector('[data-figtitle]') || {}).dataset?.figtitle || ''")
                zooms.nth(i).click()
                lb = page.locator(".lb")
                got = lb.locator(".lb-title").inner_text().strip()
                if not want or got != want:
                    problems.append(f"{where} picture {i + 1}: zoom title '{got}', want '{want}'")
                cut = lb.locator(".lb-cap").evaluate("c => c.scrollHeight > c.clientHeight + 1")
                more = lb.locator(".lb-more")
                if cut != more.is_visible():
                    problems.append(f"{where} picture {i + 1}: caption cut {cut}, Read more shown {more.is_visible()}")
                if cut:
                    more.click()
                    full = lb.locator(".lb-cap").evaluate("c => c.scrollHeight <= c.clientHeight + 1")
                    if not full or more.inner_text().strip() != "Show less":
                        problems.append(f"{where} picture {i + 1}: Read more did not show the whole caption")
                    more.click()
                    if more.inner_text().strip() != "Read more":
                        problems.append(f"{where} picture {i + 1}: Show less did not cut the caption again")
                lb.locator('[data-act="close"]').click()
        page.goto(base + "00-meta/figure-index.html", wait_until="networkidle")
        rows = page.locator("tr.figrow")
        for i in range(rows.count()):
            row = rows.nth(i)
            if not row.locator(".figtitle").inner_text().strip():
                problems.append(f"index row {i + 1}: no title")
            cut = row.locator(".figcap").evaluate("c => c.scrollHeight > c.clientHeight + 1")
            if cut != row.locator(".figmore").is_visible():
                problems.append(f"index row {i + 1}: caption cut {cut}, Read more shown")
        long_row = rows.filter(has=page.locator(".figmore:visible")).first
        if long_row.count():
            long_row.locator(".figmore").click()
            if long_row.locator(".figcap").evaluate("c => c.scrollHeight > c.clientHeight + 1"):
                problems.append("index: Read more did not show the whole caption")
        page.goto(url, wait_until="networkidle")

        # AT-FIG-20: Show on page, from the index and on the picture's own page.
        page.goto(base + "00-meta/figure-index.html", wait_until="networkidle")
        target = page.locator('tr.figrow:has([data-figpath="05-primer/img/example-solar-eclipse.svg"]) button.figzoom')
        if target.count() != 1:
            problems.append("index: no row for the solar eclipse example")
        else:
            target.click()
            link = page.locator(".lb .lb-page")
            href = link.get_attribute("href") or ""
            if link.inner_text().strip() != "Show on page" or not href.endswith(
                    "how-eclipses-occultations-and-transits-are-computed.html#fig-example-solar-eclipse"):
                problems.append(f"index: Show on page link is '{link.inner_text()}' to '{href}'")
            link.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(400)
            shown = page.evaluate("""() => { const e = document.getElementById('fig-example-solar-eclipse');
                if (!e) return false; const r = e.getBoundingClientRect();
                return r.bottom > 0 && r.top < innerHeight; }""")
            if not shown:
                problems.append(f"Show on page did not open the page at the picture ({page.url})")
        page.goto(url, wait_until="networkidle")
        no_id = page.evaluate("""() => [...document.querySelectorAll('main svg.figsvg, main figure img')]
            .filter(e => !(e.id || '').startsWith('fig-')).length""")
        if no_id:
            problems.append(f"primer: {no_id} pictures without a fig- anchor")
        late = page.locator("button.figzoom").nth(8)
        late.click()
        page.locator(".lb .lb-page").click()
        page.wait_for_timeout(400)
        inview = late.evaluate("b => { const r = b.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }")
        if page.locator(".lb").is_visible() or not inview:
            problems.append("on its own page, Show on page did not close the zoom view at the picture")
        page.goto(url, wait_until="networkidle")

        # AT-FIG-14: an animation plays in the zoom view.
        anim = page.locator(".anim-host button.figzoom").first
        anim.click()
        play = box.locator('[data-act="play"]')
        if play.count() != 1:
            problems.append("the zoom view of an animation has no play button")
        else:
            play.click()
            page.wait_for_timeout(200)
            started = box.evaluate("""b => [...b.querySelectorAll('animate,animateTransform,animateMotion')]
                .every(a => { try { a.getStartTime(); return true } catch (e) { return false } })""")
            if not started:
                problems.append("play in the zoom view did not start the animation")
        box.locator('[data-act="close"]').click()

        # AT-FIG-15: the buttons on the page are subtle.
        problems += subtle_problems("page", page.locator(".anim-play, .fig3d-open").evaluate_all(SUBTLE_JS))

        # AT-S3D-16: maximize the 3D viewer, use it, and return.
        host = page.locator('.fig3d-host[data-scene="hidden-cases"]')
        host.locator("button.fig3d-open").click()
        viewer = host.locator(".fig3d-viewer")
        viewer.locator("canvas").wait_for(timeout=15000)
        problems += subtle_problems("3D viewer", viewer.locator("button").evaluate_all(SUBTLE_JS))
        mx = viewer.locator(".fig3d-stage button.fig3d-max")
        if mx.count() != 1:
            problems.append("the 3D viewer has no maximize button in its picture")
        else:
            inline = viewer.locator(".fig3d-stage").bounding_box()["width"]
            mx.click()
            page.wait_for_timeout(500)
            wide = viewer.locator(".fig3d-stage").bounding_box()["width"]
            if wide < 0.9 * 1280:
                problems.append(f"maximized, the 3D picture is {wide:.0f} px wide")
            before = viewer.locator(".fig3d-readout").inner_text()
            set_slider(viewer, 50)
            page.wait_for_timeout(200)
            if viewer.locator(".fig3d-readout").inner_text() == before:
                problems.append("maximized, the slider did not change the status line")
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            back = viewer.locator(".fig3d-stage").bounding_box()["width"]
            if abs(back - inline) > 2:
                problems.append(f"after Escape the 3D picture is {back:.0f} px wide, was {inline:.0f}")
            mx.click()
            page.wait_for_timeout(400)
            mx.click()
            page.wait_for_timeout(400)
            again = viewer.locator(".fig3d-stage").bounding_box()["width"]
            if abs(again - inline) > 2:
                problems.append("the maximize button did not return the viewer to the page")
        if errors:
            problems.append(f"zoom and maximize: console errors: {errors}")
        browser.close()
    return problems


MAP_PAGE = "00-meta/topic-map.html"


def check_topic_map(base: str) -> list[str]:
    """AT-MAP-4, AT-MAP-8 and the browser half of AT-MAP-6 for the topic map."""
    problems: list[str] = []
    shown_js = ("ps => ps.filter(p => getComputedStyle(p).display != 'none').length")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(base + MAP_PAGE, wait_until="load")
        total = page.locator(".tm-links path").count()
        shown = page.eval_on_selector_all(".tm-links path", shown_js)
        if not 0 < shown < total:
            problems.append(f"topic map: {shown} of {total} curves shown at the default threshold")
        page.locator("#tm-min").fill("1")
        page.locator("#tm-min").dispatch_event("input")
        if page.eval_on_selector_all(".tm-links path", shown_js) != total:
            problems.append("topic map: the slider at 1 does not show every curve")

        # Point at the topic at one end of the first curve.
        ends = page.locator(".tm-links path").first.get_attribute("data-ends").split()
        own = page.eval_on_selector_all(
            ".tm-links path", "(ps, id) => ps.filter(p => p.dataset.ends.split(' ').includes(id)).length",
            ends[0])
        page.hover(f"#{ends[0]} circle")
        page.wait_for_timeout(300)
        if not page.eval_on_selector("svg.tm", "s => s.classList.contains('tm-focus')"):
            problems.append("topic map: pointing at a topic does not light it")
        if page.locator(".tm-links path.on").count() != own:
            problems.append("topic map: the lit curves are not exactly the topic's own")
        dim = page.eval_on_selector_all(
            ".tm-topic:not(.on)", "ts => ts.map(t => +getComputedStyle(t).opacity)")
        if not dim or max(dim) >= 0.5:
            problems.append("topic map: topics off the lit curves are not dimmed")
        page.mouse.move(2, 2)
        page.wait_for_timeout(300)
        if page.eval_on_selector("svg.tm", "s => s.classList.contains('tm-focus')"):
            problems.append("topic map: moving away does not restore the map")

        # AT-MAP-8: a click keeps the topic lit; Esc clears it.
        page.click(f"#{ends[0]} circle")
        page.mouse.move(2, 2)
        page.wait_for_timeout(300)
        if not page.url.endswith(MAP_PAGE):
            problems.append("topic map: the first click on a topic left the page")
        if page.locator(".tm-links path.on").count() != own:
            problems.append("topic map: a clicked topic does not stay lit")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        if page.eval_on_selector("svg.tm", "s => s.classList.contains('tm-focus')"):
            problems.append("topic map: Esc does not clear the kept topic")

        # By keyboard: focus lights the topic, Enter keeps it, Enter again opens it.
        page.focus(f"#{ends[1]}")
        if not page.eval_on_selector("svg.tm", "s => s.classList.contains('tm-focus')"):
            problems.append("topic map: focusing a topic does not light it")
        href = page.get_attribute(f"#{ends[1]}", "href")
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        if page.get_attribute(f"#{ends[1]}", "aria-current") != "true":
            problems.append("topic map: Enter on a topic does not keep it")
        try:
            with page.expect_navigation(timeout=5000):
                page.keyboard.press("Enter")
        except Exception:
            pass
        if not page.url.endswith(href.replace("../", "")):
            problems.append(f"topic map: Enter on a topic opened {page.url}, not {href}")
        if errors:
            problems.append(f"topic map: console errors {errors}")
        page.close()

        # At phone width the map keeps its size and scrolls sideways.
        page = browser.new_page(viewport={"width": 390, "height": 800})
        page.goto(base + MAP_PAGE, wait_until="load")
        box = page.eval_on_selector(".topicmap", "d => [d.scrollWidth, d.clientWidth, d.querySelector('svg').getBoundingClientRect().width]")
        if box[2] < 560 or box[0] <= box[1]:
            problems.append(f"topic map: at phone width the map is {box[2]} px wide and does not scroll")
        page.close()
        browser.close()
    return problems


def check_layout(base: str) -> list[str]:
    """AT-LAY-1 to AT-LAY-7: the hideable navigation, the two resize handles,
    the centred layout and in-page links landing below the top bar."""
    problems: list[str] = []
    box_js = "s => { const b = document.querySelector(s).getBoundingClientRect(); return [b.left, b.width, b.top]; }"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(base + PAGE, wait_until="load")
        page.evaluate("localStorage.clear()")
        page.reload(wait_until="load")
        side = lambda: page.evaluate(box_js, ".sidebar")
        doc = lambda: page.evaluate(box_js, ".colwrap .doc")

        # AT-LAY-4: two separators with a tab stop.
        handles = page.locator(".gutter")
        if handles.count() != 2:
            problems.append(f"layout: {handles.count()} resize handles, not 2")
        for i in range(handles.count()):
            h = handles.nth(i)
            if h.get_attribute("role") != "separator" or h.get_attribute("tabindex") != "0":
                problems.append(f"layout: handle {i} is not a focusable separator")

        # AT-LAY-1: Menu hides and restores the navigation.
        left0 = doc()[0]
        page.click("#navtoggle")
        page.wait_for_timeout(100)
        if page.get_attribute("#navtoggle", "aria-expanded") != "false" or page.is_visible("#sidebar"):
            problems.append("layout: Menu does not hide the navigation on a desktop")
        if doc()[0] >= left0:
            problems.append("layout: hiding the navigation does not move the text left")
        page.click("#navtoggle")
        page.wait_for_timeout(100)
        if page.get_attribute("#navtoggle", "aria-expanded") != "true" or abs(doc()[0] - left0) > 1:
            problems.append("layout: a second Menu press does not restore the navigation")

        def drag(sel, dx):
            b = page.locator(sel).bounding_box()
            x, y = b["x"] + b["width"] / 2, b["y"] + 300
            page.mouse.move(x, y)
            page.mouse.down()
            page.mouse.move(x + dx, y, steps=8)
            page.mouse.up()
            b = page.locator(sel).bounding_box()
            return b["x"] + b["width"] / 2 - (x + dx)

        # AT-LAY-2 and AT-LAY-3: the handles move their columns and stay under the
        # pointer. In a centred layout a column grows by twice the pointer's travel.
        w0 = side()[1]
        off = drag(".layout > .gutter", -40)
        if side()[1] > w0 - 40 or abs(off) > 3:
            problems.append(f"layout: the navigation handle moved it {side()[1] - w0:.0f} px, {off:.0f} px off the pointer")
        d0 = doc()[1]
        off = drag(".colwrap > .gutter", 100)
        if doc()[1] < d0 + 99 or abs(off) > 3:
            problems.append(f"layout: the text handle widened it {doc()[1] - d0:.0f} px, {off:.0f} px off the pointer")

        # AT-LAY-4: keys, persistence and reset.
        w1, d1 = side()[1], doc()[1]
        page.focus(".layout > .gutter")
        page.keyboard.press("ArrowLeft")
        if abs(side()[1] - (w1 - 16)) > 1:
            problems.append("layout: ArrowLeft does not narrow the navigation by 16 px")
        page.reload(wait_until="load")
        if abs(side()[1] - (w1 - 16)) > 1 or abs(doc()[1] - d1) > 1:
            problems.append("layout: the dragged widths do not hold after a reload")
        page.click("#navtoggle")
        page.reload(wait_until="load")
        if page.is_visible("#sidebar"):
            problems.append("layout: the hidden navigation does not stay hidden after a reload")
        page.click("#navtoggle")
        page.focus(".layout > .gutter")
        page.keyboard.press("Home")
        page.focus(".colwrap > .gutter")
        page.keyboard.press("Home")
        if abs(side()[1] - w0) > 1 or abs(doc()[1] - d0) > 1:
            problems.append("layout: Home does not reset the columns")

        # AT-LAY-8: the breadcrumbs stay under the top bar, one line, opaque.
        page.evaluate("window.scrollTo(0, 1500)")
        page.wait_for_timeout(100)
        bar, crumbs, line, bg = page.evaluate("""() => {
            const c = document.querySelector('.crumbs'), l = c.querySelector('li');
            return [document.querySelector('.topbar').getBoundingClientRect().bottom,
                    c.getBoundingClientRect().toJSON(), l.getBoundingClientRect().height,
                    getComputedStyle(c).backgroundColor]; }""")
        if abs(crumbs["top"] - bar) > 1:
            problems.append(f"layout: scrolled, the breadcrumbs sit at {crumbs['top']:.0f} px, not under the top bar at {bar:.0f}")
        if page.evaluate("document.querySelector('.crumblist').getBoundingClientRect().height") > line * 1.5:
            problems.append("layout: the sticky breadcrumbs wrap onto a second line")
        if bg in ("transparent", "rgba(0, 0, 0, 0)"):
            problems.append("layout: the sticky breadcrumbs have no background, so text shows through")

        # AT-LAY-6: a citation's reference lands below the breadcrumbs and is marked.
        bar = crumbs["bottom"]
        href = page.get_attribute(".cite a", "href")
        page.click(".cite a")
        page.wait_for_timeout(300)
        top = page.evaluate("h => document.getElementById(h).getBoundingClientRect().top", href.split("#")[1])
        if top < bar:
            problems.append(f"layout: a cited reference rests {top:.0f} px from the top, under the top bar")
        if not page.evaluate("h => document.getElementById(h).matches(':target')", href.split("#")[1]):
            problems.append("layout: the cited reference is not the :target")

        # AT-LAY-5: centred on a wide window.
        page.set_viewport_size({"width": 2560, "height": 900})
        page.wait_for_timeout(100)
        rail = page.evaluate(box_js, ".toc-rail")
        lgap, rgap = side()[0], 2560 - (rail[0] + rail[1])
        if abs(lgap - rgap) > 20:
            problems.append(f"layout: at 2560 px the columns are not centred ({lgap:.0f} px left, {rgap:.0f} px right)")

        # AT-LAY-7: no handles and no sideways scroll on a phone.
        page.set_viewport_size({"width": 390, "height": 800})
        page.wait_for_timeout(100)
        if page.locator(".gutter:visible").count():
            problems.append("layout: resize handles show at phone width")
        page.evaluate("window.scrollTo(0, 1500)")
        page.wait_for_timeout(100)
        if page.evaluate("document.querySelector('.crumbs').getBoundingClientRect().bottom") > 0:
            problems.append("layout: at phone width the breadcrumbs do not scroll away")
        if page.evaluate("document.documentElement.scrollWidth") > 390:
            problems.append("layout: the page scrolls sideways at phone width")
        if errors:
            problems.append(f"layout: console errors {errors}")
        browser.close()
    return problems


def main() -> int:
    handler = functools.partial(NoCache, directory=str(SITE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_address[1]}/{PAGE}"
    problems: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Normal motion: one labelled button per animated figure, still until pressed.
        page = browser.new_page()
        errors, failed = [], []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("requestfailed", lambda r: failed.append(r.url))
        page.goto(url, wait_until="networkidle")
        hosts = page.locator(".anim-host")
        count = hosts.count()
        if count != 3:
            problems.append(f"expected 3 animated figures, found {count}")
        for i in range(count):
            host = hosts.nth(i)
            buttons = host.locator("button.anim-play")
            if buttons.count() != 1:
                problems.append(f"figure {i}: {buttons.count()} play buttons")
                continue
            btn = buttons.first
            if not (btn.get_attribute("aria-label") or "").startswith("Play"):
                problems.append(f"figure {i}: play button has no accessible name")
            begun = host.evaluate(
                "h => [...h.querySelectorAll('animate,animateTransform,animateMotion,set')]"
                ".some(a => { try { a.getStartTime(); return true } catch (e) { return false } })")
            if begun:
                problems.append(f"figure {i}: an animation began before Play")
            btn.click()
            page.wait_for_timeout(300)
            if page.locator(".lb-open, body.lb-open").count():
                problems.append(f"figure {i}: Play opened the lightbox (FIG-5)")
            begun = host.evaluate(
                "h => [...h.querySelectorAll('animate,animateTransform,animateMotion,set')]"
                ".every(a => { try { a.getStartTime(); return true } catch (e) { return false } })")
            if not begun:
                problems.append(f"figure {i}: Play did not start the animation")
            if btn.get_attribute("aria-pressed") != "true":
                problems.append(f"figure {i}: aria-pressed not true while playing")
            btn.click()
            if not host.evaluate("h => h.querySelector('svg').animationsPaused()"):
                problems.append(f"figure {i}: second press did not pause")
        if errors:
            problems.append(f"console errors: {errors}")
        local_failed = [u for u in failed if u.startswith("http://127.0.0.1")]
        if local_failed:
            problems.append(f"failed requests: {local_failed}")
        page.close()

        # Reduced motion: no buttons at all.
        ctx = browser.new_context(reduced_motion="reduce")
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        n = page.locator("button.anim-play").count()
        if n:
            problems.append(f"reduced motion: {n} play buttons present")
        ctx.close()
        browser.close()

    problems += check_3d(url)
    problems += check_zoom(url.rsplit(PAGE, 1)[0])
    problems += check_topic_map(url.rsplit(PAGE, 1)[0])
    problems += check_layout(url.rsplit(PAGE, 1)[0])

    server.shutdown()
    for p_ in problems:
        print("FAIL", p_)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
