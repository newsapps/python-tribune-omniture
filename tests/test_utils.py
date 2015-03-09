import unittest

from tribune_omniture.utils import to_camelcase

class UtilsTestCase(unittest.TestCase):
    def test_to_camelcase(self):
        self.assertEqual(to_camelcase('page_name'), 'pageName')
        self.assertEqual(to_camelcase('prop1'), 'prop1')
        self.assertEqual(to_camelcase(''), '')