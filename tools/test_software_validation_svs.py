"""Source and numerical contracts for corrected research recommendations.

Fixtures identify published inputs, not a second implementation of the eclipse
pipeline. Contract checks read the actual notes consumed by the site build.
"""
import math
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "content/10-raw"


def topic_dir(topic):
    """A topic folder by name, wherever its group puts it."""
    found = [p for p in RAW.rglob(topic) if p.is_dir()]
    assert len(found) == 1, (topic, found)
    return found[0]


def note(topic, name):
    return (topic_dir(topic) / name).read_text(encoding="utf-8")


class SoftwareValidationSVSContracts(unittest.TestCase):
    def test_spice_supported_shapes_in_recommendation(self):
        # NAIF gfoclt_c Detailed_Input and Exceptions 9/14.
        text = note("09-software-and-repos", "open-source-libraries.md")
        self.assertIn("DSK with POINT supports ANY only", text)
        self.assertIn("cannot directly", text)
        self.assertNotIn("only off-the-shelf route to limb-shaped contact", text)

    def test_stellarium_axis_is_an_approximation(self):
        # Pinned SolarEclipseComputer.cpp:584-587; exact vector comparison.
        b, am, dm = 0.00257, math.radians(1), math.radians(0.5)
        approx = -b * math.cos(dm) * am / (1 - b)
        exact = math.atan2(-b * math.cos(dm) * math.sin(am),
                           1 - b * math.cos(dm) * math.cos(am))
        difference = math.degrees(approx - exact) * 3600
        self.assertAlmostEqual(difference, -0.000475461, places=9)
        text = note("09-software-and-repos", "open-source-libraries.md")
        self.assertIn("small-separation angular approximation", text)
        self.assertNotIn("algebraically the same construction", text)

    def test_program_s0_is_a_length(self):
        text = note("09-software-and-repos", "open-source-libraries.md")
        equation = next(line for line in text.splitlines() if "d_0 =" in line)
        self.assertNotIn("s_0", equation)
        self.assertIn("z_M", equation)

    def test_distinct_nasa_coefficient_runs(self):
        text = note("09-software-and-repos", "commercial-and-institutional-tools.md")
        # NASA SEbeselm 2024 versus Canon/Jubier x0, Earth-radius units.
        self.assertAlmostEqual(abs(-0.318157 - -0.31824401), 0.00008701)
        self.assertIn("both polynomial coefficients and ΔT", text)
        self.assertNotIn("Only the ΔT is Jubier", text)

    def test_independent_element_origin(self):
        text = note("09-software-and-repos", "github-repositories.md")
        self.assertIn("independently fitted DE440s elements", text)
        self.assertNotIn("so it generates elements rather than copying", text)

    def test_photo_ephemeris_contacts_are_smooth(self):
        text = note("09-software-and-repos", "_index.md")
        self.assertIn("smooth-Moon contact tables", text)
        self.assertIn("separate limb-aware bead simulator", text)

    def test_2017_archive_cadence(self):
        text = note("09-software-and-repos", "datasets.md")
        row = next(line for line in text.splitlines() if "| SVS 2017 GIS" in line)
        self.assertIn("10 min and 1 min", row)
        self.assertIn("1 s umbra", row)

    def test_time_scales_before_subsecond_comparisons(self):
        # USNO monthly ΔT at 2017-08-01, illustrative rather than event EOP.
        dut1 = 32.184 + 37 - 68.8373
        self.assertAlmostEqual(dut1, 0.3467, places=10)
        self.assertGreater(dut1, 0.1)
        self.assertGreater(dut1, 0.2)
        for filename in ("observed-vs-predicted.md", "error-budget-and-validation-protocol.md"):
            text = note("10-validation", filename)
            self.assertIn("UTC = UT1 − DUT1", text)
            self.assertIn("event", text)
            self.assertNotIn("below every tolerance", text)

    def test_error_budget_is_not_a_list_of_sigmas(self):
        for topic, filename in (("10-validation", "error-budget-and-validation-protocol.md"),
                                ("06-solar-radius", "effect-on-eclipse-products.md")):
            text = note(topic, filename)
            self.assertIn("covariance", text)
            self.assertNotIn("three independent errors", text)
            self.assertNotIn("physical floor", text)

    def test_overexposure_has_no_universal_signed_correction(self):
        text = note("10-validation", "observed-vs-predicted.md")
        self.assertIn("does not supply a general correction for overexposure", text)
        self.assertNotIn("Overexposure makes faint beads", text)

    def test_stephenville_cross_program_attribution(self):
        text = note("10-validation", "observed-vs-predicted.md")
        self.assertAlmostEqual(57.4 - 24.5, 32.9)
        self.assertAlmostEqual(24.5 - 12.9, 11.6)
        self.assertIn("does not isolate", text)
        self.assertNotIn("Adding the larger radius removes the remaining", text)

    def test_svs_sampling_is_not_terrestrial_accuracy(self):
        # Wright/Young 18,000 angular bins on the 1737.4 km lunar datum.
        metres = 1737.4 * 1000 * math.radians(0.02)
        self.assertAlmostEqual(metres, 606.467008, places=5)
        for filename in ("_index.md", "wright-2024-paper.md", "svs-vs-other-predictors.md"):
            text = note("11-svs-wright", filename)
            self.assertNotIn("resolution floor at about 600 m", text)
            self.assertNotIn("Negligible at the 600 m", text)
            self.assertIn("sampling interval", text)

    def test_svs_radius_conversion_uses_fixed_au(self):
        text = note("11-svs-wright", "svs-products-and-data.md")
        for function, expected in ((math.atan, 959.634), (math.asin, 959.645)):
            value = math.degrees(function(696000 / 149597870.7)) * 3600
            self.assertEqual(round(value, 3), expected)
            self.assertIn(str(expected), text)
        self.assertIn("arctangent", text)
        self.assertIn("arcsine", text)
        self.assertNotIn("change in the au", text)

    def test_broken_annular_criterion_preserves_source_status(self):
        text = note("11-svs-wright", "wright-2024-paper.md")
        self.assertIn("common angular normalisation", text)
        self.assertIn("not observationally validated", text)

    def test_negative_claims_are_scoped(self):
        for topic in ("09-software-and-repos", "10-validation", "11-svs-wright"):
            text = "\n".join(path.read_text(encoding="utf-8") for path in topic_dir(topic).glob("*.md"))
            for phrase in ("No public code exists", "only ground truth", "Only edge observations test", "Nobody has published a complete error budget"):
                self.assertNotIn(phrase, text)

    def test_ephemeris_comparison_is_not_certified_by_range_residuals(self):
        text = note("10-validation", "predictor-disagreements.md")
        self.assertNotIn("difference is under a metre", text)
        text = note("11-svs-wright", "_index.md")
        self.assertNotIn("not from the ephemeris", text)

    def test_source_provenance_and_remaining_questions_agree(self):
        text = note("10-validation", "predictor-disagreements.md")
        self.assertNotIn("Obtain the parameter table image", text)
        self.assertNotIn("Verify or discard the search-summary", text)
        text = note("06-solar-radius", "solar-radius-values.md")
        self.assertNotIn("Jubier et al. 2021 and Guhl 2023 | not stated", text)

    def test_owned_citations_resolve_against_topic_fragments(self):
        refs = {line.split("\t")[0] for path in (ROOT / "content").rglob("refs.tsv")
                for line in path.read_text(encoding="utf-8").splitlines()}
        for topic in ("06-solar-radius", "09-software-and-repos", "10-validation", "11-svs-wright"):
            for path in topic_dir(topic).glob("*.md"):
                for key in re.findall(r"\[@([^\]]+)\]", path.read_text(encoding="utf-8")):
                    self.assertIn(key, refs, str(path))

    def test_profile_spacing_explanation_is_not_duplicated(self):
        text = note("11-svs-wright", "wright-2024-paper.md")
        self.assertEqual(text.count("The 0.02-degree spacing corresponds"), 1)

    def test_glossary_keeps_fits_and_proposed_criterion_scoped(self):
        text = note("06-solar-radius", "terms.tsv")
        self.assertIn("detection model", text)
        text = note("11-svs-wright", "terms.tsv")
        self.assertIn("common angular normalisation", text)
        self.assertIn("not observationally validated", text)

    def test_bias_correction_uncertainty_is_retained(self):
        # GUM equation 13 includes covariance. Two 100 m contributions
        # have 200 m combined uncertainty when fully positively correlated.
        self.assertEqual(math.sqrt(100**2 + 100**2 + 2*100*100), 200)
        for topic, filename in (("10-validation", "error-budget-and-validation-protocol.md"),
                                ("06-solar-radius", "effect-on-eclipse-products.md")):
            text = note(topic, filename)
            self.assertIn("uncertainty of the correction", text)
            self.assertIn("Type B", text)
            self.assertIn("[@report-jcgm-gum-2008]", text)


if __name__ == "__main__":
    unittest.main()
