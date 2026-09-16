---
title: Foundations
description: Besselian elements, the fundamental plane, and how the elements are derived from an ephemeris of the Sun and Moon.
order: 1
status: working
updated: 2026-09-15
tags: [besselian, fundamental-plane, foundations]
---

::: summary
- **Eight numbers describe the shadow.** $x, y, d, \mu, l_1, l_2$ vary with time and $\tan f_1, \tan f_2$ are held constant for the eclipse. Everything a global or local product computes follows from them and their rates [@bes-es1961] [@bes-nasa-beselm].
- **Two lunar radius ratios, never one.** $k = 0.272281$ for all umbral and antumbral contacts, and for penumbral contacts 0.2724880 in the Five Millennium Canon and the NASA pages derived from it, 0.2725076 in the NASA bulletins and on EclipseWise [@bes-nasa-radius] [@bes-nasa-2024-elements].
- **ΔT enters only through $\mu$.** The elements themselves are free of it. A published $\mu$ is a Greenwich hour angle carried against a TT argument, and the shift of 15.041 arcseconds of longitude per second of ΔT is applied when $\mu$ becomes a longitude [@bes-es1961] [@bes-lasteclipse].
- **The solar semidiameter is a parameter, not a constant.** Every published prediction uses Auwers' $s_0 = 959.63$ arcseconds at 1 au, while eclipse observations give about 959.95 arcseconds [@bes-quaglia-2021].
- **No open library generates elements from a JPL ephemeris as a documented, validated function.** Skyfield does not project the shadow, and the Swiss Ephemeris computes the geometry live without ever exposing $x, y, l_1, l_2$ [@bes-skyfield-801] [@bes-swisseph-swecl].
:::

## What this topic covers

The geometric core of every solar eclipse computation: Bessel's fundamental
plane and its sign conventions, the eight tabulated elements that describe the
Moon's shadow in that plane, the constants and time scale built into them, the
polynomial form in which NASA and Meeus publish them, and the ordered equations
that turn geocentric apparent places of the Sun and Moon into a table of
elements. It also covers when to abandon the elements and compute topocentric
circumstances directly from the ephemeris.

## Notes in this topic

- [Besselian elements and the fundamental plane](besselian-elements.md): what
  the elements are, sign conventions, units, time scales, the constants, and
  the polynomial form NASA publishes.
- [From ephemeris to elements](ephemeris-to-elements.md): the ordered list of
  equations a developer needs, what the almanacs and open-source codes do about
  frames, light-time and aberration, and the polynomial fit.

## What this topic changes for the pipeline

The interface between the ephemeris stage and everything downstream is a table
of $(x, y, d, \mu, l_1, l_2)$ against TT plus the two cone constants and a
metadata record naming the ephemeris, ΔT, $k_1$, $k_2$, $s_0$, the ellipsoid
and $t_0$. Global and local circumstances consume only that record. Two design
decisions follow from it: the umbral $k$ and the solar semidiameter are inputs
rather than constants, and ΔT is carried as metadata rather than applied inside
the elements. The topocentric path is built as a second, independent engine
from the same ephemeris layer, and the agreement of the two is a regression
test.
