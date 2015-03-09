import unittest

from tribune_omniture import base

class BaseTestCase(unittest.TestCase):
    def test_generate_data_object_script(self, **kwargs):
        params = dict(
            page_name='pageName value goes here',
            prop1='Prop1 value goes here',
            prop38='third party',
            eVar24='eVar24 value goes here',
            eVar36='eVar36 value goes here',
            eVar57='eVar57 value goes here'
        )
        expected_params = [
          "pageName: 'pageName value goes here'",
          "prop1: 'Prop1 value goes here'",
          "prop38: 'third party'",
          "eVar24: 'eVar24 value goes here'",
          "eVar36: 'eVar36 value goes here'",
          "eVar57: 'eVar57 value goes here'",
        ]
        out = base.generate_data_object_script(**params)

        expected_prefix = """<script>
((((window.trb || (window.trb = {})).data || (trb.data = {})).metrics || (trb.data.metrics = {})).thirdparty = {"""
        self.assertEqual(out.startswith(expected_prefix), True)
        expected_suffix = """});
</script>"""
        self.assertEqual(out.endswith(expected_suffix), True)
        for expected_param in expected_params:
            self.assertTrue(out.index(expected_param) > out.index(expected_prefix) + 1)
            self.assertTrue(out.index(expected_param) < out.index(expected_suffix))

    def test_generate_thirdpartyservice_script(self):
        expected_urls = [
            "//chicagotribune.com/thirdpartyservice?disablenav=true&disablessor=true",
            "//chicagotribune.com/thirdpartyservice",
            "//chicagotribune.com/thirdpartyservice?disablenav=true",
        ]

        inputs = [
            ["chicagotribune.com"],
            ["chicagotribune.com", False, False],
            ["chicagotribune.com", True, False],
        ]

        for args, expected_url in zip(inputs, expected_urls):
            out = base.generate_thirdpartyservice_script(*args)

            expected = "<script src='" + expected_url + "' async></script>"

            self.assertEqual(out, expected)






