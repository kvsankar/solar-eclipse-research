---
title: Effect of the radius on eclipse products
description: How much path width, path limits, central duration, contact times and grazing zones move per 0.1 arcsecond of solar radius, with the published numbers and a way to expose the radius and its uncertainty.
order: 2
status: working
updated: 2026-09-15
tags: [solar-radius, path-limits, duration, contact-times, uncertainty]
---

::: summary
- **Each path limit moves about 0.18 km per 0.1 arcsecond** at the fundamental plane, or 0.2 to 0.3 km on the ground at typical Sun altitudes. The path narrows by twice that. Switching from 959.63 to 959.95 arcseconds moves each limit inward by roughly 0.6 to 0.9 km. That figure is derived here, and Dunham quotes 0.7 km for Maine in 2024 [@sun-iota-dunham-2024].
- **Central duration drops about 0.5 s per 0.1 arcsecond.** Quaglia et al. computed a 1.8 s loss on the 2017 central line for 959.63 to 960.00 arcseconds, and the Besselian Elements site rounds this to 130 s becoming 128 s [@sun-quaglia-2021] [@sun-be-impact].
- **Near a limit the sensitivity is about ten times larger.** At a site 1.2 km inside the 2017 southern limit the same change cut totality from 32.6 s to 13.3 s, and Wright and Young give "1 s in duration [...] corresponds to an error as small as 20 km (0.03 arcseconds)" [@sun-quaglia-2021] [@sun-wright-young-2024].
- **C2 is later and C3 earlier by 0.2 to 0.3 s per 0.1 arcsecond** on the central line, because the lunar limb sweeps the solar limb at 0.3 to 0.5 arcseconds per second [@sun-sigismondi-2012].
- **Grazing zones move but do not widen.** The radius shifts the mean limit. The zone width is set by the lunar limb profile [@sun-gsfc-explain].
- **Irwin's 2024 map** with 959.95 arcseconds moved the northern limit "several city blocks" southeast relative to NASA's 696,000 km map. The southern limit also moved, because the map added limb and terrain corrections [@sun-wright-young-2024] [@sun-earthsky-2024].
- **Report the radius uncertainty as a band.** ± 0.05 arcseconds is a ± 0.1 km band on each limit and ± 0.3 s on a central line duration, and Quaglia et al. describe the limits as "fuzzy bands 100 m wide" [@sun-quaglia-2021].
:::

**The question.** Given the values in [Solar radius values and their provenance](solar-radius-values.md), what does a change of 0.1 arcseconds in the adopted solar radius do to each eclipse product, what have the predictors themselves published about it, and how should a developer expose the radius and its uncertainty?

## The geometry

In the Besselian formulation the umbral cone half-angle $f_2$ and the penumbral half-angle $f_1$ are

$$\sin f_1 = \frac{R_\odot + k}{r_{sm}}, \qquad \sin f_2 = \frac{R_\odot - k}{r_{sm}}$$

where $R_\odot$ is the solar radius, $k$ the lunar radius and $r_{sm}$ the Sun to Moon distance, all in Earth radii. The 1961 Supplement writes the solar radius $S$ in this pair of equations, a letter this project reserves for the ellipsoid auxiliary. The radii of the shadow circles on the fundamental plane are

$$l_1 = z \tan f_1 + k \sec f_1, \qquad l_2 = z \tan f_2 - k \sec f_2$$

with $z$ the Moon's distance from the fundamental plane. These are the standard expressions behind the Besselian elements published by NASA GSFC and used by Stellarium [@sun-gsfc-explain] [@sun-stellarium-sec]. Differentiating with respect to $R_\odot$ and noting that $\delta f_2 \approx \delta R_\odot / r_{sm}$, which is just the change in the Sun's angular semidiameter $\delta s_0$ in radians,

$$\delta l_2 \approx z\,\delta s_0, \qquad \delta l_1 \approx z\,\delta s_0$$

