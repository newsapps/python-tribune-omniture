from jinja2 import nodes, Environment
from jinja2.ext import Extension

from tribune_omniture.base import (OmnitureTag,
    generate_thirdpartyservice_script)

class OmnitureExtension(Extension):
    tags = set(['omnitag', 'omniscript'])

    def parse(self, parser):
        """
        Parse the template for instances of our custom tags. And then parse
        the arguments that were passed to the tag so we can call the methods
        that output our Omniture snippets.

        """
        # The first token is the token that started the tag. In our case
        # we only listen to ``'omnitag'`` or ``'omniscript'`` so this will be a
        # name token with either `omnitag` or `omniscript` as the value. We get
        # the line number so we can give it to the nodes we create by hand.
        first_token = parser.stream.next()

        lineno = first_token.lineno

        # Check the value of first_token and set the name of the method we want
        # to run. Else raise an error.
        if str(first_token) == 'omnitag':
            method_name = 'omnitag_render'
        elif str(first_token) == 'omniscript':
            method_name = 'omniscript_render'
        else:
            raise ValueError("Unexpected tag name '{}'".format(first_token))

        # Now we parse the expressions passed to our custom tag.
        args = [n for n in parser.parse_tuple().items]

        # Now output the string that is returned by the method we call.
        return nodes.Output([
                            self.call_method(method_name, args)
                            ]).set_lineno(lineno)

    def omnitag_render(self, request, config,
                        story, story_title='', page_type=None):
        """
        Render the Omniture tag snippet based on the arguments provided in
        the custom tag of the template.

        """
        # Create a default dictionary based on the values provided by the
        # Jinja config dictionary.
        defaults = { key:value for key, value in config.items() }

        defaults.setdefault('type', 'individualarticle')

        if story:
            story_title = story.get('title', '')

        tag_attrs =  {
            'title': story_title,
        }

        if page_type is not None:
            tag_attrs['page_type'] = page_type

        tag = OmnitureTag(dict(defaults.items(), **tag_attrs))
        return tag.render()

    def omniscript_render(self, domain, disable_nav=True, disable_ssor=True):
        """
        Template tag to generate the <script> tag to include the 3rd party
        header JavaScript.

        """
        if disable_nav == '':
            disable_nav = True

        if disable_ssor == '':
            disable_ssor = True

        return generate_thirdpartyservice_script(domain,
                                                disable_nav, disable_ssor)
