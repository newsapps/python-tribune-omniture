import unittest

from tribune_omniture import base

class TestBase(unittest.TestCase):
    def test_generate_data_object_script(self, **kwargs):
        params = dict(
            page_name='pageName value goes here',
            prop1='Prop1 value goes here',
            prop38='third party',
            eVar24='eVar24 value goes here',
            eVar36='eVar36 value goes here',
            eVar57='eVar57 value goes here'
        )
        expected_params = {
          'pageName': 'pageName value goes here',
          'prop1': 'Prop1 value goes here',
          'prop38': 'third party',
          'eVar24': 'eVar24 value goes here',
          'eVar36': 'eVar36 value goes here',
          'eVar57': 'eVar57 value goes here',
        }
        expected_param_strs = ["{}: '{}'".format(k, v) for k, v in
            expected_params.items()]
        out = base.generate_data_object_script(**params)

        expected_prefix = """<script>
((((window.trb || (window.trb = {})).data || (trb.data = {})).metrics || (trb.data.metrics = {})).thirdparty = {"""
        self.assertEqual(out.startswith(expected_prefix), True)
        expected_suffix = """});
</script>"""
        self.assertEqual(out.endswith(expected_suffix), True)
        for expected_param in expected_param_strs:
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


OMNITURE_SETTINGS = {
    'domain': 'elections.chicagotribune.com',
    'sitename': 'Chicago Tribune',
    'section': 'news',
    'subsection': 'local',
    'subsubsection': 'election',
    'title': 'Elections Center',
}

OMNI_HOME_TAG = dict(OMNITURE_SETTINGS, type='dataproject', title="Election Center Home")

OMNI_HOME_TAG_PAGENAME = ('ct:elections:news:local:election:'
    'Election-Center-Home:dataproject.')

OMNI_STORY_TAG = dict(OMNITURE_SETTINGS,
    title='Story Title',
    author='Michael Jordan',
    section='classifieds',
    subsection='automotive',
    subsubsection=None,
    type='individualarticle'
)

OMNI_STORY_TAG_PAGENAME = ('ct:elections:classifieds:automotive:Story-Title:'
    'individualarticle.')

OMNI_GALLERY_TAG = dict(OMNITURE_SETTINGS,
    title='Gallery Title',
    author='Michael Jordan',
    section='classifieds',
    subsection='automotive',
    subsubsection=None,
    type='photogalleryproject'
)

OMNI_GALLERY_TAG_PAGENAME = ('ct:elections:classifieds:automotive:'
    'Gallery-Title:photogalleryproject.')


