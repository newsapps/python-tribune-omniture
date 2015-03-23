import unittest

# Make nose ignore these.  They're explicitly loaded upstream
__test__ = False


class TestTemplateTags(unittest.TestCase):
    def test_omnitag(self):
        from django.template.loader import Context, Template
        from django.test.client import RequestFactory
        req_factory = RequestFactory()
        req = req_factory.get('/')
        t = Template("{% load omnituretags %}{% omnitag request '' 'Election Center' 'dataproject' %}")
        c = Context({
            'request': req,
        })
        expected_params = {
            'pageName': 'ct:elections:news:local:election:Election-Center:dataproject.',
            'channel': 'news:local:election',
            'server': 'elections.chicagotribune.com',
            'hier1': 'chicagotribune:news:local:election',
            'hier2': 'news:local:election',
            'prop1': 'D=gn',
            'prop2': 'news',
            'prop38': 'dataproject',
            'prop57': 'D=c38',
            'eVar20': 'chicagotribune',
            'eVar21': 'D=c38',
            'eVar34': 'D=ch',
            'eVar35': 'D=gn',
        }
        expected_param_strs = ["{}: '{}'".format(k, v) for k, v in
            expected_params.items()]
        rendered = t.render(c)
        expected_prefix = """<script>
((((window.trb || (window.trb = {})).data || (trb.data = {})).metrics || (trb.data.metrics = {})).thirdparty = {"""
        self.assertEqual(rendered.startswith(expected_prefix), True)
        expected_suffix = """});
</script>"""
        self.assertEqual(rendered.endswith(expected_suffix), True)
        for expected_param in expected_param_strs:
            try:
                param_index = rendered.index(expected_param)
                self.assertTrue(param_index >
                                rendered.index(expected_prefix) + 1)
                self.assertTrue(param_index <
                                rendered.index(expected_suffix))
            except ValueError:
                msg = "Parameter \"{}\" not found in expected position".format(
                   expected_param)
                raise ValueError(msg)

    def test_omniscript(self):
        from django.template.loader import Context, Template
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
            domain = args[0]
            t = Template("{% load omnituretags %}{% omniscript domain disable_nav disable_ssor %}")
            ctx = {
                'domain': domain,
            }
            if len(args) > 1:
                ctx['disable_nav'] = args[1]

            if len(args) > 2:
                ctx['disable_ssor'] = args[2]

            c = Context(ctx)
            rendered = t.render(c)
            expected = "<script src='{}' async></script>".format(expected_url)
            self.assertEqual(rendered, expected)
