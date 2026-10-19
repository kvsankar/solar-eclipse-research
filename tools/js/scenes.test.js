// Acceptance tests AT-S3D-3 to AT-S3D-9 (docs/acceptance-tests.md).
// Run: node --test tools/js/scenes.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");

const STATIC = path.join(__dirname, "..", "..", "templates", "static");
const G = require(path.join(STATIC, "geometry.js"));
const S = require(path.join(STATIC, "scenes.js"));

const HIDDEN = ["solar-eclipse", "annular-solar-eclipse", "venus-transit",
  "star-occultation", "asteroid-occultation"];
const DARKENED = ["lunar-eclipse", "satellite-eclipse", "shadow-transit"];
const ROLES = {
  hidden: ["Light source", "Blocking body", "Observer"],
  darkened: ["Light source", "Blocking body", "Darkened body"],
};
const SAMPLES = 201;

function sample(id) {
  const out = [];
  for (let i = 0; i < SAMPLES; i++) out.push(S.state(id, i / (SAMPLES - 1)));
  return out;
}

function collapse(list) {
  return list.filter((x, i) => i === 0 || x !== list[i - 1]);
}

const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const norm = (a) => Math.sqrt(dot(a, a));

test("AT-S3D-3 each scene lists exactly its events, in order", () => {
  assert.deepEqual(S.scenes["hidden-cases"].events, HIDDEN);
  assert.deepEqual(S.scenes["darkened-cases"].events, DARKENED);
  for (const id of HIDDEN.concat(DARKENED)) {
    assert.equal(typeof S.events[id].label, "string", id);
    assert.ok(S.events[id].label.length > 0, id);
  }
  assert.equal(S.events["solar-eclipse"].label, "Solar eclipse");
  assert.equal(S.events["shadow-transit"].label, "Shadow transit");
});

test("AT-S3D-4 every body has a role and a name, with the case's roles", () => {
  for (const [kase, ids] of [["hidden", HIDDEN], ["darkened", DARKENED]]) {
    for (const id of ids) {
      const st = S.state(id, 0.5);
      assert.equal(st.case, kase, id);
      const roles = st.bodies.map((b) => b.role);
      assert.deepEqual(roles, ROLES[kase], id);
      for (const b of st.bodies) {
        assert.ok(b.name && b.name.length > 0, `${id} ${b.role} has a name`);
        assert.equal(b.position.length, 3, `${id} ${b.role} position`);
      }
    }
  }
});

test("AT-S3D-5 the stated body moves, monotonically along its path", () => {
  const expectMoving = {
    "solar-eclipse": "Blocking body", "annular-solar-eclipse": "Blocking body",
    "venus-transit": "Blocking body", "star-occultation": "Blocking body",
    "asteroid-occultation": "Blocking body", "lunar-eclipse": "Darkened body",
    "satellite-eclipse": "Darkened body", "shadow-transit": "Blocking body",
  };
  for (const id of HIDDEN.concat(DARKENED)) {
    const states = sample(id);
    const role = expectMoving[id];
    assert.equal(states[0].moving, role, id);
    const pick = (st) => st.bodies.find((b) => b.role === role).position;
    const still = states[0].bodies.filter((b) => b.role !== role).map((b) => b.role);
    let prevY = -Infinity;
    for (const st of states) {
      const y = pick(st)[1];
      assert.ok(y > prevY, `${id}: ${role} moves forward`);
      prevY = y;
      for (const r of still) {
        assert.deepEqual(st.bodies.find((b) => b.role === r).position,
          states[0].bodies.find((b) => b.role === r).position, `${id}: ${r} stays`);
      }
    }
  }
});

