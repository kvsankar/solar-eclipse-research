/* Progressive 3D figures.

   The SVG in the page is the figure. This script offers a three-dimensional
   view of the same subject *only* where the runtime can actually deliver one,
   and it never removes the SVG: the 3D view is drawn beside it and the reader
   can go back. Every gate below is a reason to stay silent rather than show a
   broken control:

     * no WebGL context
     * the reader asks for reduced motion
     * the viewport is too small to orbit usefully
     * three.js fails to load, which is normal offline or behind a policy

   three.js is vendored (MIT, see assets/vendor/three.LICENSE.md) and fetched
   only when a reader asks for a 3D view, so the 608 KB never loads for anyone
   who does not use it.

   A scene is a set of named layers. Each layer can be switched off, and each
   carries a direction along which it slides when the reader pulls the figure
   apart, so the assembly can be taken to pieces the way an exploded drawing
   takes apart an engine. */
(function () {
  "use strict";

  var hosts = document.querySelectorAll(".fig3d-host[data-scene]");
  if (!hosts.length) return;

  var here = document.currentScript && document.currentScript.src;
  if (!here) return;
  var THREE_URL = here.replace(/site3d\.js(\?.*)?$/, "vendor/three.min.js");

  // ------------------------------------------------------------ feasibility
  function webglAvailable() {
    try {
      var c = document.createElement("canvas");
      var gl = c.getContext("webgl") || c.getContext("experimental-webgl");
      if (!gl) return false;
      var lose = gl.getExtension("WEBGL_lose_context");
      if (lose) lose.loseContext();
      return true;
    } catch (e) {
      return false;
    }
  }

  function reducedMotion() {
    return !!(window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  }

  if (!webglAvailable() || reducedMotion() || window.innerWidth < 480) return;
  if (typeof Promise !== "function") return;

  // --------------------------------------------------------------- loading
  var pending = null;
  function loadThree() {
    if (pending) return pending;
    pending = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = THREE_URL;
      s.async = true;
      s.onload = function () {
        if (window.THREE) resolve(window.THREE);
        else reject(new Error("three.js loaded but exported nothing"));
      };
      s.onerror = function () { reject(new Error("three.js could not be loaded")); };
      document.head.appendChild(s);
    });
    return pending;
  }

  // --------------------------------------------------------------- palette
  /* Colours come from the same custom properties the SVGs use, read at run
     time, so a 3D figure matches the reader's theme. */
  function palette() {
    var cs = getComputedStyle(document.documentElement);
    function v(name, fallback) {
      return cs.getPropertyValue(name).trim() || fallback;
    }
    return {
      ink: v("--fig-ink", "#3a3732"),
      dim: v("--fig-dim", "#6f6b63"),
      line: v("--fig-line", "#c7c2b8"),
      accent: v("--fig-accent", "#8a5a2b"),
      accent2: v("--fig-accent-2", "#2d6a5a"),
      fill: v("--fig-fill", "#ece5da"),
      bg: v("--bg", "#fbfaf8")
    };
  }

  // ------------------------------------------------------- orbit controls
  function Orbit(camera, el, radius, THREE, home0, changed) {
    /* A scene may name the view it wants to open on: one that suits a cone
       seen end-on suits nothing else. */
    var h0 = home0 || {};
    var theta = h0.theta != null ? h0.theta : 0.9;
    var phi = h0.phi != null ? h0.phi : 1.15;
    var r = h0.r != null ? h0.r : radius;
    var target = new THREE.Vector3(0, 0, 0);
    var home = { theta: theta, phi: phi, r: r };
    var dragging = false, lx = 0, ly = 0;

    function apply() {
      phi = Math.max(0.08, Math.min(Math.PI - 0.08, phi));
      r = Math.max(0.04, Math.min(16, r));
      camera.position.set(
        target.x + r * Math.sin(phi) * Math.sin(theta),
        target.y + r * Math.cos(phi),
        target.z + r * Math.sin(phi) * Math.cos(theta)
      );
      camera.lookAt(target);
      if (changed) changed();
    }

    el.addEventListener("pointerdown", function (e) {
      dragging = true; lx = e.clientX; ly = e.clientY;
      el.setPointerCapture(e.pointerId);
      el.classList.add("grabbing");
    });
    el.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      theta -= (e.clientX - lx) * 0.008;
      phi -= (e.clientY - ly) * 0.008;
      lx = e.clientX; ly = e.clientY;
      apply();
    });
    function stop(e) {
      dragging = false;
      el.classList.remove("grabbing");
      if (e && e.pointerId != null && el.hasPointerCapture &&
          el.hasPointerCapture(e.pointerId)) {
        el.releasePointerCapture(e.pointerId);
      }
    }
    el.addEventListener("pointerup", stop);
    el.addEventListener("pointercancel", stop);
    /* Scale by the distance scrolled. A trackpad sends dozens of small wheel
       events per flick, so a fixed step per event crossed the whole zoom range
       in one gesture and slammed into the clamp. */
    el.addEventListener("wheel", function (e) {
      e.preventDefault();
      var unit = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? 400 : 1;
      var d = e.deltaY * unit * 0.0016;
      r *= Math.exp(Math.max(-0.4, Math.min(0.4, d)));
      apply();
    }, { passive: false });

    apply();
    return {
      reset: function () {
        theta = home.theta; phi = home.phi; r = home.r;
        target.set(0, 0, 0);
        apply();
      },
      aim: function (v, distance) {
        var u = v.clone().normalize();
        phi = Math.acos(Math.max(-1, Math.min(1, u.y)));
        theta = Math.atan2(u.x, u.z);
        target.copy(v);
        r = distance;
        apply();
      }
    };
  }

  // ---------------------------------------------------------------- scenes
  var SCENES = {};

  /* The fundamental plane and the eight Besselian elements, built from the
     published elements of the 2024 April 8 eclipse. Units are Earth
     equatorial radii, so the Earth is the unit sphere and every length drawn
     is the number the tables print. */
  SCENES["fundamental-plane"] = function (THREE, root, pal) {
    var E = {
      x: -0.318244, y: 0.219764,
      l1: 0.535814, l2: -0.010272,
      tanf1: 0.0046683, tanf2: 0.0046450,
      d: 7.586200, mu: 89.591217
    };
    var gamma = Math.sqrt(E.x * E.x + E.y * E.y);
    var layers = [], labels = [];

    function layer(id, label, dx, dy, dz, order, on) {
      var g = new THREE.Group();
      root.add(g);
      layers.push({
        id: id, label: label, group: g, order: order,
        explode: new THREE.Vector3(dx, dy, dz),
        on: on !== false
      });
      return g;
    }
    function tag(at, text, layerId) {
      labels.push({ at: at, text: text, layer: layerId });
    }
    function line(points, colour, dashed) {
      var g = new THREE.BufferGeometry().setFromPoints(points);
      var m = dashed
        ? new THREE.LineDashedMaterial({ color: colour, dashSize: 0.045, gapSize: 0.03 })
        : new THREE.LineBasicMaterial({ color: colour });
      var l = new THREE.Line(g, m);
      if (dashed) l.computeLineDistances();
      return l;
    }
    function arrow(from, to, colour) {
      var dir = to.clone().sub(from);
      var len = dir.length();
      return new THREE.ArrowHelper(dir.normalize(), from, len,
        new THREE.Color(colour), Math.min(0.07, len * 0.28),
        Math.min(0.045, len * 0.18));
    }
    function circle(centre, radius, colour, segments) {
      var pts = [];
      for (var i = 0; i <= (segments || 96); i++) {
        var t = i / (segments || 96) * Math.PI * 2;
        pts.push(new THREE.Vector3(
          centre.x + radius * Math.cos(t), centre.y + radius * Math.sin(t), centre.z));
      }
      return line(pts, colour);
    }

    var axisFoot = new THREE.Vector3(E.x, E.y, 0);
    var dr = E.d * Math.PI / 180;
    var pole = new THREE.Vector3(0, Math.cos(dr), Math.sin(dr));

    // --- the Earth ------------------------------------------------------
    var gGlobe = layer("globe", "Earth", 0, 0, 0, 0);
    gGlobe.add(new THREE.Mesh(
      new THREE.SphereGeometry(0.995, 48, 32),
      new THREE.MeshBasicMaterial({ color: pal.fill })));
    // Turn the graticule to the real pole rather than to the poles of its own
    // tessellation, so it does not imply an axis the Earth does not have.
    var gwire = new THREE.LineSegments(
      new THREE.WireframeGeometry(new THREE.SphereGeometry(1, 24, 16)),
      new THREE.LineBasicMaterial({ color: pal.line, transparent: true, opacity: 0.5 }));
    gwire.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), pole);
    gGlobe.add(gwire);

    // --- the shadow axis, and which way the Moon lies -------------------
    var gAxis = layer("axis", "Shadow axis", 0, 0, 0, 0);
    gAxis.add(line([new THREE.Vector3(E.x, E.y, -2.4),
                    new THREE.Vector3(E.x, E.y, 2.4)], pal.accent2));
    gAxis.add(arrow(new THREE.Vector3(E.x, E.y, 1.95),
                    new THREE.Vector3(E.x, E.y, 2.4), pal.accent2));
    tag(new THREE.Vector3(E.x, E.y, 2.5), "toward the Moon", "axis");

    // --- the fundamental plane -------------------------------------------
    var gPlane = layer("plane", "Fundamental plane", 0, 0, -1.3, 1);
    gPlane.add(new THREE.Mesh(
      new THREE.CircleGeometry(1.75, 64),
      new THREE.MeshBasicMaterial({
        color: pal.accent, transparent: true, opacity: 0.1,
        side: THREE.DoubleSide, depthWrite: false })));
    gPlane.add(circle(new THREE.Vector3(0, 0, 0), 1.75, pal.accent));
    tag(new THREE.Vector3(1.75, 0, 0), "fundamental plane", "plane");

    // --- x, y and gamma, measured on the plane ---------------------------
    var gEl = layer("elements", "x, y, γ", 0, 0, -2.3, 2);
    gEl.add(arrow(new THREE.Vector3(0, 0, 0), new THREE.Vector3(E.x, 0, 0), pal.ink));
    gEl.add(arrow(new THREE.Vector3(E.x, 0, 0), axisFoot.clone(), pal.ink));
    gEl.add(line([new THREE.Vector3(0, 0, 0), axisFoot.clone()], pal.accent2, true));
    tag(new THREE.Vector3(E.x / 2, -0.07, 0), "x = −" + Math.abs(E.x).toFixed(3), "elements");
    tag(new THREE.Vector3(E.x - 0.1, E.y / 2, 0), "y = " + E.y.toFixed(3), "elements");
    tag(new THREE.Vector3(E.x / 2 + 0.08, E.y / 2 + 0.06, 0),
        "γ = " + gamma.toFixed(3), "elements");

    // --- the two radii the cones cut on the plane ------------------------
    var gRadii = layer("radii", "l₁ and l₂", 0, 0, -3.3, 3);
    gRadii.add(circle(axisFoot, E.l1, pal.accent2));
    gRadii.add(circle(axisFoot, Math.abs(E.l2), pal.accent, 48));
    gRadii.add(arrow(axisFoot.clone(),
                     new THREE.Vector3(E.x + E.l1, E.y, 0), pal.accent2));
    tag(new THREE.Vector3(E.x + E.l1 * 0.55, E.y + 0.08, 0),
        "l₁ = " + E.l1.toFixed(3), "radii");
    tag(new THREE.Vector3(E.x + 0.16, E.y - 0.12, 0),
        "l₂ = −" + Math.abs(E.l2).toFixed(4), "radii");

    // --- the cones -------------------------------------------------------
    function r1(z) { return E.l1 - z * E.tanf1; }
    function r2(z) { return Math.abs(E.l2 - z * E.tanf2); }
    function cone(radiusAt, zLo, zHi, colour, opacity) {
      var m = new THREE.Mesh(
        new THREE.CylinderGeometry(radiusAt(zHi), radiusAt(zLo), zHi - zLo, 64, 1, true),
        new THREE.MeshBasicMaterial({
          color: colour, transparent: true, opacity: opacity,
          side: THREE.DoubleSide, depthWrite: false }));
      m.rotation.x = Math.PI / 2;
      m.position.set(E.x, E.y, (zHi + zLo) / 2);
      return m;
    }

    var gPen = layer("penumbra", "Penumbral cone", 0, 0, 1.8, 2);
    gPen.add(cone(r1, -1.9, 1.9, pal.dim, 0.14));
    tag(new THREE.Vector3(E.x + E.l1, E.y, 1.5), "penumbra", "penumbra");
    tag(new THREE.Vector3(E.x - E.l1, E.y, -1.5),
        "f₁ = 0.27°", "penumbra");

    var gUmb = layer("umbra", "Umbral cone", 0, 0, 3.1, 3);
    gUmb.add(cone(r2, E.l2 / E.tanf2, 1.9, pal.ink, 0.5));
    tag(new THREE.Vector3(E.x, E.y - 0.12, 1.2), "umbra", "umbra");

    // --- where the umbral cone meets the globe ---------------------------
    /* The cone cuts an exact circle on the plane and this shape on the
       sphere. Solved for z at each angle by Newton on |P(z)| = 1. */
    var foot = [], centre = new THREE.Vector3();
    for (var i = 0; i <= 96; i++) {
      var th = i / 96 * Math.PI * 2;
      var z = Math.sqrt(Math.max(0.01, 1 - E.x * E.x - E.y * E.y));
      for (var k = 0; k < 24; k++) {
        var rr = r2(z);
        var px = E.x + rr * Math.cos(th), py = E.y + rr * Math.sin(th);
        var f = px * px + py * py + z * z - 1;
        var df = 2 * z - 2 * E.tanf2 *
          (px * Math.cos(th) + py * Math.sin(th)) * Math.sign(E.l2 - z * E.tanf2);
        if (Math.abs(df) < 1e-9) break;
        var step = f / df;
        z -= step;
        if (Math.abs(step) < 1e-12) break;
      }
      var r = r2(z);
      foot.push(new THREE.Vector3(E.x + r * Math.cos(th), E.y + r * Math.sin(th), z));
    }
    foot.forEach(function (p) { centre.add(p); });
    centre.multiplyScalar(1 / foot.length);

    var gFoot = layer("footprint", "Umbra on the ground", 0, 0, 0.9, 1);
    gFoot.add(line(foot, pal.accent));
    tag(centre.clone(), "umbra on the ground", "footprint");

    // --- the Earth's axis, and the declination d -------------------------
    var gTilt = layer("declination", "Earth's axis and d", 0, 0, 0, 0);
    gTilt.add(line([pole.clone().multiplyScalar(-1.45),
                    pole.clone().multiplyScalar(1.45)], pal.dim));
    var arc = [];
    for (var a = 0; a <= 24; a++) {
      var t = a / 24 * dr;
      arc.push(new THREE.Vector3(0, Math.cos(t), Math.sin(t)).multiplyScalar(1.22));
    }
    gTilt.add(line(arc, pal.accent));
    tag(pole.clone().multiplyScalar(1.55), "Earth's axis", "declination");
    tag(new THREE.Vector3(0, 1.32, dr * 0.6 * 1.22),
        "d = " + E.d.toFixed(2) + "°", "declination");

    // --- the Greenwich meridian and mu -----------------------------------
    /* mu is the Greenwich hour angle of the shadow axis, the element that
       ties the shadow to the rotating Earth. */
    var gMer = layer("mu", "Greenwich meridian and μ", 0, 0, 0, 0, false);
    var zHat = new THREE.Vector3(0, 0, 1);
    var u = zHat.clone().sub(pole.clone().multiplyScalar(zHat.dot(pole))).normalize();
    var v = new THREE.Vector3().crossVectors(pole, u).normalize();
    var mr = E.mu * Math.PI / 180;
    var g = u.clone().multiplyScalar(Math.cos(mr))
      .add(v.clone().multiplyScalar(-Math.sin(mr))).normalize();

    var eq = [];
    for (var e2 = 0; e2 <= 96; e2++) {
      var t2 = e2 / 96 * Math.PI * 2;
      eq.push(u.clone().multiplyScalar(Math.cos(t2))
        .add(v.clone().multiplyScalar(Math.sin(t2))).multiplyScalar(1.004));
    }
    gMer.add(line(eq, pal.dim));
    var mer = [];
    for (var m2 = 0; m2 <= 48; m2++) {
      var s = -Math.PI / 2 + m2 / 48 * Math.PI;
      mer.push(pole.clone().multiplyScalar(Math.sin(s))
        .add(g.clone().multiplyScalar(Math.cos(s))).multiplyScalar(1.004));
    }
    gMer.add(line(mer, pal.accent));
    var muArc = [];
    for (var q = 0; q <= 40; q++) {
      var t3 = -q / 40 * mr;
      muArc.push(u.clone().multiplyScalar(Math.cos(t3))
        .add(v.clone().multiplyScalar(Math.sin(t3))).multiplyScalar(1.1));
    }
    gMer.add(line(muArc, pal.accent));
    tag(g.clone().multiplyScalar(1.12), "Greenwich meridian", "mu");
    tag(u.clone().multiplyScalar(Math.cos(-mr / 2))
      .add(v.clone().multiplyScalar(Math.sin(-mr / 2))).multiplyScalar(1.2),
      "μ = " + E.mu.toFixed(2) + "°", "mu");

    return {
      layers: layers,
      labels: labels,
      focus: { at: centre, radius: 0.1, label: "Zoom to the umbra" },
      note: "Drawn from the published elements for 2024 April 8, in Earth " +
            "radii, so nothing is exaggerated. The penumbra really is wider " +
            "than half the Earth, the umbra really is about a hundredth of " +
            "its radius, and both cone half-angles really are about a quarter " +
            "of a degree, which is why the cones look like cylinders."
    };
  };

  /* The four types of solar eclipse, as one shared drawing geometry.

     The three central cases keep one gamma and change only the umbral radius
     on the fundamental plane, u. The umbral cone closes to a point, its
     vertex, at a height u / tan f2 above that plane, and since that height
     barely changes during an eclipse the vertex sweeps out a plane of its
     own. The ground at the sub-shadow point stands sqrt(1 - gamma^2) above
     the same plane. Where the ground reaches past the vertex the converging
     umbra lands and the eclipse is total; where it does not, the vertex is
     short of the ground, the antumbra lands, and the eclipse is annular. A
     hybrid is the case where the ground crosses the vertex plane partway
     along the path, so one eclipse is both. The partial case changes gamma
     because its defining condition is that the axis misses the Earth.

     The flat figure has to bend the vertex locus into an arc, because it draws
     the Moon close enough to see. At true scale it is a plane, and the
     crossing is the work of the Earth's curvature alone.

     THE FRAME. The globe is drawn the way a reader expects to meet it: north
     up, so dragging left and right turns the Earth about its own axis and
     carries the view east and west. Everything to do with the shadow is
     therefore built on its own basis rather than on the world axes:

        M   toward the Moon, at the declination of the shadow axis
        E1  east at the sub-lunar point, which is the way the shadow travels
        E2  the Besselian y axis, toward the projection of the north pole

     and a point is placed by at(s, g, h): s along the path, g the offset of
     the axis from the geocentre, h the height above the fundamental plane.
     Units are Earth equatorial radii and nothing is exaggerated. */
  SCENES["eclipse-types"] = function (THREE, root, pal) {
    var TAN_F1 = 0.0046683;     // penumbral cone half-angle
    var TAN_F2 = 0.0046450;     // umbral cone half-angle, mean geometry
    var L1 = 0.5358;            // penumbral radius on the fundamental plane
    var RE_KM = 6378.1;         // Earth equatorial radius, for the readout
    /* Ground marks sit just clear of the globe mesh to stay out of the depth
       buffer's way. The clearance has to be small: at the zoom where a 16 km
       umbra is legible, a gap of a few thousandths of an Earth radius is
       wider than the umbra, and the footprint parts company with the cone. */
    var GLOBE_R = 0.9995;
    var LIFT = 1.0005;
    var DEC = 15.0;             // declination of the shadow axis
    var SWEEP = 0.90;           // drawn stretch of the path, each way
    /* The umbra and antumbra are one double cone translated along its axis.
       Keep the same finite length around every vertex so changing type moves
       one shape instead of resizing it. The much wider penumbra stays clipped
       to fixed planes around the Earth. */
    var UMBRA_HALF_SPAN = 2.40;
    var PENUMBRA_TOP = 2.10;
    var PENUMBRA_BOTTOM = -1.75;

    /* gamma is the least distance of the axis from the geocentre, u the
       umbral radius on the fundamental plane, both in Earth radii and both in
       the sense Meeus uses: u < 0 is total, u > 0.0047 annular, and between
       them a hybrid if u < 0.00464 sqrt(1 - gamma^2). */
    var TYPES = [
      { id: "partial", label: "Partial", gamma: 1.045, u: 0.0042 },
      { id: "annular", label: "Annular", gamma: 0.350, u: 0.0075 },
      { id: "total", label: "Total", gamma: 0.350, u: -0.0060 },
      { id: "hybrid", label: "Hybrid", gamma: 0.350, u: 0.0025 }
    ];
    var cur = TYPES[3], ZV = 0, YT = 0, groundKind = "";

    var layers = [], labels = [];

    // --- the shadow's own basis, tilted off the world axes by declination ---
    var NORTH = new THREE.Vector3(0, 1, 0);
    var dr = DEC * Math.PI / 180;
    var M = new THREE.Vector3(Math.cos(dr), Math.sin(dr), 0).normalize();
    var E1 = new THREE.Vector3().crossVectors(NORTH, M).normalize();
    var E2 = new THREE.Vector3().crossVectors(M, E1).normalize();
    // Cylinders and sphere caps are built about +Y, circles about +Z.
    var Q_Y = new THREE.Quaternion().setFromUnitVectors(NORTH, M);
    var Q_Z = new THREE.Quaternion().setFromUnitVectors(
      new THREE.Vector3(0, 0, 1), M);

    function at(s, g, h) {
      return E1.clone().multiplyScalar(s)
        .add(E2.clone().multiplyScalar(g))
        .add(M.clone().multiplyScalar(h));
    }

    function layer(id, label, ex, order, on) {
      var g = new THREE.Group();
      root.add(g);
      layers.push({
        id: id, label: label, group: g, order: order,
        explode: ex || new THREE.Vector3(),
        on: on !== false
      });
      return g;
    }
    /* Labels are placed in list order and a later one is dropped if it would
       land on an earlier one, so the order is a priority. The shadow on the
       ground is what a reader came to find: it must not lose a collision to
       the equator. */
    function tag(at_, text, layerId, prio) {
      labels.push({ at: at_, text: text, layer: layerId, prio: prio || 50 });
      return at_;
    }
    /* Every material is cached. The ground is rebuilt on every frame of the
       animation, and a material minted per call is a material orphaned per
       frame. `through` draws the line whatever stands in front of it, which
       is how buried geometry reads as a hidden line. */
    var MAT = {}, FILL = {}, PMAT = {};
    function mat(colour, dashed, through) {
      var key = colour + (dashed ? "-d" : "") + (through ? "-t" : "");
      if (!MAT[key]) {
        var m = dashed
          ? new THREE.LineDashedMaterial(
            { color: colour, dashSize: 0.05, gapSize: 0.035 })
          : new THREE.LineBasicMaterial({ color: colour });
        if (through) { m.depthTest = false; m.transparent = true; }
        MAT[key] = m;
      }
      return MAT[key];
    }
    function fillMat(colour, opacity) {
      var key = colour + "|" + opacity;
      if (!FILL[key]) {
        FILL[key] = new THREE.MeshBasicMaterial({
          color: colour, transparent: true, opacity: opacity,
          side: THREE.DoubleSide, depthWrite: false });
      }
      return FILL[key];
    }
    function surfaceMat(colour, opacity) {
      var key = colour + "|" + opacity + "|surface";
      if (!FILL[key]) {
        FILL[key] = new THREE.MeshBasicMaterial({
          color: colour, transparent: true, opacity: opacity,
          side: THREE.FrontSide, depthTest: false, depthWrite: false
        });
      }
      return FILL[key];
    }
    function line(points, colour, dashed, through) {
      var l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),
        mat(colour, dashed, through));
      if (dashed) l.computeLineDistances();
      return l;
    }
    // A circle in a plane perpendicular to the Moon's direction.
    function ring(radius, h, colour, dashed) {
      var pts = [];
      for (var i = 0; i <= 120; i++) {
        var t = i / 120 * Math.PI * 2;
        pts.push(at(radius * Math.cos(t), radius * Math.sin(t), h));
      }
      return line(pts, colour, dashed);
    }
    function disc(radius, h, colour, opacity) {
      var mesh = new THREE.Mesh(
        new THREE.CircleGeometry(radius, 96), fillMat(colour, opacity));
      mesh.quaternion.copy(Q_Z);
      mesh.position.copy(M.clone().multiplyScalar(h));
      return mesh;
    }
    function over(obj, order) {
      obj.renderOrder = order;
      return obj;
    }

    /* A point of interest is a thin ring about a dozen pixels across, and the
       same dozen at every zoom. A sphere in world units is a blob once the
       reader zooms to the shadow and invisible when they pull back, and at any
       zoom a filled ball reads as a body in the scene rather than as a mark on
       it. Points with sizeAttenuation off are measured in pixels, so the size
       holds without any per-frame work. */
    var GLYPH = {};
    function glyph(centred) {
      var key = centred ? "centred" : "ring";
      if (GLYPH[key]) return GLYPH[key];
      var cv = document.createElement("canvas");
      cv.width = cv.height = 64;
      var g2 = cv.getContext("2d");
      g2.strokeStyle = "#fff";
      g2.fillStyle = "#fff";
      g2.lineWidth = 6;
      g2.beginPath();
      g2.arc(32, 32, 21, 0, Math.PI * 2);
      g2.stroke();
      if (centred) {
        g2.beginPath();
        g2.arc(32, 32, 6, 0, Math.PI * 2);
        g2.fill();
      }
      var t = new THREE.CanvasTexture(cv);
      t.minFilter = THREE.LinearFilter;
      GLYPH[key] = t;
      return t;
    }
    function marker(p, colour, px, through, order, centred) {
      var g3 = new THREE.BufferGeometry();
      g3.setAttribute("position",
        new THREE.Float32BufferAttribute([p.x, p.y, p.z], 3));
      var pk = colour + "|" + px + "|" + through + "|" + centred;
      if (!PMAT[pk]) {
        PMAT[pk] = new THREE.PointsMaterial({
          color: colour, size: px, sizeAttenuation: false,
          map: glyph(centred),
          transparent: true, opacity: through ? 0.85 : 1,
          depthWrite: false, depthTest: !through
        });
      }
      var mk = new THREE.Points(g3, PMAT[pk]);
      mk.renderOrder = order;
      return mk;
    }
    /* Geometry only: every material in this scene comes from a cache and is
       shared, so it outlives the object and is released once, at teardown. */
    function clear(g) {
      for (var i = g.children.length - 1; i >= 0; i--) {
        var c = g.children[i];
        g.remove(c);
        if (c.geometry) c.geometry.dispose();
      }
    }

    // --- the Earth, north up, so its own graticule needs no turning --------
    var gGlobe = layer("globe", "Earth", null, 0);
    gGlobe.add(new THREE.Mesh(
      new THREE.SphereGeometry(GLOBE_R, 48, 32),
      new THREE.MeshBasicMaterial({ color: pal.fill })));
    gGlobe.add(new THREE.LineSegments(
      new THREE.WireframeGeometry(new THREE.SphereGeometry(1, 24, 16)),
      new THREE.LineBasicMaterial({
        color: pal.line, transparent: true, opacity: 0.45 })));

    var gPole = layer("pole", "Earth's axis", null, 0);
    gPole.add(line([new THREE.Vector3(0, -1.3, 0),
                    new THREE.Vector3(0, 1.3, 0)], pal.dim, true));
    var eqPts = [];
    for (var q = 0; q <= 120; q++) {
      var ea = q / 120 * Math.PI * 2;
      eqPts.push(new THREE.Vector3(
        1.004 * Math.cos(ea), 0, 1.004 * Math.sin(ea)));
    }
    gPole.add(line(eqPts, pal.dim));
    tag(new THREE.Vector3(0, 1.36, 0), "north pole", "pole", 30);
    tag(new THREE.Vector3(1.05, 0, 0), "equator", "pole", 31);

    // --- the fundamental plane, the reference the elements are given in ----
    var gF = layer("fplane", "Fundamental plane", null, 0);
    gF.add(disc(1.28, 0, pal.line, 0.10));
    gF.add(ring(1.28, 0, pal.line));
    tag(at(0, -1.30, 0), "fundamental plane", "fplane", 20);

    // --- everything below is rebuilt when the case changes ----------------
    var SWEEP_VEC = E1.clone().multiplyScalar(2 * SWEEP);
    var gV = layer("vplane", "Vertex plane", null, 0);
    var gCap = layer("cap", "Total region", null, 0);
    var gTrack = layer("track", "Central line", null, 0);
    var gGround = layer("ground", "Shadow on the ground", null, 0);
    var gAxis = layer("axis", "Shadow axis and cones", SWEEP_VEC, 0);
    var gPen = layer("penumbra", "Penumbral cone", SWEEP_VEC, 0, false);

    // Label anchors are mutated in place, so a label follows its feature from
    // one case to the next and from one moment to the next.
    var aUmb = tag(new THREE.Vector3(), function () { return groundKind; },
      "ground", 1);
    var penShown = false;
    var aPen = tag(new THREE.Vector3(), function () {
      return penShown ? "penumbra: the partial zone" : "";
    }, "ground", 2);
    var aVtx = tag(new THREE.Vector3(), "cone vertex", "axis", 3);
    var aTrk = tag(new THREE.Vector3(), function () {
      if (cur.id === "partial") return "";
      if (cur.id === "hybrid") return "total";
      return cur.id === "total" ? "total the whole way" : "annular the whole way";
    }, "track", 4);
    var aTrkL = tag(new THREE.Vector3(), function () {
      return cur.id === "hybrid" ? "annular" : "";
    }, "track", 5);
    var aTrkR = tag(new THREE.Vector3(), function () {
      return cur.id === "hybrid" ? "annular" : "";
    }, "track", 6);
    var aCap = tag(new THREE.Vector3(), function () {
      return onGlobe ? "ground past the vertex" : "";
    }, "cap", 7);
    var onGlobe = false;
    var aV = tag(new THREE.Vector3(), function () {
      return onGlobe ? "vertex plane" : "";
    }, "vplane", 8);
    var aMoon = tag(new THREE.Vector3(), "toward the Moon", "axis", 9);
    labels.sort(function (a, b) { return a.prio - b.prio; });

    function groundHeight(s) {
      var k = 1 - cur.gamma * cur.gamma - s * s;
      return k > 0 ? Math.sqrt(k) : -1;
    }

    /* The shadow on the ground, worked on the sphere rather than in the plane
       of the elements.

       A point of ground is in shadow when its perpendicular distance from the
       shadow axis is less than the cone's radius at that point's height, and
       when it faces the Moon at all. Both tests are exact and neither cares
       whether the axis happens to land on the Earth, which is what makes the
       partial case fall out of the same code as the other three: there the
       axis misses, the umbra reaches nothing, and the penumbra still covers a
       piece of ground bounded partly by its own edge and partly by the
       terminator. */
    var AXIS_A = new THREE.Vector3();

    /* These run some thousands of times per animated frame, so they work in
       scratch vectors. Cloning here was most of the garbage the animation
       produced. */
    var _u = new THREE.Vector3(), _p = new THREE.Vector3();

    function inShadow(p, r0, tanf) {
      if (p.dot(M) < 0) return false;             // the night side
      _u.copy(p).sub(AXIS_A);
      var h = _u.dot(M);
      var perp = Math.sqrt(Math.max(0, _u.lengthSq() - h * h));
      return perp <= Math.abs(r0 - h * tanf);
    }

    function into(out, c, t, alpha) {
      return out.copy(c).multiplyScalar(Math.cos(alpha))
        .addScaledVector(t, Math.sin(alpha));
    }
    function along(c, t, alpha) {
      return into(new THREE.Vector3(), c, t, alpha);
    }

    // How far the shadow reaches from its deepest point in one direction.
    // The regions here are star-shaped about that point, so a bisection is
    // both exact enough and immune to the geometry of the particular case.
    function edgeAlong(c, t, r0, tanf, iters) {
      if (!inShadow(c, r0, tanf)) return 0;
      var lo = 0, hi = Math.PI * 0.75, mid, i;
      for (i = 0; i < iters; i++) {
        mid = (lo + hi) / 2;
        if (inShadow(into(_p, c, t, mid), r0, tanf)) lo = mid; else hi = mid;
      }
      return lo;
    }

    // The deepest point of the shadow: the ground nearest the axis, on the
    // side that faces the Moon.
    function deepest(s) {
      AXIS_A.copy(at(s, cur.gamma, 0));
      var d2 = AXIS_A.lengthSq();
      if (d2 < 1) {
        return AXIS_A.clone()
          .add(M.clone().multiplyScalar(Math.sqrt(1 - d2))).normalize();
      }
      // The axis misses: the nearest ground lies on the terminator, so step a
      // little onto the lit side or every ray out of it leaves at once.
      return AXIS_A.clone().normalize()
        .add(M.clone().multiplyScalar(0.03)).normalize();
    }

    /* The region as a surface, not an outline. Rings of vertices walk out from
       the deepest point along great circles, so the patch hugs the globe
       instead of cutting a chord through it, which for a penumbra half an
       Earth radius wide would sink it out of sight. */
    function region(c, r0, tanf, n, rings, colour, opacity, order, iters) {
      var t1 = Math.abs(c.y) < 0.9
        ? new THREE.Vector3(0, 1, 0).cross(c).normalize()
        : new THREE.Vector3(1, 0, 0).cross(c).normalize();
      var t2 = new THREE.Vector3().crossVectors(c, t1).normalize();
      var alphas = [], rims = [], i, j, any = false;
      for (i = 0; i < n; i++) {
        var th = i / n * Math.PI * 2;
        var t = t1.clone().multiplyScalar(Math.cos(th))
          .add(t2.clone().multiplyScalar(Math.sin(th))).normalize();
        var a = edgeAlong(c, t, r0, tanf, iters);
        if (a > 1e-5) any = true;
        alphas.push(a);
        rims.push(t);
      }
      if (!any) return null;

      var pos = [], idx = [];
      for (j = 0; j <= rings; j++) {
        for (i = 0; i < n; i++) {
          into(_p, c, rims[i], alphas[i] * j / rings)
            .normalize().multiplyScalar(LIFT);
          pos.push(_p.x, _p.y, _p.z);
        }
      }
      for (j = 0; j < rings; j++) {
        for (i = 0; i < n; i++) {
          var a0 = j * n + i, b0 = j * n + (i + 1) % n;
          var c0 = (j + 1) * n + i, d0 = (j + 1) * n + (i + 1) % n;
          idx.push(a0, c0, b0, b0, c0, d0);
        }
      }
      var g = new THREE.BufferGeometry();
      g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
      g.setIndex(idx);
      /* The patch lies on the globe. Chords between sampled surface points
         otherwise dip through the sphere and produce a faceted checkerboard
         under depth testing, especially after zooming in. */
      var mesh = new THREE.Mesh(g, surfaceMat(colour, opacity));
      mesh.renderOrder = order;

      /* The edge, drawn only where the shadow is what ends. Where the region
         stops because the ground curved away, the boundary is the terminator,
         not an edge of the shadow, and drawing it as one would claim a limit
         that is not there. */
      var runs = [], run = null, best = -2, anchor = null;
      for (i = 0; i <= n; i++) {
        var k = i % n;
        var pt = into(_p, c, rims[k], alphas[k]).normalize();
        var lit = pt.dot(M) > 0.02 && alphas[k] > 1e-5;
        if (lit) {
          if (!run) { run = []; runs.push(run); }
          run.push(pt.clone().multiplyScalar(LIFT * 1.0004));
          /* Anchor the label inside the region rather than on its edge: an
             edge point of a shadow that grazes the limb lies where the globe
             itself hides it, and the region goes unnamed. */
          if (pt.dot(M) > best) {
            best = pt.dot(M);
            anchor = along(c, rims[k], alphas[k] * 0.55).normalize();
          }
        } else {
          run = null;
        }
      }
      return { mesh: mesh, runs: runs, anchor: anchor };
    }

    // Updated as the shadow moves, so "Zoom to the shadow" goes to where the
    // shadow is now rather than to where it was for one case.
    var FOCUS_AT = new THREE.Vector3(1, 0, 0);
    var lastS = null;

    function drawGround(s) {
      if (lastS !== null && Math.abs(s - lastS) < 2e-4) return;
      lastS = s;
      clear(gGround);

      var c = deepest(s);
      FOCUS_AT.copy(c);

      // --- the penumbra: the whole partial zone -------------------------
      var pen = region(c, L1, TAN_F1, 108, 10, pal.dim, 0.14, 1, 12);
      if (pen) {
        gGround.add(pen.mesh);
        pen.runs.forEach(function (r) {
          if (r.length > 1) gGround.add(over(line(r, pal.dim), 2));
        });
        aPen.copy((pen.anchor || c).clone().multiplyScalar(1.01));
        penShown = true;
      } else {
        penShown = false;
      }

      // --- the umbra or antumbra: the same cone, met by the same ground --
      var h = groundHeight(s);
      if (h < 0) {
        groundKind = "";
        aUmb.set(0, -9, 0);
        return;
      }
      var l2 = cur.u - h * TAN_F2;           // signed: negative is the umbra
      var dark = l2 < 0 ? pal.ink : pal.accent;   // umbra ink, antumbra brown
      var um = region(c, cur.u, TAN_F2, 96, 4, dark, l2 < 0 ? 0.8 : 0.5, 4, 18);
      if (um) {
        gGround.add(um.mesh);
        um.runs.forEach(function (r) {
          if (r.length > 1) gGround.add(over(line(r, dark), 5));
        });
      }
      /* The stretch of axis between the ground and the vertex: the very
         quantity the sentence under the figure quotes. Drawn through whatever
         stands in front of it, because for a total eclipse it runs clean
         through the planet. */
      gGround.add(over(line([at(s, cur.gamma, h), at(s, cur.gamma, ZV)],
        pal.accent2, true, true), 6));
      groundKind = l2 < 0 ? "umbra on the ground" : "antumbra on the ground";
      aUmb.copy(c.clone().multiplyScalar(1.004));
    }

    function build(id) {
      for (var i = 0; i < TYPES.length; i++) {
        if (TYPES[i].id === id) cur = TYPES[i];
      }
      ZV = cur.u / TAN_F2;
      var reach = 1 - cur.gamma * cur.gamma;
      YT = reach - ZV * ZV > 0 ? Math.sqrt(reach - ZV * ZV) : 0;
      clear(gV); clear(gCap); clear(gTrack); clear(gAxis); clear(gPen);
      lastS = null;

      /* The vertex plane is drawn as a plane only where it cuts the globe,
         which is where it divides the ground into total and annular. For an
         annular or a total eclipse it lies clear of the Earth entirely, and a
         disc floating a couple of radii out in space reads as an object in
         the scene, dwarfs the Earth and wrecks the framing while saying
         nothing the vertex track does not already say. */
      onGlobe = Math.abs(ZV) < 1;
      if (onGlobe) {
        gV.add(disc(1.12, ZV, pal.accent2, 0.16));
        gV.add(ring(1.12, ZV, pal.accent2, true));
        gV.add(ring(Math.sqrt(1 - ZV * ZV) * 1.004, ZV, pal.accent2));
        aV.copy(at(0, -1.14, ZV));
      }
      // The track the vertex itself takes stays in every case: it is what the
      // ground is being compared against.
      gV.add(line([at(-SWEEP, cur.gamma, ZV), at(SWEEP, cur.gamma, ZV)],
        pal.accent2, true, true));

      // the cap of ground that reaches past the vertex. For a partial the
      // region exists geometrically but no cone ever reaches it, and drawing
      // it would promise a totality that never happens.
      if (onGlobe && cur.gamma < 1) {
        /* Just under the ground marks (LIFT), not above them: a cap drawn
           further out is drawn over the very shadow it is there to explain. */
        var cap = new THREE.Mesh(
          new THREE.SphereGeometry(1.0003, 64, 28, 0, Math.PI * 2, 0,
            Math.acos(Math.max(-1, ZV))),
          surfaceMat(pal.accent2, 0.19));
        cap.quaternion.copy(Q_Y);
        cap.renderOrder = 3;
        gCap.add(cap);
      }
      aCap.copy(M.clone().multiplyScalar(1.09));

      // the track the shadow centre takes across the ground
      function trackPoint(s) {
        return at(s, cur.gamma, Math.max(groundHeight(s), 0))
          .multiplyScalar(LIFT * 1.0006);
      }
      function trackSeg(a, b, colour, dashed) {
        var pts = [];
        for (var i = 0; i <= 72; i++) pts.push(trackPoint(a + (b - a) * i / 72));
        return line(pts, colour, dashed);
      }
      if (cur.gamma < 1) {
        if (cur.id === "hybrid" && YT > 0 && YT < SWEEP) {
          gTrack.add(trackSeg(-SWEEP, -YT, pal.accent, true));
          gTrack.add(trackSeg(-YT, YT, pal.ink, false));
          gTrack.add(trackSeg(YT, SWEEP, pal.accent, true));
          [-YT, YT].forEach(function (sx) {
            gTrack.add(marker(trackPoint(sx), pal.accent2, 10, false, 3));
          });
          aTrkL.copy(trackPoint(-0.86));
          aTrkR.copy(trackPoint(0.86));
        } else if (cur.id === "total") {
          gTrack.add(trackSeg(-SWEEP, SWEEP, pal.ink, false));
        } else {
          gTrack.add(trackSeg(-SWEEP, SWEEP, pal.accent, true));
        }
        aTrk.copy(trackPoint(0));
      } else {
        aTrk.set(0, -9, 0);
        aTrkL.set(0, -9, 0);
        aTrkR.set(0, -9, 0);
      }

      // the axis, its two cones, and the vertex between them
      var x0 = -SWEEP;
      var top = ZV + UMBRA_HALF_SPAN;
      var bot = ZV - UMBRA_HALF_SPAN;
      function cone(rTop, rBottom, hh, hc, colour, opacity) {
        var mesh = new THREE.Mesh(
          new THREE.CylinderGeometry(rTop, rBottom, hh, 32, 1, true),
          fillMat(colour, opacity));
        mesh.quaternion.copy(Q_Y);
        mesh.position.copy(at(x0, cur.gamma, hc));
        return mesh;
      }
      gAxis.add(line([at(x0, cur.gamma, bot), at(x0, cur.gamma, top)],
        pal.ink));
      // Above the vertex the cone converges as the umbra; below it the same
      // two surfaces open out again as the antumbra.
      gAxis.add(cone(Math.abs(cur.u - top * TAN_F2), 0,
        top - ZV, (top + ZV) / 2, pal.ink, 0.4));
      gAxis.add(cone(0, Math.abs(cur.u - bot * TAN_F2),
        ZV - bot, (ZV + bot) / 2, pal.ink, 0.4));
      // Drawn through the globe: for a total eclipse the vertex lies beyond
      // the far surface, and a mark that vanishes exactly when it matters is
      // no mark at all.
      gAxis.add(marker(at(x0, cur.gamma, ZV), pal.accent2, 13, true, 6, true));
      aVtx.copy(at(x0, cur.gamma, ZV));
      aMoon.copy(at(x0, cur.gamma, top + 0.07));

      var pcone = new THREE.Mesh(
        new THREE.CylinderGeometry(
          L1 - PENUMBRA_TOP * TAN_F1,
          L1 - PENUMBRA_BOTTOM * TAN_F1,
          PENUMBRA_TOP - PENUMBRA_BOTTOM, 48, 1, true),
        fillMat(pal.dim, 0.13));
      pcone.quaternion.copy(Q_Y);
      pcone.position.copy(at(
        x0, cur.gamma, (PENUMBRA_TOP + PENUMBRA_BOTTOM) / 2));
      gPen.add(pcone);

      drawGround(x0);
    }

    function say(s) {
      var h = groundHeight(s);
      if (h < 0) {
        return "The axis passes " + (cur.gamma - 1).toFixed(3) +
          " Earth radii clear of the Earth, so neither the umbra nor the " +
          "antumbra reaches the ground anywhere. Only the penumbra lands, " +
          "and the eclipse is partial wherever it is seen at all.";
      }
      var l2 = cur.u - h * TAN_F2;
      var wide = (2 * Math.abs(l2) * RE_KM).toFixed(0);
      if (l2 < 0) {
        return "Here the ground stands " + (h - ZV).toFixed(3) +
          " Earth radii past the vertex, so the cone has not closed yet and " +
          "the umbra itself lands: total, in a shadow " + wide + " km across.";
      }
      return "Here the vertex falls " + (ZV - h).toFixed(3) +
        " Earth radii short of the ground, so the cone has closed and " +
        "reopened before reaching it: the antumbra lands and the eclipse is " +
        "annular, in a ring shadow " + wide + " km across.";
    }

    build("hybrid");

    return {
      layers: layers,
      labels: labels,
      sliderLabel: "Along the path",
      globeRadius: GLOBE_R,
      /* Opens about halfway between the shadow axis and the path: any nearer
         the axis and the cones are seen end-on as circles, any nearer the
         path and the path itself runs into the screen. North stays up, so a
         drag left or right turns the Earth on its own axis and carries the
         view east and west. */
      home: { theta: 2.46, phi: 1.20, r: 5.8 },
      variants: {
        label: "Type",
        initial: "hybrid",
        options: TYPES.map(function (t) { return { id: t.id, label: t.label }; }),
        select: function (id) { build(id); }
      },
      onProgress: function (t) {
        var s = -SWEEP + 2 * SWEEP * t;
        drawGround(s);
        return say(s);
      },
      focus: { at: FOCUS_AT, radius: 0.32, label: "Zoom to the shadow" },
      note: "Drawn in Earth radii, with tan f2 = 0.004645 and a penumbral " +
            "radius of 0.536 on the fundamental plane. North is up, and the " +
            "shadow axis stands at a declination of 15 degrees, so it meets " +
            "the Earth's axis at 75 degrees rather than along it. Nothing is " +
            "exaggerated. The umbra on the ground is the true intersection of the " +
            "cone with the globe, so at this scale it is a few tens of " +
            "kilometres across against a planet 12756 km wide: a dot the " +
            "label points at. Zoom to the shadow to see its shape meet the " +
            "cone that casts it. Pick a type, then carry the axis along " +
            "the path and read the line above."
    };
  };

  // ------------------------------------------------------------- the viewer
  function activate(host, name, button) {
    var scene, renderer, camera, controls, frame, ro, built, root;
    var explode = 0, spinning = null, lastTick = 0;
    /* How long the whole travel takes, in milliseconds. Advancing by a fixed
       amount per frame made it twice as fast on a 120 Hz display as on a
       60 Hz one, which for a shadow crossing a path is not cosmetic. */
    var SWEEP_MS = 4200;
    var dirty = true;
    function invalidate() { dirty = true; }

    var stage = document.createElement("div");
    stage.className = "fig3d-stage";
    var canvas = document.createElement("canvas");
    stage.appendChild(canvas);
    var layerEl = document.createElement("div");
    layerEl.className = "fig3d-labels";
    stage.appendChild(layerEl);

    var THREE = window.THREE;
    var pal = palette();

    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(38, 16 / 9, 0.01, 100);
      root = new THREE.Group();
      scene.add(root);
      built = SCENES[name](THREE, root, pal);
    } catch (e) {
      /* Falling back to the diagram is right, but say which scene and why.
         A scene that throws used to make the button flash "Loading..." and
         come back with nothing in the console, which costs an afternoon.
         This message once sat on the WebGL probe's catch instead, where the
         scene's name is not even in scope: a replacement that matched the
         first `catch` in the file rather than the intended one. */
      if (window.console && console.error) {
        console.error("3D scene '" + name + "' failed to build:", e);
      }
      if (scene) {
        try {
          scene.traverse(function (o) {
            if (o.geometry) o.geometry.dispose();
            dropMaterial(o.material);
          });
        } catch (cleanupError) { /* release the WebGL context below */ }
      }
      if (renderer) {
        try { renderer.forceContextLoss(); } catch (contextError) { /* unsupported */ }
        try { renderer.dispose(); } catch (disposeError) { /* partly initialised */ }
      }
      return false;
    }

    var maxOrder = built.layers.reduce(function (m, l) {
      return Math.max(m, l.order);
    }, 0);
    // Fixed for the life of the viewer; it used to be rebuilt every frame.
    var byId = {};
    built.layers.forEach(function (l) { byId[l.id] = l; });

    /* Material colours are values copied from CSS when the scene is built.
       Re-read and replace them when the page or system theme changes, rather
       than leaving an open viewer in the old theme. */
    function refreshPalette() {
      var next = palette();
      var replacements = {};
      Object.keys(pal).forEach(function (key) {
        try {
          replacements[new THREE.Color(pal[key]).getHexString()] = next[key];
        } catch (e) { /* a non-colour custom property is not a material */ }
      });
      scene.traverse(function (o) {
        var materials = o.material && o.material.length ? o.material : [o.material];
        materials.forEach(function (m) {
          if (!m || !m.color) return;
          var replacement = replacements[m.color.getHexString()];
          if (replacement) m.color.set(replacement);
        });
      });
      pal = next;
      invalidate();
    }

    // ---- controls -------------------------------------------------------
    var panel = document.createElement("div");
    panel.className = "fig3d-panel";

    var chips = document.createElement("div");
    chips.className = "fig3d-layers";
    built.layers.forEach(function (l) {
      var id = "l3d-" + name + "-" + l.id;
      var wrap = document.createElement("label");
      wrap.className = "fig3d-chip";
      wrap.innerHTML = '<input type="checkbox" id="' + id + '"' +
        (l.on ? " checked" : "") + "> <span></span>";
      wrap.querySelector("span").textContent = l.label;
      wrap.querySelector("input").addEventListener("change", function (e) {
        l.on = e.target.checked;
        l.group.visible = l.on;
        invalidate();
      });
      // Remember what the scene asked for, so Reset restores the scene's own
      // defaults rather than switching every layer on.
      l.def = l.on;
      l.group.visible = l.on;
      chips.appendChild(wrap);
    });
    panel.appendChild(chips);

    // Labels are a layer too: the quickest way to see the geometry is to
    // take them away.
    var showLabels = true;
    var labelChip = document.createElement("label");
    labelChip.className = "fig3d-chip";
    labelChip.innerHTML = '<input type="checkbox" checked> <span>Labels</span>';
    labelChip.querySelector("input").addEventListener("change", function (e) {
      showLabels = e.target.checked;
      invalidate();
    });
    chips.appendChild(labelChip);

    var row = document.createElement("div");
    row.className = "fig3d-bar";
    row.innerHTML =
      '<label class="fig3d-slider">' + (built.sliderLabel || "Take apart") + " " +
      '<input type="range" min="0" max="100" value="0" step="1"></label>' +
      '<button type="button" class="fig3d-btn" data-act="anim">Animate</button>' +
      '<button type="button" class="fig3d-btn" data-act="focus" hidden></button>' +
      '<button type="button" class="fig3d-btn" data-act="full" hidden>Full screen</button>' +
      '<button type="button" class="fig3d-btn" data-act="reset">Reset</button>' +
      '<button type="button" class="fig3d-btn" data-act="back">Back to diagram</button>';
    panel.appendChild(row);

    var slider = row.querySelector("input[type=range]");
    var animBtn = row.querySelector('[data-act="anim"]');
    function setAnimLabel() {
      if (!animBtn) return;
      animBtn.textContent = spinning !== null ? "Stop" : "Animate";
      animBtn.setAttribute("aria-pressed", spinning !== null ? "true" : "false");
    }
    function stopAnim() {
      spinning = null;
      lastTick = 0;
      setAnimLabel();
    }
    setAnimLabel();
    slider.addEventListener("input", function () {
      stopAnim();
      explode = slider.value / 100;
      invalidate();
    });

    if (built.variants) {
      var vrow = document.createElement("div");
      vrow.className = "fig3d-variants";
      var vlab = document.createElement("span");
      vlab.className = "fig3d-vlabel";
      vlab.textContent = built.variants.label || "Case";
      vrow.appendChild(vlab);
      built.variants.options.forEach(function (o) {
        var vb = document.createElement("button");
        vb.type = "button";
        vb.className = "fig3d-btn fig3d-variant";
        vb.setAttribute("aria-pressed",
          o.id === built.variants.initial ? "true" : "false");
        vb.textContent = o.label;
        vb.addEventListener("click", function () {
          Array.prototype.forEach.call(
            vrow.querySelectorAll(".fig3d-variant"), function (x) {
              x.setAttribute("aria-pressed", "false");
            });
          vb.setAttribute("aria-pressed", "true");
          stopAnim();
          explode = 0;
          slider.value = 0;
          built.variants.select(o.id);
          measure();
          invalidate();
        });
        vrow.appendChild(vb);
      });
      panel.insertBefore(vrow, panel.firstChild);
    }

    if (built.focus) {
      var fb = row.querySelector('[data-act="focus"]');
      fb.textContent = built.focus.label || "Zoom in";
      fb.hidden = false;
    }

    // Everything the viewer owns lives in one element, so full screen can
    // take the controls with it.
    var viewer = document.createElement("div");
    viewer.className = "fig3d-viewer";
    viewer.appendChild(stage);
    host.appendChild(viewer);
    host.classList.add("is3d");

    /* A line the scene rewrites as the reader moves the slider. A picture can
       show a quantity crossing a threshold; only words can say which side it
       is on now, and without that a reader is left guessing what they are
       looking at. */
    var readout = null;
    if (built.onProgress) {
      readout = document.createElement("p");
      readout.className = "fig3d-readout";
      viewer.appendChild(readout);
    }

    var tags = (built.labels || []).map(function (l) {
      var el = document.createElement("span");
      el.className = "fig3d-tag";
      el.textContent = typeof l.text === "function" ? l.text() : l.text;
      layerEl.appendChild(el);
      return { el: el, at: l.at, layer: l.layer, text: l.text, w: 0, h: 0 };
    });
    function measureOne(t) {
      var shown = t.el.style.display;
      t.el.style.display = "block";
      t.w = t.el.offsetWidth;
      t.h = t.el.offsetHeight;
      t.el.style.display = shown;
    }
    function measure() { tags.forEach(measureOne); }
    measure();

    if (built.note) {
      var note = document.createElement("p");
      note.className = "fig3d-note";
      note.textContent = built.note;
      viewer.appendChild(note);
    }

    var hint = document.createElement("p");
    hint.className = "fig3d-hint";
    hint.textContent = "Drag to orbit, scroll to zoom.";
    viewer.appendChild(hint);
    viewer.appendChild(panel);

    function isFull() { return document.fullscreenElement === viewer; }

    // Read once per resize rather than once per frame: the label pass writes
    // styles, so reading a layout property in the loop forces a reflow.
    var stageW = 0, stageH = 0;

    function size() {
      var w = stage.clientWidth || 640;
      var h;
      if (isFull()) {
        // Give the canvas whatever the controls do not need.
        h = Math.max(200, viewer.clientHeight - panel.offsetHeight -
          hint.offsetHeight - (readout ? readout.offsetHeight : 0) - 40);
      } else {
        h = Math.round(w * 9 / 16);
      }
      /* The observer watches this element, so writing a height it already
         has feeds the observer its own change and the browser reports an
         undelivered-notification loop. */
      if (stage.style.height !== h + "px") stage.style.height = h + "px";
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.setSize(w, h, false);
      camera.aspect = w / (h || 1);
      camera.updateProjectionMatrix();
      stageW = w;
      stageH = h;
      measure();
      invalidate();
    }

    if (document.fullscreenEnabled) {
      row.querySelector('[data-act="full"]').hidden = false;
    }
    var fsTimer = null;
    var onFsChange = function () {
      var b = row.querySelector('[data-act="full"]');
      if (b) b.textContent = isFull() ? "Exit full screen" : "Full screen";
      fsTimer = setTimeout(size, 60);
    };
    document.addEventListener("fullscreenchange", onFsChange);

    controls = Orbit(camera, stage, 5.2, THREE, built.home, invalidate);
    size();

    var themeObserver = null;
    if (window.MutationObserver) {
      themeObserver = new MutationObserver(refreshPalette);
      themeObserver.observe(document.documentElement, {
        attributes: true, attributeFilter: ["data-theme"]
      });
    }
    var schemeQuery = window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)");
    if (schemeQuery) {
      if (schemeQuery.addEventListener) {
        schemeQuery.addEventListener("change", refreshPalette);
      } else if (schemeQuery.addListener) {
        schemeQuery.addListener(refreshPalette);
      }
    }

    function layerOffset(l) {
      // Layers separate in turn as the slider advances, so the assembly comes
      // apart in stages rather than all at once.
      var t = Math.max(0, Math.min(1, explode * (maxOrder + 1) - l.order));
      return l.explode.clone().multiplyScalar(t);
    }

    function draw(ts) {
      frame = requestAnimationFrame(draw);
      if (spinning !== null) {
        // Clamp the step so a tab returning from the background does not jump
        // the whole sweep in one frame.
        var dt = lastTick ? Math.min(ts - lastTick, 100) : 16;
        lastTick = ts || 0;
        explode += spinning * dt / SWEEP_MS;
        if (explode >= 1) { explode = 1; stopAnim(); }
        else if (explode <= 0) { explode = 0; stopAnim(); }
        slider.value = Math.round(explode * 100);
        dirty = true;
      }
      /* A research page may leave two figures open and scroll past them. With
         nothing moving there is nothing to redraw, and a still picture should
         not hold a core and a GPU busy for the life of the page. */
      if (!dirty) return;
      dirty = false;
      if (built.onProgress) {
        var said = built.onProgress(explode);
        if (readout && said != null && said !== readout.textContent) {
          readout.textContent = said;
        }
      }
      built.layers.forEach(function (l) {
        l.group.position.copy(layerOffset(l));
      });
      renderer.render(scene, camera);

      var w = stageW || stage.clientWidth, h = stageH || stage.clientHeight;
      var globeOn = byId.globe && byId.globe.on;
      var globeR2 = (built.globeRadius || 0.995) * (built.globeRadius || 0.995);

      /* Hide a label the globe is standing in front of. Without this the far
         side of the scene writes its labels over the near side. */
      function hidden(world) {
        if (!globeOn) return false;
        var dir = world.clone().sub(camera.position);
        var len = dir.length();
        if (len < 1e-6) return false;
        dir.divideScalar(len);
        var tca = -camera.position.dot(dir);
        if (tca < 0 || tca > len) return false;
        var d2 = camera.position.lengthSq() - tca * tca;
        // Each scene says how big its globe is; 0.99 was a third number that
        // agreed with neither, so a label in the thin band between them was
        // judged visible and then drawn over.
        return d2 < globeR2;
      }

      /* Place labels in priority order and drop any that would land on one
         already placed. A label that covers the drawing is worse than a
         label that is not there, and the reader can switch the rest off. */
      var placed = [];
      tags.forEach(function (t) {
        var l = byId[t.layer];
        if (!showLabels || (l && !l.on)) { t.el.style.display = "none"; return; }
        if (typeof t.text === "function") {
          var txt = t.text();
          if (!txt) { t.el.style.display = "none"; return; }
          if (txt !== t.el.textContent) { t.el.textContent = txt; measureOne(t); }
        }
        var world = t.at.clone();
        if (l) world.add(l.group.position);
        var p = world.clone().project(camera);
        if (p.z >= 1 || Math.abs(p.x) > 1.15 || Math.abs(p.y) > 1.1 ||
            hidden(world)) {
          t.el.style.display = "none";
          return;
        }
        var lx = Math.max(t.w / 2 + 3, Math.min(w - t.w / 2 - 3,
          (p.x * 0.5 + 0.5) * w));
        var ly = Math.max(t.h * 1.6 + 3, Math.min(h - 3,
          (-p.y * 0.5 + 0.5) * h));
        // The label sits above its anchor, per the transform in the CSS.
        var box = {
          l: lx - t.w / 2, r: lx + t.w / 2,
          t: ly - t.h * 1.6, b: ly - t.h * 0.6
        };
        var clash = placed.some(function (q) {
          return !(box.r < q.l || box.l > q.r || box.b < q.t || box.t > q.b);
        });
        if (clash) { t.el.style.display = "none"; return; }
        placed.push(box);
        t.el.style.display = "block";
        t.el.style.left = lx.toFixed(1) + "px";
        t.el.style.top = ly.toFixed(1) + "px";
      });
    }
    draw();

    if (window.ResizeObserver) {
      ro = new ResizeObserver(size);
      ro.observe(stage);
    } else {
      window.addEventListener("resize", size);
    }

    function dropMaterial(m) {
      if (!m) return;
      if (m.length) { for (var i = 0; i < m.length; i++) dropMaterial(m[i]); return; }
      for (var k in m) {
        if (m[k] && m[k].isTexture) m[k].dispose();
      }
      m.dispose();
    }

    /* A browser caps how many WebGL contexts may live at once, and each open
       of a figure makes a new one. Leaving the old one to the garbage
       collector meant that opening and closing figures enough times could
       blank one that had been working. */
    function teardown() {
      if (frame) cancelAnimationFrame(frame);
      if (ro) ro.disconnect(); else window.removeEventListener("resize", size);
      if (fsTimer) clearTimeout(fsTimer);
      document.removeEventListener("fullscreenchange", onFsChange);
      if (themeObserver) themeObserver.disconnect();
      if (schemeQuery) {
        if (schemeQuery.removeEventListener) {
          schemeQuery.removeEventListener("change", refreshPalette);
        } else if (schemeQuery.removeListener) {
          schemeQuery.removeListener(refreshPalette);
        }
      }
      if (isFull() && document.exitFullscreen) {
        document.exitFullscreen().catch(function () { /* already leaving */ });
      }
      try {
        scene.traverse(function (o) {
          if (o.geometry) o.geometry.dispose();
          dropMaterial(o.material);
        });
      } catch (e) { /* a partly built scene is still worth releasing */ }
      try { renderer.forceContextLoss(); } catch (e) { /* not supported */ }
      try { renderer.dispose(); } catch (e) { /* nothing to do */ }
      viewer.remove();
      host.classList.remove("is3d");
    }

    row.addEventListener("click", function (e) {
      var b = e.target.closest("[data-act]");
      if (!b) return;
      var act = b.dataset.act;
      if (act === "anim") {
        if (spinning !== null) stopAnim();
        else {
          spinning = explode >= 1 ? -1 : 1;
          lastTick = 0;
          setAnimLabel();
        }
        invalidate();
      } else if (act === "focus") {
        controls.aim(built.focus.at, built.focus.radius);
      } else if (act === "full") {
        if (isFull()) {
          if (document.exitFullscreen) document.exitFullscreen();
        } else if (viewer.requestFullscreen) {
          viewer.requestFullscreen().catch(function () {
            // Refused, for instance without a user gesture: stay inline.
          });
        }
      } else if (act === "reset") {
        stopAnim();
        explode = 0;
        slider.value = 0;
        controls.reset();
        built.layers.forEach(function (l) {
          var cb = chips.querySelector("#l3d-" + name + "-" + l.id);
          if (cb) { cb.checked = l.on = l.def; l.group.visible = l.on; }
        });
        invalidate();
      } else {
        teardown();
        button.hidden = false;
        button.focus();
      }
    });

    return true;
  }

  // ------------------------------------------------------------- the offers
  hosts.forEach(function (host) {
    var name = host.dataset.scene;
    if (!SCENES[name]) return;

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "fig3d-open";
    btn.textContent = "View in 3D";
    host.appendChild(btn);

    btn.addEventListener("click", function () {
      // Belt as well as braces: never build a second viewer over the first.
      if (host.classList.contains("is3d")) return;
      btn.disabled = true;
      btn.textContent = "Loading…";
      loadThree().then(function () {
        var ok = activate(host, name, btn);
        btn.disabled = false;
        btn.textContent = "View in 3D";
        if (ok) btn.hidden = true;
      }).catch(function () {
        // Offline, blocked, or unsupported: the diagram is still the figure.
        btn.remove();
      });
    });
  });
})();