The umbra shrinks and the penumbra grows by the same linear amount. With $z$ between 363,000 and 405,000 km and $\delta s_0 = 0.1$ arcseconds $= 4.85 \times 10^{-7}$ rad, $\delta l_2$ is 0.176 to 0.196 km. On the ground each limit moves by $\delta l_2 / \sin h$ where $h$ is the Sun's altitude: 0.19 km at $h = 70^{\circ}$ and 0.28 km at $h = 40^{\circ}$ per 0.1 arcseconds. The full 0.32 arcsecond change from 959.63 to 959.95 arcseconds therefore moves each limit inward by 0.6 to 0.9 km and narrows a path by 1.2 to 1.8 km. Dunham checked this on Jubier's map for Maine in 2024: Jubier's limb-corrected duration reaches zero "about 0.7 km farther northwest" than Irwin's 959.95 arcsecond limit, "which is consistent with the difference in the values for the solar radius used" [@sun-iota-dunham-2024]. Wright and Young's raster method contains the same dependence in a different form: an observer in the [?limb-test-zone] is in totality only if every limb element, scaled to units of the apparent solar radius, lies at a distance $\rho > 1$ from the Sun's centre, so the radius enters as the unit of the limb test [@sun-wright-young-2024].

## Path width and the position of the limits

| Change in adopted radius | Shift of each limit at the fundamental plane | Shift on the ground ($h$ = 40° to 70°) | Change in path width |
|---|---|---|---|
| +0.1 arcseconds | 0.18 km inward | 0.19 to 0.28 km | −0.4 to −0.6 km |
| 959.63 → 959.95 (+0.32) | 0.59 km inward | 0.6 to 0.9 km | −1.2 to −1.8 km |
| 959.63 → 960.00 (+0.37) | 0.68 km inward | 0.7 to 1.0 km | −1.4 to −2.1 km |
| 959.63 → 959.22 (−0.41) | 0.76 km outward | 0.8 to 1.2 km | +1.6 to +2.3 km |

These are derived figures. The published checks agree with them. Quaglia et al. found that the distance from their Oregon site to the southern limit was "1200 m" for 959.63 arcseconds and "less than 400 m" for 960.00 arcseconds, a shift of about 0.8 km at a Sun altitude near 45° [@sun-quaglia-2021]. Wright and Young report that Irwin's 959.95 arcsecond map shifted "the northern limit of the path to the southeast by several city blocks compared to maps calculated with the conventional radius" [@sun-wright-young-2024]. EarthSky's description of Irwin's map notes that "the entire northern edge of the path of totality is narrower than we thought, while the southern edge is wider in Texas but narrower everywhere else". The Texas anomaly comes from the limb and terrain corrections that Irwin's map also includes, not from the radius, which always narrows the path [@sun-earthsky-2024]. NASA's own 2017 and 2024 maps used 696,000 km, so a product built on 959.95 arcseconds will disagree with them by 0.6 to 0.9 km at every limit [@sun-svs-4515] [@sun-wright-young-2024].

## Central duration

On the central line totality ends when the Moon's limb clears the far side of the Sun, so a larger Sun shortens totality at both ends. The lunar limb crosses the solar limb at "the angular speed of 0.3-0.5 arcsec/s" as seen from the ground [@sun-sigismondi-2012]. Each 0.1 arcsecond of extra radius therefore delays C2 by 0.2 to 0.33 s and advances C3 by the same amount, for a loss of 0.4 to 0.7 s of duration. Quaglia et al. computed the loss for the 2017 eclipse between 959.63 and 960.00 arcseconds: "on the centreline the drop in duration is only 1.8 s", which is 0.49 s per 0.1 arcseconds [@sun-quaglia-2021]. The Besselian Elements site states the same example as "the duration of totality drops from 130s to 128s" [@sun-be-impact]. The Photographer's Ephemeris (Photo Ephemeris) uses the same reasoning to justify its bead simulator setting: "a larger Sun remains eclipsed for a shorter time" [@sun-photoephemeris-technote]. The 2 s figure is small against the ± 3 to 15 s that the lunar limb profile contributes to C2 and C3 at any site [@sun-photoephemeris-technote], so on the central line the radius choice is a second-order correction.

## Duration and contact times near a limit

The observed cases themselves are collected in [observed against predicted](../10-validation/observed-vs-predicted.md). This section keeps the sensitivity the radius owns.

