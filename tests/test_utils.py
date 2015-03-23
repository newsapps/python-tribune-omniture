import unittest

from tribune_omniture.utils import property_abbrev, to_camelcase, slugify

class UtilsTestCase(unittest.TestCase):
    def test_to_camelcase(self):
        self.assertEqual(to_camelcase('page_name'), 'pageName')
        self.assertEqual(to_camelcase('prop1'), 'prop1')
        self.assertEqual(to_camelcase(''), '')

    def test_property_abbrev(self):
        test_vals = [
            ('LA Times', 'lat'),
            ('Chicago Tribune', 'ct'),
            ('Morning Call', 'amc'),
            ('Orlando Sentinel', 'os'),
            ('Hartford Courant', 'hc'),
            ('Sun-Sentinel', 'sfss'),
            ('Baltimore Sun', 'bs'),
            ('Daily Press', 'hrdp'),
        ]
        for prop, abbrev in test_vals:
            self.assertEqual(property_abbrev(prop), abbrev)

    def test_slugify(self):
        test_vals = [
            ('Home Page', 'Home-Page'),
        ]

        for title, slug in test_vals:
            self.assertEqual(slugify(title), slug)
