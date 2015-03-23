import django
from django.conf import settings


if not settings.configured:
    print("HERE")
    settings.configure(
        INSTALLED_APPS=('tribune_omniture.django',),
        OMNITURE={
          'domain': 'elections.chicagotribune.com',
          'sitename': 'Chicago Tribune',
          'section': 'news',
          'subsection': 'local',
          'subsubsection': 'election',
          'title': 'Elections Center',
          'type': 'dataproject',
        },
        TEMPLATE_DEBUG=True,
    )


try:
    # For Django >= 1.7
    if hasattr(django, 'setup'):
        django.setup()
except RuntimeError:
    pass


# Import the unittest.TestCase classes from the Django app so they'll be run
# by the test runner
from tribune_omniture.django.tests import TestTemplateTags
