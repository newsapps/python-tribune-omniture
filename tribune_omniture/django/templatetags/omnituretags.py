from django import template
from django.conf import settings

from tribune_omniture.base import (OmnitureTag,
    generate_thirdpartyservice_script)

register = template.Library()


DEFAULTS = {
    'title': settings.OMNITURE['title'],
    'type': settings.OMNITURE.get('type', 'individualarticle'),
    'section': settings.OMNITURE['section'],
    'subsection': settings.OMNITURE['subsection'],
    'subsubsection': settings.OMNITURE['subsubsection'],
    'domain': settings.OMNITURE['domain'],
    'sitename': settings.OMNITURE['sitename'],
}

def section_from_path(path):
    """
    Detect section based on a page's path

    This logic is deprecated and reflects earlier versions of omniture tracker
    generation.  It is just preserved here for reference.

    """
    first_slash = path.find('/')
    last_slash = path.rfind('/')
    return path[first_slash + 1:last_slash]


def type_from_path(path):
    """
    Detect story type based on a page's path

    This logic is deprecated and reflects earlier versions of omniture tracker
    generation.  It is just preserved here for reference.

    """
    if path.endswith('.photogallery'):
        page_type = 'photoga.'
    elif path.endswith('.htmlstory'):
        page_type = 'htmlstory'
    elif path.endswith('/'):
        page_type = '3rd party'
    else:
        page_type = 'story'

    return page_type


@register.simple_tag
def omnitag(request, story, story_title='', page_type=None):
    """
    Template tag to render the analytics JavaScript configuration object
    snippet

    Args:
        request: Django request object for the current request.
        story: Dictionary for the current page.
        page_name: String

    Returns:
        String containing an HTML snippet with the '<script>' tag
        containing the JavaScript configuration object.

    """
    if story:
        story_title = story.get('title', '')

    tag_attrs =  {
        'title': story_title,
    }

    if page_type is not None:
        tag_attrs['page_type'] = page_type

    tag = OmnitureTag(dict(DEFAULTS.items(), **tag_attrs))
    return tag.render()


@register.simple_tag
def omniscript(domain, disable_nav=True, disable_ssor=True):
    """
    Template tag to generate the <script> tag to include the 3rd party header
    JavaScript

    """
    if disable_nav == '':
        disable_nav = True

    if disable_ssor == '':
        disable_ssor = True

    return generate_thirdpartyservice_script(domain, disable_nav, disable_ssor)
