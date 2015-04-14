import unittest

from flask import Flask, Request
from jinja2 import Environment, Template
from werkzeug.test import EnvironBuilder

from tribune_omniture.jinja import OmnitureExtension

OMNITURE = {
    'domain': 'nfldraft.chicagotribune.com',
    'sitename': 'Chicago Tribune',
    'section': 'sports',
    'subsection': 'bears',
    'subsubsection': '',
    'title': 'NFL Draft',
    'type': 'dataproject',
}

class TestExtension(unittest.TestCase):
    app = Flask('test')

    def setUp(self):
        # With Flask, variables passed to the template are available
        # via app.config.
        self.config = self.app.config
        self.config.update(OMNITURE=OMNITURE)

    def test_omnitag(self):
        builder = EnvironBuilder(path='/', method='GET')
        req = Request(builder.get_environ())
        # Here we instantiate a Jinja environment, and pass it our
        # OmnitureExtension class.
        environment = Environment(extensions=[OmnitureExtension])
        # We load our template from a simple string.
        t = environment.from_string("{% omnitag request, config, None, \
                                    'NFL Draft', 'dataproject' %}")

        # Here is the context we will pass when we render our template.
        c = {
            'request': req,
            'config': self.config,
        }

        expected_params = {
            'pageName': 'ct:nfldraft:sports:bears:NFL-Draft:dataproject.',
            'channel': 'sports:bears',
            'server': 'nfldraft.chicagotribune.com',
            'hier1': 'chicagotribune:sports:bears',
            'hier2': 'sports:bears',
            'prop1': 'D=pageName',
            'prop2': 'sports',
            'prop38': 'dataproject',
            'prop57': 'D=c38',
            'eVar20': 'chicagotribune',
            'eVar21': 'D=c38',
            'eVar34': 'D=ch',
            'eVar35': 'D=pageName',
        }
        expected_param_strs = ["{}: '{}'".format(k, v) for k, v in
            expected_params.items()]
        rendered = t.render(**c)
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
            environment = Environment(extensions=[OmnitureExtension])
            t = environment.from_string("{% omniscript domain, \
                                        disable_nav, disable_ssor %}")
            # Here is the context we will pass when we render our template,
            # note that the disable values might be modified based on args.
            ctx = {
                'domain': domain,
                'disable_nav': True,
                'disable_ssor': True,
            }
            if len(args) > 1:
                ctx['disable_nav'] = args[1]

            if len(args) > 2:
                ctx['disable_ssor'] = args[2]

            rendered = t.render(ctx)
            expected = "<script src='{}' async></script>".format(expected_url)
            self.assertEqual(rendered, expected)