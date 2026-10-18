#!/usr/bin/env python3
"""Headless browser checks AT-FIG-4 and AT-FIG-5 (docs/acceptance-tests.md).

    python tools/check_browser.py

Serves site/ on a local port with caching off, opens the general primer in
headless Chromium, and checks the animated figures with normal and with
reduced motion. Records console errors and failed requests. Needs Playwright
for Python with Chromium installed; it is a local check, not part of CI.
"""

from __future__ import annotations

import functools
import http.server
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

    server.shutdown()
    for p_ in problems:
        print("FAIL", p_)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
