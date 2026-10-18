"""Scientific regression demonstrations tied to the published note contracts.

All geometry fixtures are synthetic, not observed eclipse measurements.
Original evidence: Herald (1983) pp. 242–243, NASA JSEX getduration(),
NAIF gfoclt_c Detailed_Input, SunPy 8.0 eclipse_amount and Astropy 8.0.1.
"""
import ast
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def note(topic, name):
    found = [d for d in (ROOT / 'content/10-raw').rglob(topic) if d.is_dir()]
    assert len(found) == 1, (topic, found)
    return (found[0] / name).read_text(encoding='utf-8')


def lens_fraction(rs, rm, separation):
    if separation >= rs + rm:
        return 0.0
    if separation <= abs(rs - rm):
        return min(1.0, (rm / rs) ** 2)
    a = math.acos((separation**2 + rm**2 - rs**2) / (2 * separation * rm))
    b = math.acos((separation**2 + rs**2 - rm**2) / (2 * separation * rs))
    triangle = math.sqrt((-separation+rs+rm)*(separation+rs-rm)*
                         (separation-rs+rm)*(separation+rs+rm)) / 2
    return (rm**2*a + rs**2*b - triangle) / (math.pi * rs**2)


class LocalLimbModels(unittest.TestCase):
    def assertIn(self, member, container, msg=None):
        self.assertTrue(member in container, msg or f'Missing documented contract: {member}')

    def assertNotIn(self, member, container, msg=None):
        self.assertFalse(member in container, msg or f'Obsolete documented contract: {member}')

    def test_datum_shift_preserves_physical_radius(self):
        almanac_radius = 6378.137 * 0.2725076
        point_radius = 1737.9
        h_dem = point_radius - 1737.4
        h_almanac = h_dem - (almanac_radius - 1737.4)
        self.assertAlmostEqual(almanac_radius, 1738.0908063412, places=10)
        self.assertAlmostEqual(almanac_radius + h_almanac, point_radius, places=10)
        self.assertLess(h_almanac, 0)
        text = note('05-lunar-limb', 'datasets-watts-kaguya-lola.md')
        self.assertIn('subtract 0.6908 km', text)

    def test_signed_valley_and_grazing_rates(self):
        # Solar limb measured outward from lunar centre: entry shrinks,
        # exit grows. A valley of -0.2 arcseconds changes the times oppositely.
        height = -0.2
        entry_rate, exit_rate = -0.4, 0.4
        self.assertEqual(height / entry_rate, 0.5)
        self.assertEqual(height / exit_rate, -0.5)
        v, theta, motion = 0.4, 0.0, math.radians(89)
        radial_rate = v * math.cos(theta - motion)
        self.assertGreater(abs(height / radial_rate), 28)
        self.assertLess(radial_rate, v / 50)
        # The old contact-direction projection produces v at theta=X.
        old_rate = v * math.cos(theta - theta)
        self.assertGreater(old_rate / radial_rate, 50)
        methods = note('05-lunar-limb', 'limb-profile-methods.md')
        self.assertIn(r'\dot g_i \approx v\cos(\theta_i-N)', methods)
        self.assertIn(r'\alpha_i-g_i(T_0)', methods)
        self.assertNotIn(r'v\cos(X - \theta_i)', methods)
        correction = note('04-local-circumstances', 'corrections-and-code.md')
        self.assertIn('a valley delays C2 and advances C3', correction)

    def test_herald_inward_departure_is_not_dem_outward_height(self):
        rs, rm, angle = 960.0, 1008.0, math.radians(30)
        separation = rm - rs
        g = separation*math.cos(angle) + math.sqrt(rs**2 - separation**2*math.sin(angle)**2)
        outward_departure = g - rm
        herald_inward = rs * (rm/rs - 1) * (1-math.cos(angle))
        self.assertLess(outward_departure, 0)
        self.assertGreater(herald_inward, 0)
        self.assertLess(abs(outward_departure + herald_inward), 0.31)
        methods = note('05-lunar-limb', 'limb-profile-methods.md')
        self.assertIn('inward solar-limb departure', methods)
        self.assertIn(r'\Delta_i+h_i', methods)

    def test_bead_figure_translates_inward_chart_height(self):
        # Load only the real figure's constants/functions, without its render
        # side effect. The consumer must subtract positive inward departure.
        path = ROOT / 'tools/figures/bailys_beads.py'
        tree = ast.parse(path.read_text(encoding='utf-8'))
        keep = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in {'rise', 'sun'}:
                keep.append(node)
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id in {'S0', 'MAG'}
                for target in node.targets
            ):
                keep.append(node)
        scope = {'math': math}
        exec(compile(ast.Module(keep, type_ignores=[]), str(path), 'exec'), scope)
        self.assertLess(scope['sun'](30, 0), 0)
        self.assertAlmostEqual(scope['sun'](30, 0), -scope['rise'](30))

    def test_lusaka_published_signed_displacements(self):
        # NASA TP-1999-209484 section 1.14 gives chart-read time
        # corrections, not digitised valley heights. Preserve exactly what
        # is published; do not invent a profile to recreate the chart.
        c2 = 13*3600 + 9*60 + 19.3
        c3 = 13*3600 + 12*60 + 32.8
        self.assertAlmostEqual(c2 + 4.0, 13*3600 + 9*60 + 23.3)
        self.assertAlmostEqual(c3 - 1.2, 13*3600 + 12*60 + 31.6)
        self.assertAlmostEqual((c3 - 1.2) - (c2 + 4.0), 188.3)
        methods = note('05-lunar-limb', 'limb-profile-methods.md')
        self.assertIn('13:09:23.3 UT', methods)
        self.assertIn('13:12:31.6 UT', methods)

    def test_magnitude_branch_discontinuity_and_obscuration_order(self):
        l1, l2 = 1.0, -0.025
        self.assertEqual((l1-abs(l2))/(l1+l2), 1.0)
        self.assertAlmostEqual((l1-l2)/(l1+l2), 1.0512820512820513)
        self.assertAlmostEqual(lens_fraction(1, 1, 1), 0.39100221895577075)
        self.assertAlmostEqual(lens_fraction(1, 1.05, 0.07), 0.993327525274487, places=10)
        self.assertGreater(lens_fraction(1, 1.05, 0.07), 0.99)
        text = note('04-local-circumstances', 'contact-times-and-magnitude.md')
        self.assertIn('switches convention', text)
        self.assertIn('With unequal radii that ordering need not hold', text)

    def test_obscuration_plateaus_do_not_define_annular_roots(self):
        self.assertEqual(lens_fraction(1, 1.1, 2.2), 0)
        self.assertEqual(lens_fraction(1, 1.1, 3.0), 0)
        self.assertEqual(lens_fraction(1, 1.1, 0.05), 1)
        self.assertEqual(lens_fraction(1, 1.1, 0.0), 1)
        self.assertAlmostEqual(lens_fraction(1, 0.9, 0.0), 0.81)
        text = note('04-local-circumstances', 'topocentric-method.md')
        self.assertIn('percentage from 0 to 100', text)
        self.assertIn(r'\delta-|r_s-r_m|=0', text)
        self.assertIn('plateaus', text)

    def test_closest_approach_is_scoped_as_a_product_search_seed(self):
        text = note('04-local-circumstances', 'contact-times-and-magnitude.md')
        self.assertIn('closest approach is a search seed', text)
        self.assertNotIn('this is when $m^2$ is a minimum', text)
        index = note('04-local-circumstances', '_index.md')
        self.assertNotIn('for maximum eclipse', index.split('## What this topic covers')[0])

    def test_source_backed_api_contracts(self):
        topocentric = note('04-local-circumstances', 'topocentric-method.md')
        self.assertIn('DSK support requires the other target to be POINT', topocentric)
        self.assertIn('ANY', topocentric)
        ephemerides = note('08-lunar-and-solar-model', 'ephemerides.md')
        self.assertIn('`erfa.ab()`', ephemerides)
        self.assertIn('v8.0.1', ephemerides)
        self.assertNotIn("astropy's \"apparent\" is the almanac's astrometric place", ephemerides)
        self.assertIn('target at emission time and the observer at reception time', ephemerides)
        self.assertIn('separate annual aberration', ephemerides)

    def test_moon_to_observer_vector_selects_visible_hemisphere(self):
        moon, observer = (2, 3, 4), (10, 3, 4)
        vector = tuple(o-m for o, m in zip(observer, moon))
        opposite = tuple(m-o for o, m in zip(observer, moon))
        lon = math.atan2(vector[1], vector[0])
        wrong_lon = math.atan2(opposite[1], opposite[0])
        self.assertEqual(lon, 0)
        self.assertEqual(abs(wrong_lon-lon), math.pi)
        text = note('08-lunar-and-solar-model', 'lunar-figure-and-libration.md')
        self.assertNotIn('observer-to-Moon vector', text)
        self.assertIn('Moon-to-observer vector', text)
        self.assertIn('Moon-to-Earth', note('08-lunar-and-solar-model', 'refs.tsv'))

    def test_formatter_units_and_symbol_contract(self):
        self.assertAlmostEqual((0.05/60)*60, 0.05)
        self.assertEqual(math.floor(12.96 + 0.05), 13)
        self.assertEqual(math.floor(12.94 + 0.05), 12)
        text = note('04-local-circumstances', 'contact-times-and-magnitude.md')
        self.assertIn('0.05/60 minutes, or 0.05 seconds', text)
        self.assertIn(r'q_{\mathrm{par}}', text)
        self.assertIn(r'C_{\mathrm{ell}}', text)
        self.assertIn('between the Moon and its vertex', text)
        self.assertIn(r'(1.002738\times15/3600)', text)

    def test_surface_mean_does_not_fix_silhouette_maximum(self):
        # Equal global averages with different directional maxima.
        first, second = [0, 0, 2, 2], [1, 1, 1, 1]
        self.assertEqual(sum(first)/len(first), sum(second)/len(second))
        self.assertNotEqual(max(first), max(second))
        text = note('05-lunar-limb', 'datasets-watts-kaguya-lola.md')
        self.assertIn('cannot be inferred from the global mean radius', text)


if __name__ == '__main__':
    unittest.main()
