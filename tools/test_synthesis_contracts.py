"""Source-backed numerical and API contracts in the implementable reports.

The numerical fixtures evaluate the equations printed in the pipeline, rather
than an unrelated reference implementation. Constants and conventions come
from the Explanatory Supplements, NASA JSEX and NAIF's API documentation.
"""

import math
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def arithmetic(expression):
    expression = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", expression)
    expression = expression.replace(r"\times", "*").replace(r"\,", "")
    if not re.fullmatch(r"[0-9.()+*/\s-]+", expression):
        raise AssertionError(f"Unsupported dimensional coefficient: {expression}")
    return eval(expression, {"__builtins__": {}}, {})


class SynthesisContracts(unittest.TestCase):
    def setUp(self):
        self.pipeline = text("content/20-reports/pipeline-design.md")

    def test_hour_angle_converts_seconds_to_degrees_once(self):
        match = re.search(r"\$\\theta = \\mu\(t\) - \\lambda(?:_W)? - (.*?)\\,?\\Delta T\$",
                          self.pipeline, re.S)
        self.assertIsNotNone(match, "The local hour angle must state its conversion coefficient")
        coefficient = arithmetic(match[1])
        # 69 seconds at the published sidereal rotation rate, in degrees.
        self.assertAlmostEqual(coefficient * 69, 0.288287175, places=10)

    def test_observer_radius_is_reduced_from_fundamental_plane_only_once(self):
        match = re.search(r"L_2' = ([lL]_2) - \\zeta\\tan f_2", self.pipeline)
        self.assertIsNotNone(match)
        fundamental = -0.01
        height_correction = 0.00465
        values = {"l_2": fundamental, "L_2": fundamental - height_correction}
        self.assertAlmostEqual(values[match[1]] - height_correction, -0.01465)

    def test_total_duration_is_positive_with_signed_umbral_radius(self):
        match = re.search(r"Central duration \$([^$]+)\$", self.pipeline)
        self.assertIsNotNone(match)
        expression = match[1].split("=")[-1].strip()
        radius, speed = -0.01, 0.5
        expression = expression.replace("|L_2|", "*(" + str(abs(radius)) + ")")
        expression = expression.replace("L_2", "*(" + str(radius) + ")").replace("n", str(speed))
        self.assertAlmostEqual(arithmetic(expression) * 3600, 144.0)

    def test_lens_angle_labels_reproduce_unequal_disc_overlap(self):
        solar_radius, lunar_radius, separation = 1.0, 1.1, 0.2
        solar = math.acos((separation**2 + solar_radius**2 - lunar_radius**2) /
                          (2 * separation * solar_radius))
        lunar = math.acos((separation**2 + lunar_radius**2 - solar_radius**2) /
                          (2 * separation * lunar_radius))
        intersection = math.pi - solar - lunar
        if "$B$ and $C$ the angles at the solar" in self.pipeline:
            angle_a, angle_b, angle_c = intersection, solar, lunar
        else:
            self.assertIn("$A$ at the lunar centre", self.pipeline)
            self.assertIn("$B$ at the solar centre", self.pipeline)
            self.assertIn("$C$ at either intersection", self.pipeline)
            angle_a, angle_b, angle_c = lunar, solar, intersection
        area = (lunar_radius**2 * angle_a + angle_b -
                lunar_radius * math.sin(angle_c)) / math.pi
        self.assertAlmostEqual(area, 0.9543524098080188, places=10)

    def test_datum_conversion_preserves_the_physical_radius(self):
        datum, equatorial_radius, k = 1737.4, 6378.137, 0.2725076
        height = 0.2
        difference = equatorial_radius * k - datum
        if "constant to add only" in self.pipeline:
            converted = height + difference
        else:
            self.assertIn("subtract 0.6908 km", self.pipeline)
            converted = height - difference
        self.assertAlmostEqual(datum + height, equatorial_radius * k + converted)

    def test_spice_experiment_respects_finite_disc_shape_constraints(self):
        questions = text("content/20-reports/open-questions.md")
        self.assertIn("does not support a DSK Moon paired with an ellipsoid Sun", questions)
        self.assertIn("ANY", questions)

    def test_uncertainty_recipe_distinguishes_covariance_and_bias(self):
        budget = text("content/20-reports/error-budget.md")
        self.assertNotIn("Sum the rows that apply in quadrature", budget)
        self.assertIn("covariance", budget)
        self.assertIn("independence", budget)

    def test_summaries_do_not_claim_universal_besselian_or_ground_truth(self):
        for path in ("content/_index.md", "content/20-reports/executive-summary.md",
                     "content/05-primer/worked-example-solar-eclipse.md"):
            page = text(path)
            self.assertNotIn("Every published eclipse product derives from one algorithm", page)
            self.assertNotIn("One algorithm underlies every eclipse product", page)
            self.assertNotIn("Every map and every table is derived from those eight numbers", page)
        self.assertNotIn("only public ground truth", text("content/20-reports/executive-summary.md"))

    def test_refraction_does_not_carry_an_unvalidated_timing_bound(self):
        budget = text("content/20-reports/error-budget.md")
        self.assertNotIn("10 to 80 s", budget)
        self.assertNotIn("optional flagged C1 and C4 adjustment", self.pipeline)

    def test_maximum_product_uses_its_actual_objective(self):
        self.assertIn("Closest approach is a search seed", self.pipeline)
        # Synthetic disc sizes: the smallest separation need not maximise
        # covered diameter when the solar angular radius varies with time.
        def magnitude(time):
            solar, lunar, distance = 1 + 0.2*time, 1, 0.2 + time*time
            return (solar + lunar - distance) / (2*solar)
        self.assertGreater(magnitude(-0.05), magnitude(0))

    def test_catalogue_gamma_preserves_its_north_south_sign(self):
        self.assertIn("with the sign of $y$", self.pipeline)
        x, y = 0.3, -0.4
        signed_gamma = math.copysign(math.hypot(x, y), y)
        self.assertEqual(signed_gamma, -0.5)

    def test_unquantified_ephemeris_pair_is_not_plotted_as_a_bound(self):
        budget = text('content/20-reports/error-budget.md')
        row = next(line for line in budget.splitlines() if '| 20 |' in line)
        self.assertNotIn('Sub-metre', row)
        self.assertIn('not quantified', row)
        figure = text('tools/figures/error_budget.py')
        self.assertNotRegex(figure, r'\(20,.*DE421')


if __name__ == "__main__":
    unittest.main()
