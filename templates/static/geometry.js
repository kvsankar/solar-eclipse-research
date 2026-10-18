/* Shadow and occultation geometry shared by the 3D scenes and the explorer.
 *
 * Specification: docs/specs.md, section GEO. Pure functions only: no page
 * access and no dependency, so the same file loads as a plain script from
 * file:// (as the global EclipseGeometry) and as a module under Node for tests.
 *
 * Lengths are in any one unit (km in the tests). Angles are radians.
 */
(function (root, factory) {
  "use strict";
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.EclipseGeometry = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // GEO-1. Cone angles from the source and body radii and their separation:
  // sin f_u = (R_s - R_b) / D for the umbra, sin f_p = (R_s + R_b) / D for the
  // penumbra. At distance x behind the body's centre the radii are
  // R_b sec f -/+ x tan f, the form of the Besselian l1 and l2.
  function shadowRadii(sourceRadius, bodyRadius, distance, behind) {
    const fu = Math.asin((sourceRadius - bodyRadius) / distance);
    const fp = Math.asin((sourceRadius + bodyRadius) / distance);
    const umbra = bodyRadius / Math.cos(fu) - behind * Math.tan(fu);
    const penumbra = bodyRadius / Math.cos(fp) + behind * Math.tan(fp);
    return { umbra: Math.abs(umbra), antumbra: umbra < 0, penumbra: penumbra };
  }

  // Distance from the body's centre to the umbral vertex: R_b / sin f_u.
  function umbraLength(sourceRadius, bodyRadius, distance) {
    return bodyRadius / ((sourceRadius - bodyRadius) / distance);
  }

  // GEO-2. Which part of the shadow a point is in, from its distance behind
  // the body and its distance from the shadow axis.
  function region(sourceRadius, bodyRadius, distance, behind, fromAxis) {
    const s = shadowRadii(sourceRadius, bodyRadius, distance, behind);
    if (fromAxis < s.umbra) return s.antumbra ? "antumbra" : "umbra";
    if (fromAxis < s.penumbra) return "penumbra";
    return "outside";
  }

  // Area common to two discs of radii r1 and r2 whose centres are d apart.
  function lensArea(r1, r2, d) {
    const a = r1 * r1 * Math.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1));
    const b = r2 * r2 * Math.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2));
    const c = 0.5 * Math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2));
    return a + b - c;
  }

  // GEO-3. The observer's view of a source disc of apparent radius rs and an
  // occulting disc of apparent radius ro, centres s apart. covered is the
  // fraction of the source disc's area that is hidden (the obscuration).
  function discView(rs, ro, s) {
    if (s >= rs + ro) return { kind: "none", covered: 0 };
    if (s <= ro - rs) return { kind: "total", covered: 1 };
    if (s <= rs - ro) return { kind: "annular", covered: (ro * ro) / (rs * rs) };
    return { kind: "partial", covered: lensArea(rs, ro, s) / (Math.PI * rs * rs) };
  }

  // GEO-4. A point source is hidden when it lies inside the occulting disc.
  function pointHidden(s, ro) {
    return s < ro;
  }

  // GEO-5. Contacts of a straight-line pass: relative position (u, v),
  // relative velocity (u', v'), limiting distance L. With n^2 = u'^2 + v'^2
  // and sin psi = (u v' - u' v) / (n L), the 1961 Explanatory Supplement gives
  // t = L cos psi / n - (u u' + v v') / n^2, cos psi negative at the first
  // contact. Returns [first, last] or null when the pass misses.
  function contacts(u, v, up, vp, L) {
    const n2 = up * up + vp * vp;
    if (n2 === 0) return null;
    const n = Math.sqrt(n2);
    const sinPsi = (u * vp - up * v) / (n * L);
    if (Math.abs(sinPsi) > 1) return null;
    const cosPsi = Math.sqrt(1 - sinPsi * sinPsi);
    const mid = -(u * up + v * vp) / n2;
    const half = (L * cosPsi) / n;
    return [mid - half, mid + half];
  }

  return {
    shadowRadii: shadowRadii,
    umbraLength: umbraLength,
    region: region,
    discView: discView,
    pointHidden: pointHidden,
    contacts: contacts,
  };
});
