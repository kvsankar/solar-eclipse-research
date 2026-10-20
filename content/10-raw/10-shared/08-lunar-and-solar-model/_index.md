---
title: Lunar and solar model
description: Ephemerides, lunar radius, centre of figure, coordinate frames and libration choices used by solar eclipse calculation algorithms.
order: 8
status: working
updated: 2026-09-30
tags: [ephemeris, jpl-de, lunar-radius, libration, lunar-frames]
seo_title: Sun and Moon Models for Solar Eclipse Algorithms
---

::: summary
- **Modern ephemerides fit lunar ranging closely.** DE440's recent range residuals are about 1.3 cm. Range residuals and inter-release differences do not certify every orbit component. Consistent reductions, [ΔT](../07-earth-and-time/delta-t-and-earth-rotation.md), [limb profiles](../../20-solar-eclipses-and-transits/05-lunar-limb/limb-profile-methods.md) and the [solar radius](../../20-solar-eclipses-and-transits/06-solar-radius/solar-radius-values.md) remain necessary for the cited modern eclipse comparisons [@moon-park-2021] [@moon-williams-2013].
- **The figure is not a sphere and $k$ is a compromise.** The IAU $k = 0.2725076$ is a limb mean 0.9 km larger than the [LOLA](https://lola.gsfc.nasa.gov/) mean sphere. [Espenak](https://en.wikipedia.org/wiki/Fred_Espenak) uses $k = 0.272281$ for umbral contacts so that beaded annulars are not called total [@moon-espenak-2001-bulletin] [@moon-williams-2013].
- **The ephemeris gives the centre of mass, the limb is set by the figure.** The centre of figure sits 1.935 km from the centre of mass, mostly along the Earth-Moon line, so the sky-plane part is about 0.5 arcseconds [@moon-jones-2025] [@moon-espenak-meeus-canon].
- **Orientation comes from the ephemeris, not the IAU series.** Use `moon_pa_de440_200625.bpc` with the constant principal-axis to mean-Earth rotation, and compute libration per observer, since topocentric libration differs from geocentric by up to 1 degree [@moon-naif-moon-fk-de440] [@moon-es-1992].
:::

## What this topic covers

Two notes on the bodies that cast the shadow. The first asks which ephemeris places the Moon and the Sun, and how far the semi-analytical theories fall behind the numerical integrations. The second asks what the Moon's solid figure does that its centre of mass does not: the radius ratio $k$, the offset of the centre of figure, the principal-axis and mean-Earth frames, and the libration that orients a limb profile.

## Notes in this topic

- [Lunar and solar ephemerides](ephemerides.md): the JPL DE series release by release, INPOP, EPM, ELP and VSOP87, the kernel files, the readers, and where each error lands in arcseconds, seconds and kilometres.
- [Lunar figure, radius ratio k, and libration](lunar-figure-and-libration.md): centre of mass versus centre of figure, the three values of $k$, the DE Euler angles, the PA and ME frames, topocentric libration, and the master table of every model choice with its size.

## What this topic changes for the pipeline

The pipeline's Moon is two objects, not one: a centre of mass from DE440 and a figure from LOLA oriented by DE440 librations in the mean-Earth frame. Use `de440s.bsp` only within its stated 1849 to 2150 interval, with the matching lunar orientation kernel. Validate the reduction chain as well as ΔT, limb profile and solar radius [@moon-naif-summaries] [@moon-naif-moon-pa-de440-cmt]. The constant $k$ survives only as the datum radius that profile heights are measured from and as a fallback for profile-free products. The master table of every model choice, with its size on the sky, in contact time and in path shift, is at the end of [lunar figure, radius ratio k, and libration](lunar-figure-and-libration.md).
