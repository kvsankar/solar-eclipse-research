/* The state of each event in the 3D guided scenes.
 *
 * Specification: docs/specs.md, section S3D. Pure functions only: given an
 * event and a slider position t in [0, 1], state() returns where every body
 * is, which part of the shadow the observer (or the darkened body) is in, and
 * what is seen from there. The 3D viewer only draws this state, and the Node
 * tests check it against the geometry module.
 *
 * The scenes are not to scale. Each event's numbers are compressed so every
 * body fits in view, but chosen so that its shadow parts come in the same
 * order as in the real event (S3D-7, S3D-9). Units are arbitrary scene units.
 * The source sits at the origin, the shadow falls along +x, and motion is
 * along +y.
 */
(function (root, factory) {
  "use strict";
  if (typeof module === "object" && module.exports) {
    module.exports = factory(require("./geometry.js"));
  } else {
    root.EclipseScenes = factory(root.EclipseGeometry);
  }
})(typeof self !== "undefined" ? self : this, function (G) {
  "use strict";

  /* For each event: the source (radius Rs; a point source has none), the
     blocking body (radius Rb, distance D from the source), and the observer
     or darkened body (distance d behind the blocking body, radius Rr when it
     is a body). The moving body travels from y = -B to y = +B. In the
     hidden case the observer stands on a world, or rides in a craft, of
     radius Rw named by world (the Earth unless stated). */
  var EVENTS = {
    "solar-eclipse": {
      label: "Solar eclipse", case: "hidden", source: "disc",
      names: ["the Sun", "the Moon", "on the Earth"], possessive: "the Moon's",
      Rs: 2.5, Rb: 0.6, D: 12, d: 2.6, Rr: 1.3, B: 1.4, moving: "Blocking body"
    },
    "annular-solar-eclipse": {
      label: "Annular solar eclipse", case: "hidden", source: "disc",
      names: ["the Sun", "the Moon", "on the Earth"], possessive: "the Moon's",
      Rs: 2.5, Rb: 0.6, D: 12, d: 5.2, Rr: 1.3, B: 1.8, moving: "Blocking body"
    },
    "venus-transit": {
      label: "Transit of Venus", case: "hidden", source: "disc",
      names: ["the Sun", "Venus", "on the Earth"], possessive: "Venus's",
      Rs: 2.5, Rb: 0.15, D: 9, d: 6, Rr: 1.3, B: 1.5, moving: "Blocking body"
    },
    "star-occultation": {
      label: "Lunar occultation of a star", case: "hidden", source: "point",
      names: ["a star", "the Moon", "on the Earth"], possessive: "the Moon's",
      Rb: 0.6, D: 12, d: 3, Rr: 1.3, B: 0.8, moving: "Blocking body"
    },
    "asteroid-occultation": {
      label: "Occultation by an asteroid", case: "hidden", source: "point",
      names: ["a star", "an asteroid", "on the Earth"], possessive: "the asteroid's",
      Rb: 0.25, D: 12, d: 4, Rr: 1.3, B: 0.4, moving: "Blocking body"
    },
    // The Artemis II crew watched from the Orion spacecraft, close behind the
    // Moon, where the Moon looks far larger than the Sun. The spacecraft's
    // own motion carried them through the shadow.
    "artemis-eclipse": {
      label: "Solar eclipse from Artemis II", case: "hidden", source: "disc",
      names: ["the Sun", "the Moon", "in the Orion spacecraft"], possessive: "the Moon's",
      Rs: 2.5, Rb: 0.6, D: 12, d: 1.0, Rr: 0.14, B: 1.2, moving: "Observer",
      world: "the Orion spacecraft"
    },
    // Phobos is too small to cover the Sun seen from Mars: the observer
    // stands in its antumbra.
    "phobos-transit": {
      label: "Phobos from Mars", case: "hidden", source: "disc",
      names: ["the Sun", "Phobos", "on Mars"], possessive: "Phobos's",
      Rs: 2.5, Rb: 0.2, D: 12, d: 1.2, Rr: 1.0, B: 0.6, moving: "Blocking body",
      world: "Mars"
    },
    "lunar-eclipse": {
      label: "Lunar eclipse", case: "darkened", source: "disc",
      names: ["the Sun", "the Earth", "the Moon"], possessive: "the Earth's",
      Rs: 2.5, Rb: 1.2, D: 12, d: 3, Rr: 0.33, B: 2.8, moving: "Darkened body"
    },
    "satellite-eclipse": {
      label: "Eclipse of a satellite", case: "darkened", source: "disc",
      names: ["the Sun", "Jupiter", "Io"], possessive: "Jupiter's",
      Rs: 2.5, Rb: 1.6, D: 14, d: 3, Rr: 0.2, B: 3.3, moving: "Darkened body"
    },
    "shadow-transit": {
      label: "Shadow transit", case: "darkened", source: "disc",
      names: ["the Sun", "Io", "Jupiter"], possessive: "Io's",
      Rs: 2.5, Rb: 0.45, D: 12, d: 2.4, Rr: 1.4, B: 1.5, moving: "Blocking body"
    }
  };

  var SCENES = {
    "hidden-cases": {
      events: ["solar-eclipse", "annular-solar-eclipse", "venus-transit",
        "star-occultation", "asteroid-occultation", "artemis-eclipse",
        "phobos-transit"],
      note: "Not to scale: sizes and distances are compressed so every body " +
        "fits in view, but each event's shadow parts come in the real order. " +
        "Pick an event, then move the blocking body across the line from the " +
        "observer to the source and read the line below."
    },
    "darkened-cases": {
      events: ["lunar-eclipse", "satellite-eclipse", "shadow-transit"],
      note: "Not to scale: sizes and distances are compressed so every body " +
        "fits in view, but each event's shadow parts come in the real order. " +
        "Pick an event, then move it along its path and read the line below."
    }
  };

  // A distance that stands for "at infinity" for a point source, in scene
  // units, used only to place the star in the drawing.
  var STAR_DISTANCE = 18;

  function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function norm(a) { return Math.sqrt(dot(a, a)); }
  function scale(a, k) { return [a[0] * k, a[1] * k, a[2] * k]; }

  function percent(f) {
    var p = Math.round(f * 100);
    if (p < 1) return "less than 1%";
    if (p > 99) return "more than 99%";
    return p + "%";
  }

  // Where the line from the source's centre through the blocking body's
  // centre first meets the darkened body's surface, or null if it misses.
  function groundPoint(src, blk, centre, radius) {
    var dir = sub(blk, src);
    dir = scale(dir, 1 / norm(dir));
    var oc = sub(src, centre);
    var b = dot(oc, dir);
    var c = dot(oc, oc) - radius * radius;
    var disc = b * b - c;
    if (disc < 0) return null;
    var t = -b - Math.sqrt(disc);
    return [src[0] + dir[0] * t, src[1] + dir[1] * t, src[2] + dir[2] * t];
  }

  // The shadow part at point p and the view of the source from p.
  function circumstances(e, src, blk, p) {
    var axisVec = sub(blk, src);
    var D = norm(axisVec);
    var axis = scale(axisVec, 1 / D);
    var rel = sub(p, blk);
    var behind = dot(rel, axis);
    var fromAxis = norm(sub(rel, scale(axis, behind)));
    var part = G.region(e.Rs, e.Rb, D, behind, fromAxis);
    var toSrc = sub(src, p);
    var toBlk = sub(blk, p);
    var rs = Math.asin(e.Rs / norm(toSrc));
    var ro = Math.asin(e.Rb / norm(toBlk));
    var sep = Math.acos(Math.min(1, dot(toSrc, toBlk) / (norm(toSrc) * norm(toBlk))));
    return { part: part, view: G.discView(rs, ro, sep) };
  }

  function hiddenText(e, part, view) {
    var where = part === "outside"
      ? "The observer is outside " + e.possessive + " shadow"
      : "The observer is in " + e.possessive + " " + part;
    var src = e.names[0];
    var Src = src.charAt(0).toUpperCase() + src.slice(1);
    if (view.kind === "none") return where + ": no eclipse, " + src + " is in full view.";
    if (view.kind === "total") return where + ": " + src + " is totally hidden.";
    if (e.Rb < 0.2) {
      // A transit: the planet is too small to cover the Sun.
      return where + ": " + e.names[1] + " is " +
        (view.kind === "annular" ? "a dark dot on " : "on the edge of ") + src +
        ", covering " + percent(view.covered) + " of " + src + "'s disc.";
    }
    if (view.kind === "annular") {
      return where + ": an annular eclipse, " + percent(view.covered) + " of " +
        src + "'s disc covered and a ring of it left around " + e.names[1] + ".";
    }
    return where + ": a partial eclipse, " + percent(view.covered) + " of " +
      Src.replace(/^The /, "the ") + "'s disc covered.";
  }

  function darkenedText(e, part, view) {
    var body = e.names[2];
    var Body = body.charAt(0).toUpperCase() + body.slice(1);
    if (part === "outside") return Body + " is outside " + e.possessive + " shadow: fully lit.";
    if (part === "umbra") {
      return Body + " is in " + e.possessive + " umbra: no direct sunlight reaches its centre.";
    }
    return Body + " is in " + e.possessive + " penumbra: from its centre, " +
      percent(view.covered) + " of the Sun's disc is hidden, so it dims.";
  }

  // Where the Earth is drawn for Jupiter's events: off the shadow, between
  // the Sun and Jupiter and below the line, at a distance not to scale.
  var FAR_EARTH = { dx: -5, y: -3.4, radius: 0.8 };

  // Signed angle at p from the direction of a to the direction of b, in the
  // plane of the scene, where every body lies.
  function signedAngle(p, a, b) {
    var aa = Math.atan2(a[1] - p[1], a[0] - p[0]);
    var bb = Math.atan2(b[1] - p[1], b[0] - p[0]);
    var d = bb - aa;
    while (d > Math.PI) d -= 2 * Math.PI;
    while (d < -Math.PI) d += 2 * Math.PI;
    return d;
  }

  function onSurface(centre, radius, toward) {
    var dir = sub(toward, centre);
    return sub(centre, scale(dir, -radius / norm(dir)));
  }

  function state(id, t) {
    var e = EVENTS[id];
    if (!e) throw new Error("unknown event: " + id);
    var y = -e.B + 2 * e.B * t;
    var src = e.source === "point" ? [-STAR_DISTANCE, 0, 0] : [0, 0, 0];
    var blk = [e.D, e.moving === "Blocking body" ? y : 0, 0];
    var rcv = [e.D + e.d, e.moving === "Blocking body" ? 0 : y, 0];
    var bodies, world;

    if (e.case === "hidden") {
      // The observer stands on the near side of their world, facing the
      // blocking body along the line from the source.
      world = { name: e.world || "the Earth", centre: [rcv[0] + e.Rr, rcv[1], 0], radius: e.Rr };
      bodies = [
        { role: "Light source", name: e.names[0], position: src, radius: e.source === "point" ? 0 : e.Rs },
        { role: "Blocking body", name: e.names[1], position: blk, radius: e.Rb },
        { role: "Observer", name: e.names[2], position: rcv, radius: 0 }
      ];
    } else {
      // Someone on the Earth watches. For a lunar eclipse the Earth is the
      // blocking body and they stand on its night side, facing the Moon.
      var watched = id === "shadow-transit" ? rcv : blk;
      world = e.Rb && id === "lunar-eclipse"
        ? { name: "the Earth", centre: blk, radius: e.Rb }
        : { name: "the Earth", centre: [e.D + FAR_EARTH.dx, FAR_EARTH.y, 0], radius: FAR_EARTH.radius };
      var obs = id === "lunar-eclipse"
        ? [blk[0] + e.Rb, 0, 0]
        : onSurface(world.centre, world.radius, watched);
      bodies = [
        { role: "Light source", name: e.names[0], position: src, radius: e.Rs },
        { role: "Blocking body", name: e.names[1], position: blk, radius: e.Rb },
        { role: "Darkened body", name: e.names[2], position: rcv, radius: e.Rr },
        { role: "Observer", name: "on the Earth", position: obs, radius: 0 }
      ];
    }
    var out = {
      event: id, label: e.label, case: e.case, source: e.source,
      moving: e.moving, bodies: bodies, ground: null, world: world,
      umbraLength: e.source === "disc" ? G.umbraLength(e.Rs, e.Rb, e.D) : null
    };

    if (e.source === "point") {
      // A star at infinity: the shadow is a cylinder along +x through the
      // blocking body (GEO-4).
      var rel = sub(rcv, blk);
      var behind = rel[0];
      var perp = Math.sqrt(rel[1] * rel[1] + rel[2] * rel[2]);
      var s = Math.asin(perp / norm(rel));
      var ro = Math.asin(e.Rb / norm(rel));
      var hidden = behind > 0 && G.pointHidden(s, ro);
      out.part = hidden ? "hidden" : "outside";
      out.view = { hidden: hidden };
      // The star lies along -x from everywhere.
      out.sees = { kind: "star", blockerRadius: ro,
        offset: signedAngle(rcv, [rcv[0] - 1, rcv[1], 0], blk) };
      out.text = hidden
        ? "The observer is in " + e.possessive + " shadow in starlight: the star is hidden."
        : "The observer is outside " + e.possessive + " shadow in starlight: the star is visible.";
      return out;
    }

    if (id === "shadow-transit") {
      var g = groundPoint(src, blk, rcv, e.Rr);
      out.sees = { kind: "planet", name: e.names[2], spot: g ? (g[1] - rcv[1]) / e.Rr : null };
      if (!g) {
        out.part = "outside";
        out.view = { kind: "none", covered: 0 };
        out.text = e.possessive.charAt(0).toUpperCase() + e.possessive.slice(1) +
          " shadow misses " + e.names[2] + ".";
        return out;
      }
      out.ground = g;
      var cg = circumstances(e, src, blk, g);
      out.part = cg.part;
      out.view = cg.view;
      out.text = e.possessive.charAt(0).toUpperCase() + e.possessive.slice(1) +
        " shadow falls on " + e.names[2] + "'s cloud tops: under it the Sun is " +
        (cg.view.kind === "total" ? "totally hidden." : percent(cg.view.covered) + " hidden.");
      return out;
    }

    var c = circumstances(e, src, blk, rcv);
    out.part = c.part;
    out.view = c.view;
    if (e.case === "hidden") {
      out.sees = { kind: "disc",
        sourceRadius: Math.asin(e.Rs / norm(sub(src, rcv))),
        blockerRadius: Math.asin(e.Rb / norm(sub(blk, rcv))),
        offset: signedAngle(rcv, src, blk) };
      out.text = hiddenText(e, c.part, c.view);
    } else {
      out.sees = { kind: "body", name: e.names[2],
        dimmed: c.part === "umbra" ? 1 : c.view.covered,
        tint: id === "lunar-eclipse" ? "copper" : "dark" };
      out.text = darkenedText(e, c.part, c.view);
    }
    return out;
  }

  return { events: EVENTS, scenes: SCENES, state: state };
});
