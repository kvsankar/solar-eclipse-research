---
title: Observations, the black drop and the solar radius
seo_title: Transit Observations: Black Drop and Solar Radius
description: What observed transit contacts show against predictions, why the black drop blurs them, the Venus aureole, the astronomical unit, and solar radius results.
order: 3
status: working
updated: 2026-10-17
tags: [transits, black-drop, aureole, solar-radius, astronomical-unit, validation]
---

::: summary
- **The black drop is optical blurring of a limb-darkened edge, not an atmosphere.** The Transition Region and Coronal Explorer (TRACE) saw a faint black drop at the 1999 Mercury transit from space, and its only radial anisotropies came from "the convolution of the instrumental point-spread function with the solar limb-darkened, back-lit, illumination function" [@tr-spg-2004]. Ground seeing widens that function. Historical timings were therefore good only to about a minute [@tr-spg-2003-hoa].
- **The aureole of Venus is real and comes from its mesosphere.** Photometry of the 2004 transit fitted refraction about 26 to 38.5 km above the opaque layer, with scale heights of 3.1 to 4.8 km [@tr-tanga-2012]. It affects contact timing at about the scale of the telescope's PSF [@tr-xie-2013].
- **Transits gave the first good astronomical unit.** The 1761 and 1769 results ranged from 8.5 to 10.5 arcseconds of solar parallax depending on the reducer. Encke later derived 8.5776 arcseconds and [Newcomb](https://en.wikipedia.org/wiki/Simon_Newcomb) 8.79 arcseconds from 1874 and 1882, against the radar value of 8.79415 [@tr-eso-eis-f2] [@tr-eso-eis-f5].
- **In 2004, 4550 public timings recovered the astronomical unit (AU) to 0.007 per cent, but only after a cut that assumes the prediction.** Keeping the 583 timings within 4 seconds of prediction gave 149 608 708 ± 11 835 km. With all timings within 30 seconds the average was 1 086 436 km short [@tr-eso-vt2004-results] [@tr-imcce-vt2004-note2].
- **Space transits measure the [solar radius](../06-solar-radius/solar-radius-values.md).** The Michelson Doppler Imager on the Solar and Heliospheric Observatory ([SOHO](https://en.wikipedia.org/wiki/Solar_and_Heliospheric_Observatory)/MDI) timed the 2003 and 2006 Mercury transits. The timings gave 960.12 ± 0.09 arcseconds. The Helioseismic and Magnetic Imager on the [Solar Dynamics Observatory](https://en.wikipedia.org/wiki/Solar_Dynamics_Observatory) (SDO/HMI) at the 2012 Venus transit gave 959.57 ± 0.02 arcseconds after PSF correction [@tr-emilio-2012] [@tr-emilio-2020]. The two differ by 0.55 arcseconds, more than the 0.41 arcsecond gap between 959.63 arcseconds and the IAU nominal radius [@sun-prsa-2016] [@sun-quaglia-2021].
- **Modern observed-minus-predicted contact differences are a few seconds in space and tens of seconds on the ground.** MDI contacts were offset 8 s and 5 s from NASA's ephemeris [@tr-emilio-2012]. Visual 2016 observations in Rome and Tehran ranged from 2 s to 107 s late [@tr-sigismondi-altafi-2018]. No observed-versus-predicted analysis of the 2019 Mercury transit has appeared in the Journal for Occultation Astronomy (JOA), the Journal of the British Astronomical Association (BAA) or [arXiv](https://arxiv.org/). A space timing must be predicted for the spacecraft's position [@tr-emilio-2012].
:::

**The question.** When observed transit contacts are compared with the predictions of [Contacts and local circumstances](contacts-and-local-circumstances.md), what do the differences show, what limits the timing, and what have transits measured: the astronomical unit historically and the solar radius today? Eclipse-based radius work is in [Solar radius](../06-solar-radius/_index.md) and the eclipse validation record is in [Observed against predicted](../10-validation/observed-vs-predicted.md).

## The black drop

### What observers see

[Espenak](https://en.wikipedia.org/wiki/Fred_Espenak) describes the appearance at second contact. "Just before contact II, the so-called black drop effect is seen. At that time, the transiting planet seems to be attached to the Sun's limb by a thin column or thread. When the thread breaks and the planet is completely surrounded by sunlight, this marks the true instant of contact II. Contact III occurs in exactly the reverse order" [@tr-nasa-oh2012]. His 2019 article adds that the thread-breaking time is delayed after true contact "by some seconds, up to a minute" [@tr-ew-tm2019]. Schneider, Pasachoff and Golub define the [?tr-black-drop|black drop] as "the appearance of a band linking the solar limb to the disk of a transiting planet near the point of internal tangency" and state that it "had limited the accuracy of the determination of the Astronomical Unit and the scale of the Solar System in the 18th and 19th centuries" [@tr-spg-2004]. In their conference summary, the historical "timing accuracy was thus closer to a minute than to the expected second or two" [@tr-spg-2003-hoa].

### Four explanations in the sources

The sources give four causes, and the differences matter for how a contact is defined:

| Explanation | Source | Status |
|---|---|---|
| The atmosphere of Venus | Discussed and rejected by Schneider et al., who say the problem "was misunderstood in the case of Venus ... due the presence of its atmosphere" [@tr-spg-2004] | Rejected for Mercury, which has no atmosphere and still shows the effect |
| Diffraction by the telescope | The Institut de mécanique céleste et de calcul des éphémérides ([IMCCE](https://www.imcce.fr/)) for the European Southern Observatory (ESO), quoting Couderc and [Danjon](https://en.wikipedia.org/wiki/Andr%C3%A9_Danjon) (1969): "It is due to diffraction and can be reproduced and photographed in the laboratory" [@tr-eso-eis-f2] | Part of the PSF |
| Atmospheric seeing | Espenak: "Modern analyses show that the black drop is the result of seeing effects due to Earth's turbulent atmosphere" [@tr-nasa-oh2012] | Part of the PSF on the ground |
| PSF convolved with solar limb darkening | Schneider, Pasachoff and Golub from TRACE [@tr-spg-2004] | The measured mechanism |

The TRACE result decides between them. TRACE observed the 1999 November 15 transit in white light with 0.5 arcsecond pixels and a 30 cm telescope, "Nyquist-limited by the 0.5 pixels sampling of its CCD" rather than diffraction-limited [@tr-spg-2004]. "In spite of the telescope's location beyond the Earth's atmosphere, and the absence of a significant mercurian atmosphere, a faint Black Drop effect was detected. After calibration and removal of, or compensation for, both internal and external systematic effects, the only radially directed brightness anisotropies found resulted from the convolution of the instrumental point-spread function with the solar limb-darkened, back-lit, illumination function" [@tr-spg-2004]. The conclusion is that "the principal cause of the Black Drop effect ... is optical broadening resulting from the convolution of the systemic PSF with the planetary and limb-darkened solar disks" [@tr-spg-2004]. The [?tr-psf|point-spread function] of a ground telescope includes both its diffraction and the seeing, so the diffraction and seeing explanations are special cases. The [?limb-darkening-function|limb darkening] makes the edge of the Sun dim, so a blurred dark planet near it merges with the dark sky beyond the limb.

Three numbers from the TRACE analysis set the scale. Richardson-Lucy deconvolution made the planet's "photometric radius ~0.55" (~270 km) narrower" [@tr-spg-2004]. After 50 iterations the edge still had "a residual photometric half-width of ~1.13 pixels (0.56")" [@tr-spg-2004]. A polychromatic Fresnel calculation put the diffraction edge of Mercury's own disc at about 43 km at Mercury's distance, "only ~1/6 of a TRACE pixel" and "not a significant contributor to the Black Drop effect" [@tr-spg-2004]. The 2003 TRACE data could not repeat the analysis because they were downlinked in a compressed format that lost the low end of the dynamic range [@tr-spg-2003-hoa].

### What it does to a contact time

The black drop delays the visual second contact and advances the visual third contact. Its size depends on the aperture. Sigismondi and colleagues state that the effect is "mainly dependent on the instrumental point spread function", "large" in telescopes of 10 cm or less, and that it "tends to disappear in larger telescopes" of 25 cm or more [@tr-sigismondi-mg13]. For the 2016 Mercury transit Sigismondi estimated the black drop to last "about 40 seconds and more after the internal contact t2" in ingress [@tr-sigismondi-2016]. Observers in Rome and Tehran in 2016 saw second contact "with only 2s of delay (2-4 s for most of the observers)", and the black drop "was confined within 2s" [@tr-sigismondi-altafi-2018]. The remedy proposed by Sigismondi is [?tr-chord-extrapolation|chord extrapolation]: measure the chord where the planet's disc cuts the limb in time-tagged images, fit "the analytic function of the chord c(t)" and find "the times when it is zero" [@tr-sigismondi-2016].

## The aureole of Venus

During ingress and egress of a Venus transit "the portion of the planet's disk outside the Solar photosphere has been repeatedly perceived as outlined by a thin, bright arc ('aureole')", which historical observers "correctly ascribed to the refraction of light by the outer layers of a dense atmosphere" [@tr-tanga-2012]. IMCCE records the 1761 descriptions of "a diffuse halo around the planet which was observed between exterior and interior contacts" [@tr-eso-eis-f2]. The 2004 transit gave "the first quantitative analysis of the phenomenon" [@tr-tanga-2012].

Tanga and colleagues modelled the [?tr-aureole|aureole] with the Baum and Code refraction formula, corrected for the Sun's finite distance, with two free parameters: the scale height $H$ and the altitude $r$ of the half-occultation level above an opaque layer [@tr-tanga-2012]. The refraction angle of a ray that passes at distance $r$ from the centre of Venus is

$$
\omega = -\nu(r)\sqrt{2\pi r/H} = -\frac{H}{D}\,e^{-(r - r_{1/2})/H},
$$

with $\nu$ the gas refractivity, $D$ the distance from Venus to the Earth and $r_{1/2}$ the half-light radius. The image of a solar surface element is shrunk radially by $\Phi = 1/(1 - D\omega/H)$, and the projected position $r_i$ of the element follows from

$$
\frac{1}{k_D}\left(\frac{1}{\Phi} - 1\right) + \log\left(\frac{1}{\Phi} - 1\right) = \frac{r_{1/2} - r_i}{H},\qquad k_D = 1 + D/D',
$$

with $D'$ the distance from Venus to the Sun [@tr-tanga-2012]. The paper writes the factor as $k$. It is $k_D$ here because $k$ is the lunar radius ratio elsewhere in the corpus. The factor "is equal to unity in the original formula" of Baum and Code, for which the source is at infinite distance [@tr-tanga-2012]. In this model $r$ and $\omega$ are Tanga's symbols, not the radius vector or the relative speed used elsewhere in this topic. Fits to the Dutch Open Telescope light curves gave $H = 3.1$ km and $r = 26$ km at mid-latitudes and $H = 4.8$ km and $r = 38.5$ km at the pole. The authors state that 3 km in $r$ or 100 m in $H$ moves the model outside the error bars [@tr-tanga-2012]. The apparent radius of Venus that day was 28.9 arcseconds [@tr-tanga-2012].

For contact timing the aureole matters near ingress and egress, exactly where contacts are timed. Xie and colleagues expect its effect on contact timings "to be of the order of the point-spread function of the telescope" and note that it "is extended also to the side of the planet immersed in the photosphere background and it decreases the perceived diameter of Venus, modifying slightly the contact timings" [@tr-xie-2013]. Neither paper gives the correction in seconds.

## The astronomical unit: the historical role

### Halley's and Delisle's methods

[Halley](https://en.wikipedia.org/wiki/Edmond_Halley) proposed in 1716 to use [transits of Venus](_index.md) to measure the solar distance, and transits of Venus suit the purpose better than Mercury's because "Venus is closer to Earth and consequently exhibits a larger parallax" [@tr-nasa-oh2012]. The measured quantity is a time, and the [?tr-diurnal-parallax|diurnal parallax] converts it to a distance. IMCCE explains: "The measurement of the AU by means of timing observations of contacts is not a measure of distance, but a measure of time, this time being different for all the observers" [@tr-imcce-vt2004-note1].

[?tr-halley-method|Halley's method] times the whole transit from sites at different latitudes. Observers see Venus cross along different chords, so the durations differ [@tr-spg-2003-hoa] [@tr-faherty-2012]. IMCCE's simplified two-site treatment states the geometry: the separation of the two apparent centres of Venus equals the difference of the parallaxes of Venus and the Sun for the baseline, and Kepler's third law gives the ratio of the Venus and Earth orbital radii [@tr-eso-eis-b4]. Since each parallax is inversely proportional to the body's distance, the measured difference fixes the solar parallax. The method needs both ingress and egress at each site.

[?tr-delisle-method|Delisle's method] compares the absolute times of one contact at two distant sites. It "only requires the observers to note the time of ingress interior ... or egress interior ... along with the observers latitude and longitude", and was "initially developed by the French astronomer Joseph-Nicolas Delisle for the 1753 transit of Mercury" [@tr-faherty-2012]. It needs accurate longitudes and clocks, which the eighteenth century lacked. For 1761 the results "varied from 8.5" to 10.5", according to who reduced the observations", because of "poor knowledge of the longitudes of the observing sites and the phenomenon known as the black drop" [@tr-eso-eis-f2].

### The eighteenth- and nineteenth-century values

IMCCE's summary table for ESO gives the [?tr-solar-parallax|solar parallax] determinations [@tr-eso-eis-f5]:

| Method or author | Solar parallax |
|---|---|
| Transits of 1761 and 1769 | 8.43″ and 8.80″ |
| Transits of 1761 and 1769, Encke (1824) | 8.5776″ |
| Transits of 1761 and 1769 (1835 revision) | 8.571 ± 0.037″ |
| Transits of 1874 and 1882, Newcomb (1890) | 8.79″ |
| Radar, NASA (1990) | 8.79415″ |

Sigismondi quotes Newcomb's transit value as 8.794 ± 0.018 arcseconds [@tr-sigismondi-au-2013] [@tr-sigismondi-mg13]. The 1761 transit had "120" professional observers "at 62 sites" [@tr-eso-eis-f2]. For 1882 the U.S. Naval Observatory alone sent eight expeditions [@tr-eso-eis-f5]. [Chauvenet](https://en.wikipedia.org/wiki/William_Chauvenet)'s own presentation shows how the time measurements enter: each observed contact at a known longitude "furnishes an equation of condition" for the correction to the planet's parallax, and the ratio of the planet's and the Sun's parallax is known from Kepler's laws [@bes-chauvenet-1863].

## 2004: VT-2004 and the AU

The ESO and IMCCE VT-2004 campaign collected "4550 contact timings ... from 1510 registered observers" of the 2004 June 8 transit and published a final value [@tr-eso-vt2004-results]:

$$
1\ \mathrm{AU} = 149\,608\,708 \pm 11\,835\ \mathrm{km}
$$

which is 10 838 km larger than the value adopted for the predictions, 149 597 870 km, equivalent to a solar parallax of 8.794142 arcseconds [@tr-eso-vt2004-results] [@tr-imcce-vt2004-note1]. The final value rests on a selection that a developer validating predictions must understand. IMCCE's Explanatory Note 2 accepts an observation as "good" if it lies close to the prediction [@tr-imcce-vt2004-note2]:

| Acceptance window | Timings kept | Mean AU (km) | Difference from the adopted AU |
|---|---|---|---|
| ±30 s | 2459 | 148 511 434 | −1 086 436 km |
| ±15 s | 1719 | 148 789 697 | −808 172 km |
| ±8 s | 1066 | 149 421 803 | −176 067 km |
| ±4 s | 583 | 149 608 708 | +10 838 km |

The authors argue that convergence as the window shrinks "confirms that the initial value of the parallax ... used for the predictions is correct" [@tr-imcce-vt2004-note2]. Their quoted ±11 835 km comes from the 583 timings that were selected for agreeing with predictions made with the radar AU. The table is still useful as a validation result. Of 4367 timings in the June 18 dataset, 1066 were within 8 seconds of the prediction and 583 within 4 seconds [@tr-imcce-vt2004-note2]. Timings of third contact gave the worst AU because most observers saw it with the Sun high, so their diurnal parallax was small, and because "the observation of the exact moment of the interior contact T3 is a bit more difficult than that of the external contact T4 because of the Black Drop phenomenon" [@tr-imcce-vt2004-note2].

The sensitivity has a geometric zero. "For a given geometrical contact, all the sites on Earth defined by the intersection of the shadow cone (or penumbra depending on the contact) and the terrestrial ellipsoid will see the contact at the same time as a fictive observer located at the center of the Earth", so a site near that line constrains the AU not at all [@tr-imcce-vt2004-note1]. IMCCE gives the linearised coefficients for first internal contact as $A = 2.1970$, $B = 0.2237$, $C = 1.1206$ and $dD/dt = -2.9394$ arcseconds per minute, in a relation in which $A\cos\phi\cos\lambda + B\cos\phi\sin\lambda + C\sin\phi$ multiplies the parallax correction and equals the rate times the observed-minus-calculated time [@tr-imcce-vt2004-note1]. This note does not reproduce the symbol the note uses for the parallax correction.

Applying [Delisle](https://en.wikipedia.org/wiki/Joseph-Nicolas_Delisle)'s pairing to the ±8 s set, with pairs whose predicted times differ by more than 6 minutes, gave 1 AU = 149 840 958 ± 310 577 km from 4386 pairs [@tr-imcce-vt2004-note2]. Holding the AU fixed and solving for radii instead gave a solar radius of 695 980.7 ± 806 km and a Venus radius of 6052.3 ± 7.0 km [@tr-eso-vt2004-results].

## 2012: Venus, the last for a century

A school network, the Hetu'u Global Network, applied Delisle's method to second and third contacts from 19 groups and obtained 152 ± 30 and 163 ± 30 million km [@tr-faherty-2012]. Space instruments observed the transit. HINODE, SDO, RHESSI and PICARD imaged it, while SOHO at L1 could not [@tr-sigismondi-mg13]. The Venus Twilight Experiment placed coronagraphs at eight sites around the Pacific for multi-wavelength aureole photometry [@tr-xie-2013]. For 2004, Xie and colleagues found that "virtually no chronodated sequences of images of ingress and egress phases are available" [@tr-xie-2013]. Sigismondi found only 50 time-tagged ingress and egress images from Athens [@tr-sigismondi-mg13].

## The solar radius from transits

### The method

A transit chord is a ruler laid across the Sun. If the ephemeris fixes the planet's track, the observed duration between internal contacts measures the solar radius. Emilio and colleagues use the relation of Shapiro (1980),

$$
\Delta R = \frac{\omega^2}{R_\odot}\,T\,\Delta T^{O-C}
$$

where $\omega$ is the planet's speed relative to the Sun, $T$ the total length of the transit, $R_\odot$ the apparent solar radius at 1 au from the ephemeris, for which they adopt 959.645 arcseconds or 696 000 ± 40 km, and $\Delta T^{O-C}$ the observed minus ephemeris duration [@tr-emilio-2012]. Here $\Delta T^{O-C}$ is a duration difference in time, not the Earth-rotation [ΔT](../../10-shared/07-earth-and-time/delta-t-and-earth-rotation.md). The chord geometry of the previous note fixes the coefficient. With $L$ the contact radius, which is close to $R_\odot$ for a small planet, $b$ the least separation and $D = 2\sqrt{L^2 - b^2}/\omega$ the duration, $dD/dL = 2L/(\omega\sqrt{L^2-b^2}) = 4L/(\omega^2 D)$. Hence

$$
\Delta L = \frac{\omega^2 D}{4L}\,\Delta D
$$

for the full duration $D$ and its observed-minus-computed difference $\Delta D$. If $T$ and $\Delta T^{O-C}$ are both half-durations, $D = 2T$ and $\Delta D = 2\Delta T^{O-C}$, and the result is the printed $\omega^2 T\,\Delta T^{O-C}/R_\odot$ with $L \approx R_\odot$. If $T$ is the full duration and $\Delta T^{O-C}$ a full-duration difference, the printed form is four times too large. This coefficient is derived here. Emilio and colleagues do not define $T$ beyond "the total length of the transit" [@tr-emilio-2012]. Sigismondi uses the simpler proportion "Tcalc\Tobs = 959.63"\R" for the times of maximum chord and of contacts [@tr-sigismondi-mg13].

### Results

| Transit | Instrument | Radius at 1 au | Source |
|---|---|---|---|
| 2003 May 7, Mercury | SOHO/MDI | 960.03 ± 0.08″ timing value | [@tr-emilio-2012] |
| 2006 November 8, Mercury | SOHO/MDI | 960.07 ± 0.05″ timing value | [@tr-emilio-2012] |
| 2003 and 2006 combined | SOHO/MDI | 960.12 ± 0.09″ (696 342 ± 65 km) | [@tr-emilio-2012] |
| 2004 June 8, Venus | 583 ground timings, AU held fixed | 695 980.7 ± 806 km | [@tr-eso-vt2004-results] |
| 2012 June 6, Venus | SDO/HMI at 617.3 nm | 959.57 ± 0.02″ (695 946 ± 15 km) | [@tr-emilio-2020] [@sun-emilio-2015] |
| 2016 May 9, Mercury | Visual, 3-inch refractor, Rome | change of −0.12 ± 0.17″ from the reference | [@tr-sigismondi-altafi-2018] |

The 2012 HMI value is after "applying a correction for the instrumental point spread function", and "the difference in the solar radius determined from measurements near the line core and in the continuum wing was 0".23 (167 km)" [@tr-emilio-2020]. The MDI timings came from fits of Mercury's track to the limb at the inflection point of the limb-darkening function, which they define as "the maximum of the LDF derivative squared" [@tr-emilio-2012]. That is the [?inflection-point-radius|inflection-point radius], not the limb of a prediction. Emilio and colleagues argue that the IAU 2015 nominal radius of 695 700 km "is off by more than 300 km" [@tr-emilio-2020]. The 0.55 arcsecond gap between the MDI and HMI results is larger than the gap between the [?canonical-solar-radius|canonical 959.63 arcseconds] and the IAU [?nominal-solar-radius|nominal value]. For a predictor this means that a transit-derived radius carries the instrument's limb definition with it.

Ground timings scatter more. "The average deviation of observations for each transit is typically between 0".5, and 1" on ground observations", and internal contacts "are much more defined than the external ones" [@tr-emilio-2020]. The historical series of more than 2000 Mercury contact timings since the 1720s was used by Parkinson, Morrison and Stephenson and by Shapiro to look for secular change in the radius, and Sveshnikov extended it to 4500 timings since 1631 [@tr-emilio-2020] [@tr-sigismondi-mg13]. Those papers are cited here through Emilio et al. and Sigismondi et al.

## Observed against predicted contact times

The published direct comparisons are few and of mixed quality:

| Transit | Observation | Observed minus predicted | Source |
|---|---|---|---|
| 1861 November 11, Mercury | Egress at Altona, Petersen and Pape | −1.9 s against Chauvenet's prediction | [@bes-chauvenet-1863] |
| 2003 May 7, Mercury | SOHO/MDI contact fits | 8 s offset in absolute [contact times](../04-local-circumstances/contact-times-and-magnitude.md) | [@tr-emilio-2012] |
| 2006 November 8, Mercury | SOHO/MDI contact fits | 5 s offset | [@tr-emilio-2012] |
| 2004 June 8, Venus | 4367 public timings | 1066 within ±8 s, 583 within ±4 s | [@tr-imcce-vt2004-note2] |
| 2016 May 9, Mercury, Rome | Visual projection, contact I | +107 s, 11:13:57 against 11:12:10.3 UTC | [@tr-sigismondi-altafi-2018] |
| 2016 May 9, Mercury, Rome | Visual projection, contact II | +1.7 s, 11:15:23 against 11:15:21.3 UTC | [@tr-sigismondi-altafi-2018] |
| 2016 May 9, Mercury, Tehran | H-alpha, contact I | +2.6 s, 11:11:17 against 11:11:14.4 UTC | [@tr-sigismondi-altafi-2018] |
| 2016 May 9, Mercury, Tehran | H-alpha, contact II | −27.4 s, 11:13:58 against 11:14:25.4 UTC | [@tr-sigismondi-altafi-2018] |
| 2019 November 11, Mercury | None in JOA, the BAA Journal or arXiv | | [@tr-joa-2019] [@tr-baa-2019] |

The MDI offsets were "both inside our 2σ error" [@tr-emilio-2012]. The 2016 predictions were from CalSky, with the Helios program agreeing to 0.1 s [@tr-sigismondi-altafi-2018]. The 107 s late contact I in Rome was attributed to an "effect surprise" and poor contrast in the projected image. The authors estimate the observer's resolution at 3.6 arcseconds from seeing, aperture and eye together [@tr-sigismondi-altafi-2018]. The authors use the Tehran H-alpha timings to estimate the height of the active H-alpha layer at the transit latitude, 1.84 arcseconds, instead of the photospheric radius [@tr-sigismondi-altafi-2018]. Each row therefore tests a different limb definition.

For 2019 the Journal for Occultation Astronomy carried only a pre-event plan, aiming at "0.1" final resolution on the solar limb positioning" with lucky imaging and 0.1 s timing [@tr-joa-2019]. The BAA observer report lists observers and images but records no timings analysis and no black-drop sightings [@tr-baa-2019]. The negative finding covers JOA issues 2019-3, 2019-4 and 2020-1, the BAA report and arXiv. It does not cover analyses of the SDO/HMI images of the 2019 transit outside those venues.

### Space timings: the spacecraft is the observer

A space timing must be predicted for the spacecraft, not for the Earth's centre or a ground site. The observer's position is the spacecraft's state vector, read from its orbit ephemeris such as an [?spk-kernel|SPK kernel], in place of $\rho\sin\phi'$ and $\rho\cos\phi'$. Emilio and colleagues used "the NASA ephemeris calculations provided by NASA for the SOHO Mercury transit observations". They state that the ephemeris uncertainty of the absolute contact times is "not greater than 0.18 s based on the SOHO absolute position error" [@tr-emilio-2012]. SOHO is near the first Lagrangian point L1 [@tr-sigismondi-mg13], and the Sun looks larger from there. Emilio and colleagues give 961.45 arcseconds "as seen from SOHO", which was 0.99876 au from the Sun, against 960.26 arcseconds reduced to 1 au [@tr-emilio-2012].

SDO is in an inclined geosynchronous orbit at an altitude of 35,788 km [@tr-nasa-sdo-eps], which is 6.61 Earth radii from the Earth's centre. The differential parallax grows in proportion to that distance. With the IAA RAS differences of horizontal parallax, SDO's offset displaces Mercury against the Sun by up to about 47 arcseconds in 2016 and 27 arcseconds in 2019. That is 12 and 4.6 minutes of the planet's relative motion. For Venus in 2012, with Espenak's Venus parallax of about 30 arcseconds less the Sun's 8.8 arcseconds, the displacement is up to about 140 arcseconds, or about 35 minutes of relative motion. These figures are computed here [@tr-iaa-2016] [@tr-iaa-2019] [@tr-nasa-venus0412]. A geocentric prediction compared with an SDO timing can therefore be wrong by minutes.

## Pointer: exoplanet transits

The 2004 and 2012 transits were studied "in view of exoplanets with atmosphere in transits over their stars" [@tr-sigismondi-au-2013], and the Venus Twilight Experiment aimed at "good models to interprete the forthcoming observations of extrasolar planets transits with similar properties" [@tr-sigismondi-mg13]. Espenak notes that the 1:32.6 diameter ratio of Venus to the Sun gives "an effective 0.001 magnitude drop in the Sun's integrated magnitude" [@tr-nasa-venus0412]. The analogy is a pointer only. Exoplanet transit modelling is outside this corpus.

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Schneider, Pasachoff and Golub, *Icarus* 2004 [@tr-spg-2004] | The space measurement that fixes the black-drop mechanism, with sizes in arcseconds and kilometres. |
| Tanga et al., *Icarus* 2012 [@tr-tanga-2012] | The only quantitative aureole model, with fitted $H$ and $r$. |
| IMCCE VT-2004 notes [@tr-imcce-vt2004-note1] [@tr-imcce-vt2004-note2] | The largest public set of observed-minus-predicted contact statistics, the per-contact AU analysis and Delisle pairings. |
| IMCCE InfoSheets for ESO [@tr-eso-eis-f2] [@tr-eso-eis-f5] [@tr-eso-eis-b4] | History, parallax values by era, and the two-site parallax geometry. |
| Emilio et al. 2012 and 2020 [@tr-emilio-2012] [@tr-emilio-2020] | Space-based radius from transit timing, with the duration relation, the offset of observed contacts from NASA's ephemeris and predictions made for SOHO's position. |
| Sigismondi and colleagues [@tr-sigismondi-2016] [@tr-sigismondi-altafi-2018] [@tr-sigismondi-mg13] | Ground methods against the black drop and the only 2016 observed-minus-predicted contacts found. |
| Espenak [@tr-nasa-oh2012] [@tr-ew-tm2019] | The operational definition of contact II used in observer instructions. |

## What a developer should do

1. Predict the geometric contact, defined by the limb at the chosen solar radius, and say so. Do not try to predict the black-drop break, which depends on the observer's PSF [@tr-spg-2004].
2. Validate against space data first, with the spacecraft's state vector as the observer. The SOHO/MDI 2003 and 2006 offsets of 8 s and 5 s are the cleanest published residuals [@tr-emilio-2012]. An SDO timing predicted for the Earth's centre can be minutes off [@tr-nasa-sdo-eps]. Ground visual timings scatter by tens of seconds and some differ by more than a minute [@tr-sigismondi-altafi-2018].
3. When comparing with observations, record the observer's limb definition: white-light inflection point, H-alpha chromosphere, or visual thread break [@tr-emilio-2012] [@tr-sigismondi-altafi-2018].
4. When a radius is derived from transit timings, carry its wavelength and limb definition with it. HMI's line-core and continuum radii differ by 0.23 arcseconds [@tr-emilio-2020].
5. To reproduce the VT-2004 analysis, start from IMCCE's Explanatory Note 2 and its acceptance windows. Report results for all windows, because the ±4 s result alone hides the selection [@tr-imcce-vt2004-note2].

## What this changes

The pipeline needs a contact-definition field for transits, as it does for eclipses. A geometric contact at a stated $s_0$ is the product. The black drop and the aureole belong to an observer model and are not corrections to the ephemeris. The validation suite gains space-based transit timings as a solar-radius-sensitive test that does not depend on a lunar [limb profile](../05-lunar-limb/limb-profile-methods.md).

## Open questions

- Emilio et al. (2015), ApJ 798, 48, on the 2012 HMI radius: obtain the paper and record its contact residuals against the ephemeris and which ephemeris it used [@sun-emilio-2015].
- SDO/HMI and AIA data for the 2016 and 2019 Mercury transits: find a published radius or contact-residual analysis. None is in arXiv, JOA 2019 to 2020 or the BAA report [@tr-joa-2019] [@tr-baa-2019].
- Shapiro (1980), *Science* 208, 51: obtain the paper to confirm whether $T$ in the duration relation quoted by Emilio et al. is the half-duration, as the derived coefficient requires [@tr-emilio-2012].
- Schaefer (2001), *Journal for the History of Astronomy* 32, 325, on the black drop: obtain it to record its diffraction calculation, which Schneider et al. say underestimated edge diffraction [@tr-spg-2004].
- Halley (1716), *Philosophical Transactions* 29, 454: obtain the original to quote his method and his expected precision directly, instead of through later summaries [@tr-faherty-2012].
- Hauchecorne et al. (2014), ApJ, on the 2012 transit with PICARD/SODISM and HMI: obtain it to compare its radius with Emilio et al.'s 959.57 arcseconds [@tr-emilio-2020].