class TestOmnitureTag(unittest.TestCase):

    def test_init(self):
        self.assertRaises(ValueError, base.OmnitureTag, {})

        omni_tag = base.OmnitureTag({
            'domain': 'www.chicagotribune.com',
            'sitename': 'Chicago Tribune',
            'type': 'articleproject'
        })
        self.assertEquals(omni_tag.type, 'articleproject')

    def test_parse_subdomain(self):
        omni_tag = base.OmnitureTag({
            'domain': 'elections.chicagotribune.com',
            'sitename': 'Chicago Tribune',
            'type': 'articleproject'
        })
        test_vals = [
            ('elections.chicagotribune.com', 'elections'),

        ]
        for domain, subdomain in test_vals:
            self.assertEqual(omni_tag._parse_subdomain(domain), subdomain)

    def test_parse_second_level_domain(self):
        omni_tag = base.OmnitureTag({
            'domain': 'elections.chicagotribune.com',
            'sitename': 'Chicago Tribune',
            'type': 'articleproject'
        })
        test_vals = [
            ('elections.chicagotribune.com', 'chicagotribune'),

        ]
        for domain, second_level_domain in test_vals:
            self.assertEqual(omni_tag._parse_second_level_domain(domain),
                second_level_domain)

    def test_build_pageName(self):
        # Home
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_pageName(), OMNI_HOME_TAG_PAGENAME)

        # Story
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)
        self.assertEquals(omni_tag.build_pageName(), OMNI_STORY_TAG_PAGENAME)

        # Gallery
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)
        self.assertEquals(omni_tag.build_pageName(), OMNI_GALLERY_TAG_PAGENAME)

    def test_build_channel(self):
        # Home
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(
            omni_tag.build_channel(),
            "{}:{}:{}".format(OMNI_HOME_TAG['section'],
                OMNI_HOME_TAG['subsection'],
                OMNI_HOME_TAG['subsubsection']))

        # Story
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)
        self.assertEquals(
            omni_tag.build_channel(),
            "{}:{}".format(
                OMNI_STORY_TAG['section'],
                OMNI_STORY_TAG['subsection'],
            )
        )

        # Gallery
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)
        self.assertEquals(
            omni_tag.build_channel(),
            "{}:{}".format(
                OMNI_GALLERY_TAG['section'],
                OMNI_GALLERY_TAG['subsection'],
            )
        )

    def test_build_hier1(self):
        # Home
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(
            omni_tag.build_hier1(),
            "chicagotribune:{}:{}:{}".format(
                OMNI_HOME_TAG['section'],
                OMNI_HOME_TAG['subsection'],
                OMNI_HOME_TAG['subsubsection']))

        # Story
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)
        self.assertEquals(
            omni_tag.build_hier1(),
            "chicagotribune:{}:{}".format(
                OMNI_STORY_TAG['section'],
                OMNI_STORY_TAG['subsection']
            )
        )

        # Gallery
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)
        self.assertEquals(
            omni_tag.build_hier1(),
            "chicagotribune:{}:{}".format(
                OMNI_STORY_TAG['section'],
                OMNI_STORY_TAG['subsection']
            )
        )

    def test_build_hier2(self):
        # Home
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_hier2(),
            "{}:{}:{}".format(
                OMNI_HOME_TAG['section'],
                OMNI_HOME_TAG['subsection'],
                OMNI_HOME_TAG['subsubsection'],
            ))

        # Story
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)
        self.assertEquals(
            omni_tag.build_hier2(),
            "{}:{}".format(
                OMNI_STORY_TAG['section'],
                OMNI_STORY_TAG['subsection']
            )
        )

        # Gallery
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)
        self.assertEquals(
            omni_tag.build_hier2(),
            "{}:{}".format(
                OMNI_GALLERY_TAG['section'],
                OMNI_GALLERY_TAG['subsection']
            )
        )

    def test_build_prop1(self):
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_prop1(), 'D=pageName')

    def test_build_prop2(self):
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEqual(omni_tag.build_prop2(), OMNI_HOME_TAG['section'])


    def test_build_prop38(self):
        # Home
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_prop38(), OMNI_HOME_TAG['type'])

        # Story
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)
        self.assertEquals(omni_tag.build_prop38(), OMNI_STORY_TAG['type'])

        # Gallery
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)
        self.assertEquals(omni_tag.build_prop38(), OMNI_GALLERY_TAG['type'])

    def test_build_prop57(self):
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_prop57(), 'D=c38')

    def test_build_eVar20(self):
        # Home
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(
            omni_tag.build_eVar20(), 'chicagotribune')

        # Story
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)
        self.assertEquals(
            omni_tag.build_eVar20(), 'chicagotribune')

        # Gallery
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)
        self.assertEquals(
            omni_tag.build_eVar20(), 'chicagotribune')

    def test_build_eVar21(self):
        # Home
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_eVar21(), 'D=c38')

        # Story
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)
        self.assertEquals(omni_tag.build_eVar21(), 'D=c38')

        # Gallery
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)
        self.assertEquals(omni_tag.build_eVar21(), 'D=c38')

    def test_build_eVar34(self):
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_eVar34(), 'D=ch')

    def test_build_eVar35(self):
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)
        self.assertEquals(omni_tag.build_eVar35(), 'D=pageName')

    def test_home_tag(self):
        omni_tag = base.OmnitureTag(OMNI_HOME_TAG)

        self.assertEqual(
            omni_tag.type, OMNI_HOME_TAG['type'])
        self.assertEqual(
            omni_tag.domain, OMNITURE_SETTINGS['domain'])
        self.assertEqual(
            omni_tag.sitename, OMNITURE_SETTINGS['sitename'])

        self.assertEqual(omni_tag.build_pageName(), OMNI_HOME_TAG_PAGENAME)

    def test_story_tag(self):
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)

        self.assertEqual(
            omni_tag.title, OMNI_STORY_TAG['title'])
        self.assertEqual(
            omni_tag.author, OMNI_STORY_TAG['author'])
        self.assertEqual(
            omni_tag.section, OMNI_STORY_TAG['section'])
        self.assertEqual(
            omni_tag.subsection, OMNI_STORY_TAG['subsection'])
        self.assertEqual(
            omni_tag.type, OMNI_STORY_TAG['type'])
        self.assertEqual(
            omni_tag.domain, OMNITURE_SETTINGS['domain'])
        self.assertEqual(
            omni_tag.sitename, OMNITURE_SETTINGS['sitename'])

        self.assertEqual(omni_tag.build_pageName(), OMNI_STORY_TAG_PAGENAME)

    def test_gallery_tag(self):
        omni_tag = base.OmnitureTag(OMNI_GALLERY_TAG)

        self.assertEqual(
            omni_tag.title, OMNI_GALLERY_TAG['title'])
        self.assertEqual(
            omni_tag.author, OMNI_GALLERY_TAG['author'])
        self.assertEqual(
            omni_tag.section, OMNI_GALLERY_TAG['section'])
        self.assertEqual(
            omni_tag.subsection, OMNI_GALLERY_TAG['subsection'])
        self.assertEqual(
            omni_tag.type, OMNI_GALLERY_TAG['type'])
        self.assertEqual(
            omni_tag.domain, OMNITURE_SETTINGS['domain'])
        self.assertEqual(
            omni_tag.sitename, OMNITURE_SETTINGS['sitename'])

        self.assertEqual(omni_tag.build_pageName(), OMNI_GALLERY_TAG_PAGENAME)

    def test_build_long_pageName(self):
        omni_tag = base.OmnitureTag(OMNI_STORY_TAG)

        # Set the title to something greater than 100 characters
        omni_tag.title = 'X' * 101

        # Make sure build_pageName returns 100 characters
        self.assertEqual(len(omni_tag.build_pageName()), 100)
