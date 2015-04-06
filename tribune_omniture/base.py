from .utils import property_abbrev, to_camelcase, slugify


def generate_data_object_script(**kwargs):
    """Generate JavaScript to configure third party analytics service"""
    bits = []

    bits.append("<script>")

    bits.append("((((window.trb || (window.trb = {})).data || "
        "(trb.data = {})).metrics || (trb.data.metrics = {})).thirdparty = {")

    for key, value in kwargs.items():
        js_key = to_camelcase(key)
        bits.append("  {key}: '{value}',".format(key=js_key, value=value))

    bits[-1] = bits[-1].rstrip(',')

    bits.append("});")

    bits.append("</script>")


    return "\n".join(bits)


def generate_thirdpartyservice_script(domain, disable_nav=True, disable_ssor=True):
    """
    Generate the <script> tag to include the 3rd party header JavaScript

    Args:
        domain (str): Domain where the script should be loaded.
        disable_nav (bool): Should the third party header be hidden and the
            script only be used for analytics?  Default is True.
        disable_ssor (bool): Should SSOR code be omitted? Default is True.

    """
    qs_bits = []

    if disable_nav is True:
        qs_bits.append("disablenav=true")

    if disable_ssor is True:
        qs_bits.append("disablessor=true")

    qs = "&".join(qs_bits)

    url = "//" + domain + "/thirdpartyservice"

    if qs:
        url = url + "?" + qs

    script = "<script src='" + url + "' async></script>"

    return script

# Content types for most subdomains and external sites
# Please contact analysismetric@tribune.com if you do not believe these
# meet your reporting needs.
CONTENT_TYPES = [
    # project that links to a series of interrelated pages that present stories
    # or written explanations; content is primarily written in nature
    # with minimal written explanation
    'articleproject',
    # project that links to a series of interrelated pages that present data
    # listings; content is primarily numeric in nature with minimal written
    # explanation
    'dataproject',
    # photogallery off of the NGUX platform and landing pages associated with
    # the photogallery
    'photogalleryproject',
    # landing page for a marketing campaign
    'landingpage',
    # one-off page where the content is primarily visual; likely to have an
    # interactive element
    'individualgraphic',
    # one-off page that's a written article off of the NGUX platform
    'individualarticle',
    # subdomain or partner external domain with static measurement across
    # the entire subdomain or partner pages
    '3rd party',
]

class OmnitureTag(object):
    requirements = ['type', 'domain', 'sitename', ]

    content_types = set(CONTENT_TYPES)

    def __init__(self, attributes={}):
        for requirement in self.requirements:
            if attributes.get(requirement, None) is None:
                raise ValueError(
                    'OmnitureTag requires a %s attribute' % requirement)

        # Make sure the content type is one of the canonical values
        assert attributes['type'] in self.content_types

        for key, val in attributes.items():
            setattr(self, key, val)

    def build_vars(self):
        ret = {
            'channel':  self.build_channel(),
            'server':   self.build_server(),
            'pageName': self.build_pageName(),
            'hier1':    self.build_hier1(),
            'hier2':    self.build_hier2(),
            'prop1':    self.build_prop1(),
            'prop2':    self.build_prop2(),
            'prop38':   self.build_prop38(),
            'prop57':   self.build_prop57(),
            'eVar20':   self.build_eVar20(),
            'eVar21':   self.build_eVar21(),
            'eVar34':   self.build_eVar34(),
            'eVar35':   self.build_eVar35(),
        }
        return ret

    def _parse_subdomain(self, domain):
        return domain.split('.')[0]

    def _parse_second_level_domain(self, domain):
        return domain.split('.')[-2]

    def build_pageName(self):
        try:
            return self.page_name
        except AttributeError:
            bits = []
            total_len = 0

        abbrev = property_abbrev(self.sitename)
        total_len += len(abbrev)
        bits.append(abbrev)

        if self.domain:
            subdomain = self._parse_subdomain(self.domain)
            total_len += len(subdomain)
            bits.append(subdomain)

        if self.section:
            bits.append(self.section)
            total_len += len(self.section)

            if self.subsection:
                bits.append(self.subsection)
                total_len += len(self.subsection)

                if self.subsubsection:
                    bits.append(self.subsubsection)
                    total_len += len(self.subsubsection)

        bits.append(self.type)
        total_len += len(self.type)
        # The number of separator characters, ':' will be equal to the number of
        # bits. The pageName property also contains a trailing '.' character
        total_len += len(bits) + 1

        if self.title:
            # The title will be part of the pageName property, so we'll have
            # an additional separator character
            total_len += 1
            title_slug = slugify(self.title)

            if total_len + len(title_slug) > 100:
                # The pageName property can only be 100 characters.  Truncate
                # the title_slug so it will fit
                title_slug = title_slug[:100 - total_len + 1].rstrip('-')

            bits.insert(-1, title_slug)

        return ':'.join(bits) + '.'

    def build_channel(self):
        return self._build_hier()

    def build_server(self):
        return self.domain

    def _build_hier(self, initial_bits=[]):
        bits = [] + initial_bits

        if self.section:
            bits.append(self.section.lower())

            if self.subsection:
                bits.append(self.subsection.lower())

                if self.subsubsection:
                    bits.append(self.subsubsection.lower())
        elif self.type:
            bits.append(self.type)

        return ':'.join(bits)

    def build_hier1(self):
        return self._build_hier(
            [self._parse_second_level_domain(self.domain)])

    def build_hier2(self):
        return self._build_hier()

    def build_prop1(self):
        return "D=pageName"

    def build_prop2(self):
        try:
            return self.section
        except AttributeError:
            return ''

    def build_prop38(self):
        return self.type

    def build_prop57(self):
        return "D=c38"

    def build_eVar20(self):
        return self._parse_second_level_domain(self.domain)

    def build_eVar21(self):
        return self.build_prop57()

    def build_eVar34(self):
        return "D=ch"

    def build_eVar35(self):
        return "D=pageName"

    def render(self):
        return generate_data_object_script(**self.build_vars())