Near a limit the geometry is tangential and the sensitivity explodes. At Quaglia's site, 1.2 km inside the 2017 southern limit, the predicted duration for 959.63 arcseconds was 32.6 s and for 960.00 arcseconds it was 13.3 s: "at the observing site the drop is 19.3 s" [@sun-quaglia-2021]. That is 5.2 s per 0.1 arcseconds, about ten times the central line figure. The flash-spectrum video showed 9 to 17 s of photospheric extinction, incompatible with the 32.6 s predicted by the standard radius [@sun-quaglia-2021]. The Besselian Elements site gives the same case as "34s to 13s" [@sun-be-impact]. Wright and Young state the general rule for such sites: "a discrepancy of 1 s in duration, for example, corresponds to an error as small as 20 km (0.03 arcseconds) in solar radius" [@sun-wright-young-2024]. Dunham draws the practical conclusion for observers: durations read from Jubier's map near the 2024 limits "should be up to 10s less than these, if John Irwin's solar radius had been used for the calculation", and a site should keep an [?umbral-depth] of at least 2.0 km [@sun-iota-dunham-2024].

The predictors also disagree with each other at the same radius. For Quaglia's site and 959.63 arcseconds, Solar Eclipse Maestro predicted 36.1 s, Occult's main eclipse page 33.3 s, Occult's Baily's beads tool 34.1 s and Irwin's model 32.6 s. The authors convert the spread into radius terms: "for a given value of the duration of totality, Occult would infer a value for the solar radius S 0.03″ higher than the one inferred by our model while Solar Eclipse Maestro would be 0.07″ higher" [@sun-quaglia-2021]. An eclipse radius is therefore tied to the limb model and contact algorithm it was fitted with, at the 0.03 to 0.07 arcsecond level.

## Outer contacts, magnitude and obscuration

C1 and C4 move by $\delta s_0 / \omega$, the same 0.2 to 0.3 s per 0.1 arcseconds as C2 and C3 but in the opposite sense: a larger Sun makes C1 earlier and C4 later. Magnitude and obscuration depend on the ratio of lunar to solar semidiameter. A 0.32 arcsecond change in 959.63 arcseconds is 0.03 per cent, invisible in any published table. No source reviewed here proposes a separate solar radius for the penumbral contacts, and the physics does not require one at the precision of published C1 and C4 times.

## Grazing zones

Espenak's graze zones are bands around each mean limit within which the lunar limb profile determines whether an observer sees a brief total or a beaded eclipse. The NASA eclipse site (eclipse.gsfc.nasa.gov) explanation page describes them under "Limb Corrections to the Path Limits: Graze Zones" and computes them from the Watts limb extremes [@sun-gsfc-explain]. A change of solar radius translates the mean limit by the amounts tabulated above and carries the graze zone with it. The width of the zone is set by the spread of limb heights and is unchanged to first order. Irwin's 2024 Google Earth file plots the corrected limit with its ± 1σ lines as "the 3 orange lines", separated by less than 90 m, which Dunham considers too optimistic "considering the sensitivity of different telescopes and cameras for recording the smaller beads" [@sun-iota-dunham-2024].

## What the predictors have published about it

- **NASA SVS.** Wright and Young acknowledge that "predictions of the duration of totality, the appearance and distribution of Baily's beads, and the location of the path limits are all exquisitely sensitive to the choice of solar radius". They list the eclipse-derived values 959.99, 959.95, 959.98 and 960.01 arcseconds and describe the 2024 media reaction to Irwin's map. Their figures nevertheless assume 696,000 km, and the SVS 2017 constants block prints "Sun radius 696,000 km (959.645 arcsec at 1 AU)" [@sun-wright-young-2024] [@sun-svs-4515]. No SVS 2023 or 2024 page reviewed prints a constants block [@sun-svs-5073] [@sun-svs-5365].
- **Jubier.** The map help page warns that the true photospheric radius "is closer to 959.98 arc-seconds at one astronomical unit (±0.02 arc-second)" while the map uses 959.63 arcseconds [@sun-jubier-map-help].
- **Occult.** Occult simulates with 959.63 arcseconds and treats observed bead timings as a correction ΔR to that radius [@sun-raponi-sigismondi-2011]. Adassuriya's reduction with Occult 4.0.8.6 and DE423 is the worked example: eight beads, ΔR = +0.26 ± 0.18 arcseconds [@sun-adassuriya-2011].
- **IOTA.** Dunham's 2024 page recommends Jubier's map for topography-corrected times but Irwin's limits for position, and gives the 0.7 km and 10 s rules quoted above [@sun-iota-dunham-2024].
- **Besselian Elements.** The team publishes 959.95 ± 0.05 arcseconds and the 130 s to 128 s and 34 s to 13 s examples [@sun-be-solar-radius] [@sun-be-impact].
- **timeanddate.** The help page says the shaded areas "may be off by a few hundred meters" and advises moving "a few hundred meters toward the center", without naming the radius [@sun-timeanddate-help].

