#!/usr/bin/env python3
"""Headless browser checks AT-FIG-4, AT-FIG-5 and the AT-S3D checks (docs/acceptance-tests.md).

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
                    const lines = v.querySelectorAll('.fig3d-callouts line').length;
                    return {boxes, discs, lines};
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

    server.shutdown()
    for p_ in problems:
        print("FAIL", p_)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
