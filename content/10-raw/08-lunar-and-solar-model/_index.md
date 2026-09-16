---
title: Lunar and solar model
description: The ephemerides that place the Moon and Sun, the physical model of the Moon (centre of mass versus figure, the radius ratio k, the PA and ME frames, libration) and what each choice costs in arcseconds, seconds and kilometres.
order: 8
status: working
updated: 2026-09-15
tags: [ephemeris, jpl-de, lunar-radius, libration, lunar-frames]
---

::: summary
- **The orbit is solved.** DE440 places the Moon to about a metre in the present century, which is under 10 ms of contact time. The errors that matter live in ΔT, the limb profile and the solar radius [@moon-park-2021] [@moon-williams-2013].
- **The figure is not a sphere and $k$ is a compromise.** The IAU $k = 0.2725076$ is a limb mean 0.9 km larger than the LOLA mean sphere. Espenak uses $k = 0.272281$ for umbral contacts so that beaded annulars are not called total [@moon-espenak-2001-bulletin] [@moon-williams-2013].
- **The ephemeris gives the centre of mass, the limb is set by the figure.** The centre of figure sits 1.935 km from the centre of mass, mostly along the Earth-Moon line, so the sky-plane part is about 0.5 arcseconds [@moon-jones-2025] [@moon-espenak-meeus-canon].
- **Orientation comes from the ephemeris, not the IAU series.** Use `moon_pa_de440_200625.bpc` with the constant principal-axis to mean-Earth rotation, and compute libration per observer, since topocentric libration differs from geocentric by up to 1 degree [@moon-naif-moon-fk-de440] [@moon-es-1992].
:::

## What this topic covers

Two notes on the bodies that cast the shadow. The first asks which ephemeris places the Moon and the Sun, and how far the semi-analytical theories fall behind the numerical integrations. The second asks what the Moon's solid figure does that its centre of mass does not: the radius ratio $k$, the offset of the centre of figure, the principal-axis and mean-Earth frames, and the libration that orients a limb profile.

## Notes in this topic

- [Lunar and solar ephemerides](ephemerides.md): the JPL DE series release by release, INPOP, EPM, ELP and VSOP87, the kernel files, the readers, and where each error lands in arcseconds, seconds and kilometres.
- [Lunar figure, radius ratio k, and libration](lunar-figure-and-libration.md): centre of mass versus centre of figure, the three values of $k$, the DE Euler angles, the PA and ME frames, topocentric libration, and the master table of every model choice with its size.

## What this topic changes for the pipeline

The pipeline's Moon is two objects, not one: a centre of mass from DE440 and a figure from LOLA oriented by DE440 librations in the mean-Earth frame. The ephemeris can therefore be fixed once, as `de440s.bsp`, and validation effort spent on ΔT, the limb profile and the solar radius instead. The constant $k$ survives only as the datum radius that profile heights are measured from and as a fallback for profile-free products. The master table of every model choice, with its size on the sky, in contact time and in path shift, is at the end of [lunar figure, radius ratio k, and libration](lunar-figure-and-libration.md).