test("AT-S3D-6 the status line names the shadow part and the view", () => {
  const total = sample("solar-eclipse").find((s) => s.part === "umbra");
  assert.match(total.text, /umbra/);
  assert.match(total.text, /totally hidden/);
  const partial = sample("solar-eclipse").find((s) => s.part === "penumbra" && s.view.kind === "partial");
  assert.match(partial.text, /penumbra/);
  assert.match(partial.text, /\b\d{1,2}% of the Sun/);
  const annular = sample("annular-solar-eclipse").find((s) => s.part === "antumbra");
  assert.match(annular.text, /antumbra/);
  assert.match(annular.text, /annular/);
  const star = sample("star-occultation");
  assert.match(star.find((s) => s.part === "hidden").text, /star is hidden/);
  assert.match(star[0].text, /star is visible/);
  const lunar = sample("lunar-eclipse").find((s) => s.part === "umbra");
  assert.match(lunar.text, /the Moon is in the Earth's umbra/i);
  const outside = sample("solar-eclipse")[0];
  assert.match(outside.text, /outside/);
  assert.match(outside.text, /no eclipse/);
  for (const id of HIDDEN.concat(DARKENED)) {
    for (const st of sample(id)) assert.ok(st.text.length > 0, id);
  }
});

test("AT-S3D-7 each event passes through the real event's shadow parts", () => {
  const want = {
    "solar-eclipse": ["outside", "penumbra", "umbra", "penumbra", "outside"],
    "annular-solar-eclipse": ["outside", "penumbra", "antumbra", "penumbra", "outside"],
    "venus-transit": ["outside", "penumbra", "antumbra", "penumbra", "outside"],
    "star-occultation": ["outside", "hidden", "outside"],
    "asteroid-occultation": ["outside", "hidden", "outside"],
    "lunar-eclipse": ["outside", "penumbra", "umbra", "penumbra", "outside"],
    "satellite-eclipse": ["outside", "penumbra", "umbra", "penumbra", "outside"],
    "shadow-transit": ["outside", "umbra", "outside"],
  };
  for (const [id, seq] of Object.entries(want)) {
    assert.deepEqual(collapse(sample(id).map((s) => s.part)), seq, id);
  }
  // The shadow transit's ground point crosses the planet from limb to limb.
  const ground = sample("shadow-transit").filter((s) => s.ground).map((s) => s.ground);
  assert.ok(ground.length > 10);
  const planet = S.state("shadow-transit", 0.5).bodies.find((b) => b.role === "Darkened body");
  const lat = ground.map((g) => (g[1] - planet.position[1]) / planet.radius);
  for (let i = 1; i < lat.length; i++) assert.ok(lat[i] > lat[i - 1], "ground point moves one way");
  assert.ok(lat[0] < -0.9 && lat[lat.length - 1] > 0.9, "from one limb to the other");
});

test("AT-S3D-8 parts and views equal the geometry module's answers", () => {
  for (const id of HIDDEN.concat(DARKENED)) {
    for (const st of sample(id)) {
      const [src, blk, rcv] = st.bodies;
      // The point whose circumstances are reported: the observer, the
      // darkened body's centre, or the ground point of a shadow transit.
      const p = st.ground || rcv.position;
      if (st.source === "point") {
        const along = [1, 0, 0];
        const rel = sub(p, blk.position);
        const behind = dot(rel, along);
        const perp = norm(sub(rel, along.map((c) => c * behind)));
        const s = Math.asin(perp / norm(rel));
        const ro = Math.asin(blk.radius / norm(rel));
        const hidden = behind > 0 && G.pointHidden(s, ro);
        assert.equal(st.part, hidden ? "hidden" : "outside", id);
        assert.equal(st.view.hidden, hidden, id);
        continue;
      }
      if (id === "shadow-transit" && !st.ground) {
        assert.equal(st.part, "outside", id);
        continue;
      }
      const axisVec = sub(blk.position, src.position);
      const D = norm(axisVec);
      const axis = axisVec.map((c) => c / D);
      const rel = sub(p, blk.position);
      const behind = dot(rel, axis);
      const fromAxis = norm(sub(rel, axis.map((c) => c * behind)));
      assert.equal(st.part, G.region(src.radius, blk.radius, D, behind, fromAxis), `${id} part`);
      const toSrc = sub(src.position, p);
      const toBlk = sub(blk.position, p);
      const rs = Math.asin(src.radius / norm(toSrc));
      const ro = Math.asin(blk.radius / norm(toBlk));
      const sep = Math.acos(Math.min(1, dot(toSrc, toBlk) / (norm(toSrc) * norm(toBlk))));
      const v = G.discView(rs, ro, sep);
      assert.equal(st.view.kind, v.kind, `${id} view`);
      assert.ok(Math.abs(st.view.covered - v.covered) < 1e-12, `${id} covered`);
    }
  }
});

test("AT-S3D-9 each scene's note says it is not to scale", () => {
  for (const name of ["hidden-cases", "darkened-cases"]) {
    assert.match(S.scenes[name].note, /not to scale/i, name);
  }
});
