// Acceptance tests AT-GEO-1 to AT-GEO-6 (docs/acceptance-tests.md).
// Run: node --test tools/js/
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");

const G = require(path.join(__dirname, "..", "..", "templates", "static", "geometry.js"));

const SUN_RADIUS = 696000; // km, the prediction constant the corpus uses
const MOON_RADIUS = 1737.4; // km
const SUN_MOON = 149597870.7 - 384400; // km, Sun to Moon at new moon, mean

const close = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg}: ${a} vs ${b}`);

test("AT-GEO-1 shadow radii follow the cone angles", () => {
  const s = G.shadowRadii(SUN_RADIUS, MOON_RADIUS, SUN_MOON, 0);
  close(s.umbra, MOON_RADIUS / Math.cos(Math.asin((SUN_RADIUS - MOON_RADIUS) / SUN_MOON)), 1e-6, "umbra at the body");
  // The umbral vertex lies at R_b / sin f_u behind the centre of the body.
  const vertex = MOON_RADIUS / ((SUN_RADIUS - MOON_RADIUS) / SUN_MOON);
  close(G.umbraLength(SUN_RADIUS, MOON_RADIUS, SUN_MOON), vertex, 1e-3, "umbra length");
  assert.ok(vertex > 370000 && vertex < 380000, "Moon's umbra is about 374,000 km long");
  const beyond = G.shadowRadii(SUN_RADIUS, MOON_RADIUS, SUN_MOON, vertex + 10000);
  assert.equal(beyond.antumbra, true);
  assert.ok(beyond.umbra > 0, "antumbra radius is reported as a positive number");
  const before = G.shadowRadii(SUN_RADIUS, MOON_RADIUS, SUN_MOON, vertex - 10000);
  assert.equal(before.antumbra, false);
  assert.ok(before.penumbra > before.umbra);
});

test("AT-GEO-2 a point is classified by the shadow region it sits in", () => {
  const x = 380000; // just beyond the umbral vertex: annular for points on the axis
  const s = G.shadowRadii(SUN_RADIUS, MOON_RADIUS, SUN_MOON, x);
  assert.equal(G.region(SUN_RADIUS, MOON_RADIUS, SUN_MOON, x, 0), "antumbra");
  assert.equal(G.region(SUN_RADIUS, MOON_RADIUS, SUN_MOON, x, s.penumbra * 0.99), "penumbra");
  assert.equal(G.region(SUN_RADIUS, MOON_RADIUS, SUN_MOON, x, s.penumbra * 1.01), "outside");
  const y = 360000; // inside the umbral cone
  const t = G.shadowRadii(SUN_RADIUS, MOON_RADIUS, SUN_MOON, y);
  assert.equal(G.region(SUN_RADIUS, MOON_RADIUS, SUN_MOON, y, t.umbra * 0.99), "umbra");
  assert.equal(G.region(SUN_RADIUS, MOON_RADIUS, SUN_MOON, y, t.umbra * 1.01), "penumbra");
});

test("AT-GEO-3 the observer's view of two discs", () => {
  assert.equal(G.discView(1, 1.05, 0).kind, "total");
  assert.equal(G.discView(1, 1.05, 0).covered, 1);
  const ann = G.discView(1, 0.95, 0);
  assert.equal(ann.kind, "annular");
  close(ann.covered, 0.95 * 0.95, 1e-12, "annular covered fraction");
  assert.equal(G.discView(1, 0.3, 1.31).kind, "none");
  assert.equal(G.discView(1, 0.3, 1.31).covered, 0);
  // Equal discs half a radius apart: lens area 2 acos(1/4) - (1/2) sqrt(15)/4... checked by the formula.
  const r = 1, d = 0.5;
  const lens = 2 * r * r * Math.acos(d / (2 * r)) - (d / 2) * Math.sqrt(4 * r * r - d * d);
  const p = G.discView(r, r, d);
  assert.equal(p.kind, "partial");
  close(p.covered, lens / Math.PI, 1e-12, "lens fraction");
  close(lens / Math.PI, 0.6850, 1e-4, "tabulated value for equal discs at d = 0.5");
});

test("AT-GEO-4 a point source is hidden only inside the disc", () => {
  assert.equal(G.pointHidden(0.999, 1), true);
  assert.equal(G.pointHidden(1.001, 1), false);
});

test("AT-GEO-5 contact times solve the straight-line pass", () => {
  const u = -3, v = 0.4, up = 1.2, vp = 0.1, L = 0.8;
  const c = G.contacts(u, v, up, vp, L);
  assert.ok(c && c.length === 2 && c[0] < c[1]);
  // Step along the path and find where the separation crosses L.
  const sep = (t) => Math.hypot(u + up * t, v + vp * t);
  let first = null, last = null;
  for (let t = 0; t <= 6; t += 1e-5) {
    const inside = sep(t) <= L;
    if (inside && first === null) first = t;
    if (inside) last = t;
  }
  close(c[0], first, 2e-5, "first contact");
  close(c[1], last, 2e-5, "last contact");
  assert.equal(G.contacts(u, 2, up, 0, L), null, "a pass that misses has no contacts");
  assert.equal(G.contacts(u, v, 0, 0, L), null, "no motion, no contacts");
});

test("AT-GEO-6 the module is plain, with no page access", () => {
  const src = require("node:fs").readFileSync(
    path.join(__dirname, "..", "..", "templates", "static", "geometry.js"), "utf8");
  assert.ok(!/\bdocument\b|\bwindow\b/.test(src), "no DOM access");
  assert.ok(!/\brequire\(/.test(src), "no dependency");
});
