"""Scientific fixtures and contracts for the geometry/time research notes.

These test the equations and their published instructions, not an eclipse solver.
NASA fixtures: 2024 SEbeselm table and SEcat5/uncertainty.html (2007-02-07).
Ellipsoid fixture: WGS84 and Stellarium 69888f4f47af2aa4d1c9d14ec3853e874e253c73.
"""
import math
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "content/10-raw"


def note(topic, name):
    return (RAW / topic / name).read_text(encoding="utf-8")


class GeometryTimeContracts(unittest.TestCase):
    def test_delta_t_longitude_direction_at_fixed_tt(self):
        text = note("07-earth-and-time", "delta-t-and-earth-rotation.md")
        # Bind the published east-positive equation to the consumer's actual sign.
        self.assertIn(r"\delta\lambda_E = +\omega_\oplus\delta T", text,
                      "An increased Delta T must shift fixed-TT east longitude eastward")
        self.assertIn(r"\delta\lambda_W = -\omega_\oplus\delta T", text)
        self.assertNotIn("465 m too far west", text)
        self.assertIn(r"\delta t_{\mathrm{UT1}}=-\delta T", text)
        # NASA 2024 t0 mu fixture; H stays fixed when the TT geometry stays fixed.
        mu_deg, h_deg = 89.59122, 25.0
        omega_deg_per_s = 1.002738 * 15 / 3600
        west = [mu_deg - omega_deg_per_s * dt - h_deg for dt in (69, 70)]
        east = [-longitude for longitude in west]
        self.assertAlmostEqual(west[1] - west[0], -0.004178075, places=12)
        self.assertAlmostEqual(east[1] - east[0], +0.004178075, places=12)
        # Geographical displacement of the same point along the equator.
        shift_m = math.radians(east[1] - east[0]) * 6378137
        self.assertAlmostEqual(shift_m, 465.1011814961, places=5)
        tt_s = 18 * 3600
        self.assertEqual((tt_s - 70) - (tt_s - 69), -1)

    def test_nasa_hour_angle_single_correction(self):
        text = note("01-foundations", "ephemeris-to-elements.md")
        self.assertIn("NASA ephemeris-meridian", text)
        self.assertIn("as if it were UT1", text)
        self.assertIn("already contains", text)
        self.assertNotIn("To match NASA, evaluate", text)
        delta = 70.6
        # JSEX converts seconds to radians with the printed 13713.44 factor.
        from_jsex = math.degrees(delta / 13713.44)
        explicit_degrees = delta * (1.002738 * 15 / 3600)
        self.assertAlmostEqual(from_jsex, explicit_degrees, delta=1e-7)
        self.assertAlmostEqual(explicit_degrees, 0.294972095, places=10)

    def test_nasa_six_hour_sample_grid(self):
        text = note("01-foundations", "ephemeris-to-elements.md")
        self.assertIn("t = -3, -1.5, 0, +1.5, +3", text)
        grid = [-3, -1.5, 0, 1.5, 3]
        self.assertEqual(grid[-1] - grid[0], 6)
        self.assertEqual([b - a for a, b in zip(grid, grid[1:])], [1.5] * 4)

    def test_ellipsoid_transformed_norm_and_document_equation(self):
        text = note("03-global-circumstances", "path-and-limits.md")
        self.assertIn(r"\zeta_1 = [\zeta/\rho_2 + \eta_1\sin(d_1-d_2)]/\cos(d_1-d_2)", text)
        f = 1 / 298.257223563
        e2 = f * (2 - f)
        phi, d = map(math.radians, (45, 23))
        c = 1 / math.sqrt(1 - e2 * math.sin(phi) ** 2)
        rs, rc = (1 - e2) * c * math.sin(phi), c * math.cos(phi)
        eta, zeta = rs * math.cos(d) - rc * math.sin(d), rs * math.sin(d) + rc * math.cos(d)
        r1, r2 = math.sqrt(1 - e2 * math.cos(d) ** 2), math.sqrt(1 - e2 * math.sin(d) ** 2)
        sdd, cdd = e2 * math.sin(d) * math.cos(d) / (r1 * r2), math.sqrt(1 - e2) / (r1 * r2)
        eta1 = eta / r1
        zeta1 = (zeta / r2 + eta1 * sdd) / cdd
        self.assertAlmostEqual(eta1 ** 2 + zeta1 ** 2, 1, places=14)
        # Preserve the counterexample to the omitted rotation.
        self.assertAlmostEqual(eta1 ** 2 + (zeta / r2) ** 2, 0.9983276534549561, places=14)

    def test_positive_duration_and_correct_optimiser(self):
        text = note("03-global-circumstances", "path-and-limits.md")
        self.assertIn(r"D = 2|L_2|/n", text)
        self.assertIn("C3 minus C2", text)
        candidates = [-0.01, -0.02]
        self.assertEqual(max(candidates, key=lambda radius: 2 * abs(radius) / 0.5), -0.02)
        self.assertEqual(max(candidates, key=lambda radius: 2 * radius / 0.5), -0.01)
        self.assertIn(r"2|L_2|/n", note("03-global-circumstances", "data-products-and-code.md"))

    def test_huber_examples_from_published_formula(self):
        text = note("02-catalogs", "enumerating-eclipses.md")
        self.assertIn("3,732 s at −2000 and 16,291 s at −4000", text)
        def sigma(n):
            return 365.25 * n * math.sqrt(n * 0.058 / 3 * (1 + n / 2500)) / 1000
        for n, expected in [(1500, 3731.990022), (3500, 16291.132706), (495, 612.180937)]:
            self.assertAlmostEqual(sigma(n), expected, delta=1e-5)
        earth = note("07-earth-and-time", "delta-t-and-earth-rotation.md")
        self.assertIn("612 s at +2500", earth)
        self.assertNotIn("grows as the square", earth)

    def test_dut1_conversion_sign(self):
        text = note("07-earth-and-time", "delta-t-and-earth-rotation.md")
        instructions = text.split("## What a developer should do")[1]
        self.assertIn("subtract DUT1 when printing UTC", instructions)
        dut1 = 69.184 - 68.8373
        ut1_seconds = 12 * 3600
        utc_seconds = ut1_seconds - dut1
        self.assertAlmostEqual(utc_seconds + dut1, ut1_seconds, places=10)
        self.assertAlmostEqual(dut1, 0.3467, places=10)

    def test_vertex_and_track_width_contract(self):
        text = note("02-catalogs", "types-and-classification.md")
        self.assertIn("negative when the umbral vertex lies below", text)
        self.assertIn("perpendicular to the direction of ground motion", text)
        self.assertIn("major-axis approximation", text)
        # NASA 2024 l2 and tan(f2): c2=l2/tan(f2) puts vertex below plane.
        c2 = -0.010274 / 0.0046450
        self.assertLess(c2, 0)
        self.assertLess(-0.010274 - 1 * 0.0046450, 0)

    def test_refraction_bounds_and_light_time_mechanism(self):
        text = note("07-earth-and-time", "refraction-light-time-and-frames.md")
        self.assertNotIn("roughly a quarter", text)
        self.assertNotRegex(text, r"(?:20 s and 80 s|10 to 80 s|under 1 m for DE440)")
        self.assertIn("one-to-one", text)
        self.assertIn(r"\mathbf{T}(t-\tau)-\mathbf{O}(t)", text)
        self.assertIn("observer's barycentric velocity", text)
        self.assertNotIn("together cost less than", note("07-earth-and-time", "_index.md"))

    def test_glossary_uses_same_time_contract(self):
        foundations = note("01-foundations", "terms.tsv")
        self.assertNotIn("bake ΔT into it", foundations)
        self.assertIn("NASA's tabulated μ requires this correction once", foundations)
        earth = note("07-earth-and-time", "terms.tsv")
        self.assertIn("Subtract UT1 − UTC", earth)
        self.assertIn("numerical TT epoch as if it were UT1", earth)

    def test_track_width_depends_on_motion_direction(self):
        text = note("03-global-circumstances", "path-and-limits.md")
        self.assertIn(r"2|L_2|/\zeta", text)
        # Same spherical surface point, same footprint, different track direction.
        x, zeta, radius = 0.6, 0.8, 0.01
        width_along_tilt = 2 * radius / math.sqrt(zeta**2 + x**2)
        width_across_tilt = 2 * radius / zeta
        self.assertAlmostEqual(width_along_tilt, 0.02, places=14)
        self.assertAlmostEqual(width_across_tilt, 0.025, places=14)
        self.assertNotEqual(width_along_tilt, width_across_tilt)

    def test_maximum_product_is_not_closest_approach(self):
        text = note("03-global-circumstances", "global-maps-and-contours.md")
        self.assertIn("time-dependent apparent radii", text)
        # Dimensionless synthetic two-disc geometry: separation minimum at t=0.
        # Solar radius changes with t, so normalised magnitude is larger earlier.
        def magnitude(t):
            rs, rm, separation = 1 + 0.2 * t, 1, 0.2 + t*t
            return (rs + rm - separation) / (2 * rs)
        self.assertLess(0.2, 0.2 + 0.05**2)
        self.assertGreater(magnitude(-0.05), magnitude(0))

    def test_noncentral_and_contour_objective_contracts(self):
        gis = note("03-global-circumstances", "data-products-and-code.md")
        self.assertNotIn("If $p < 0$ skip the time", gis)
        self.assertIn("Continue the limit and outline", gis)
        contours = note("03-global-circumstances", "global-maps-and-contours.md")
        self.assertIn("optimise the quantity being contoured", contours)
        self.assertIn("Maximum magnitude and maximum obscuration need not", contours)


if __name__ == "__main__":
    unittest.main()