## Sources compared

| Source | What it uniquely provides for this note |
|---|---|
| Quaglia et al. 2021 [@sun-quaglia-2021] | Duration versus radius at the central line and at a limit, computed every 0.01 arcseconds, plus the Occult and Solar Eclipse Maestro cross-check. |
| Wright and Young 2024 [@sun-wright-young-2024] | The 1 s ↔ 0.03 arcsecond rule near the limits and NASA's account of the 2024 map controversy. |
| Dunham, IOTA 2024 [@sun-iota-dunham-2024] | Field-tested shift of 0.7 km and duration correction of up to 10 s on Jubier's map. |
| Besselian Elements impact note [@sun-be-impact] | The 2017 Vale example in round numbers. |
| Sigismondi 2012 [@sun-sigismondi-2012] | The 0.3 to 0.5 arcsecond per second limb speed that converts radius to contact time. |
| GSFC explanation page [@sun-gsfc-explain] | The definition of graze zones and the k convention. |

## What a developer should do

1. Expose `solar_radius_arcsec` (default 959.95, uncertainty 0.05, provenance "Quaglia et al. 2021, Lamy et al. 2015") as a top-level parameter of every product, alongside the ephemeris, ΔT and limb dataset identifiers. Provide the preset 959.63 so users can reproduce NASA, Jubier and Occult output.
2. Compute every path limit twice more, at $s \pm \sigma_s$, and publish the three lines. With $\sigma_s = 0.05$ arcseconds the band is ± 0.1 km at the fundamental plane and ± 0.1 to 0.15 km on the ground. Add the limb-profile uncertainty in quadrature and state the combined width. Quaglia's "fuzzy bands 100 m wide" is the physical floor [@sun-quaglia-2021].
3. Report central duration with a ± 0.3 s radius term for two-minute eclipses. Near a limit, report the duration as the range obtained from the $s \pm \sigma_s$ runs.
4. For local circumstances within about 2 km of a limit, print the [?umbral-depth] and a warning that the radius uncertainty dominates, following Dunham's 2 km rule [@sun-iota-dunham-2024].
5. When comparing against a reference product, first match its radius, its $k$ and its limb dataset. A 0.03 to 0.07 arcsecond difference between Occult, Solar Eclipse Maestro and Irwin's model at the same nominal radius is otherwise mistaken for a bug [@sun-quaglia-2021].

## What this changes

The path-limit, duration and local-circumstance outputs of the pipeline acquire a radius-dependent uncertainty band, and the comparison harness in [error budget and validation protocol](../10-validation/error-budget-and-validation-protocol.md) must record the radius used by each reference. The Besselian element generator needs no structural change. Only the constant $R_\odot$ and its propagation to $f_1$, $f_2$, $l_1$, $l_2$ are affected.

## Open questions

- Obtain Quaglia et al.'s Figure 2 data (duration and limit distance versus radius every 0.01 arcseconds) or reproduce it with the LOLA limb to confirm the 5 s per 0.1 arcsecond slope at 1.2 km from a limit [@sun-quaglia-2021].
- Obtain Irwin's 2024 Google Earth KML with the ± 1σ limit lines to measure the band width he published [@sun-iota-dunham-2024].
- Obtain Wright and Young's raster code or its equivalent to test whether the limb-test formulation and the Besselian formulation give the same limit shift per 0.1 arcseconds [@sun-wright-young-2024].
- Obtain a published table of C1 and C4 sensitivity to the solar radius. None was located, and the figures above are derived from the limb-speed argument.
