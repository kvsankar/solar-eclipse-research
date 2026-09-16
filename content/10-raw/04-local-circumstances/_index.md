---
title: Local circumstances
description: From Besselian elements or a topocentric ephemeris to one observer's contact times, magnitude, obscuration, position angles, altitude, duration, the corrections that move those numbers by seconds, and the public code that computes them.
order: 4
status: working
updated: 2026-09-15
tags: [local-circumstances, besselian, topocentric, contacts, bailys-beads]
---

::: summary
- **The algorithm is the 1961 Explanatory Supplement section 9D,** restated in 1992 with a recommendation for direct root finding, and implemented verbatim in NASA's `program.js`, Stellarium's AstroCalc and the open GitHub engines [@loc-es1961-local] [@loc-es1992-ch8] [@loc-jsex-program-js].
- **The whole reduction is eight formulas.** Project the observer onto the fundamental plane, subtract from the shadow-axis coordinates, shrink the shadow radii with $L' = L - \zeta\tan f$, then solve $u^2+v^2 = L'^2$ for the contacts and $uu'+vv'=0$ for maximum eclipse [@loc-es1961-local].
- **The topocentric method is one equation on the apparent separation,** used by USNO and the Swiss Ephemeris, and it agrees with the Besselian reduction to 0.1 s when the ephemeris, the radii and $\Delta T$ agree [@loc-usno-sec] [@loc-swecl-c].
- **The lunar limb and the solar radius are the corrections that matter,** at 2 to 3 s and 1 to 2 s on the central line and tens of seconds near the path edge. Every open implementation omits both [@loc-nasa-limb-help] [@loc-be-solar-radius].
- **The choice of $k$ is worth 4 s of totality,** with 2m40.3s against 2m44.3s for 2017 August 21 in Illinois [@loc-eclipsewise-radius].
:::

## What this topic covers

This topic takes the elements as given and reduces them to one site. It covers the observer's projection onto the fundamental plane, the contact and maximum-eclipse solutions, magnitude in its two branches, obscuration as a lens area, the position and vertex angles, altitude, azimuth and duration, and the conversion from Terrestrial Time to UT. It then covers the direct topocentric alternative and the libraries that support it, and finally the corrections that the smooth-Moon reduction leaves out, with their sizes in seconds and a survey of the public code that does or does not apply them.

## Notes in this topic

- [Contact times, magnitude and position angles from Besselian elements](contact-times-and-magnitude.md): the thirteen-step reduction, then the formulas with symbols, constants and the JSEX code, step by step.
- [The direct topocentric method](topocentric-method.md): the separation equation, USNO, Swiss Ephemeris, sunpy, Skyfield, astropy, PyEphem, Horizons, SPICE and Stellarium.
- [Corrections that move contact times, Baily's beads, and public code](corrections-and-code.md): sizes in seconds, the bead computation, and a table of implementations.

## What this topic changes for the pipeline

The local stage becomes two interchangeable engines that must agree to 0.1 s, one Besselian and one topocentric. The corrections layer sits above them, and its inputs, the solar radius, the limb profile and $\Delta T$, become explicit pipeline parameters rather than constants buried in element files. The stage must also export, for each interior contact, the position angle $P$, the position angle and speed of the relative motion and the topocentric libration, because those are what the limb and bead stages consume.
