python-tribune-omniture
=======================

Python package for rendering HTML snippets to enable Tribune Publishing's Omniture Analytics and Third Party navigation.

Installation
------------

    pip install git+https://github.com/newsapps/python-tribune-omniture.git#egg=tribune_omniture

Implementation with Django applications
---------------------------------------

In your settings file, create an Omniture dictionary, which we will use to populate our JavaScript object. Here is an example:

    OMNITURE = {
      'domain': 'elections.chicagotribune.com',
      'sitename': 'Chicago Tribune',
      'section': 'news',
      'subsection': 'local',
      'subsubsection': 'election',
      'title': 'Elections Center',
      'type': 'dataproject',
    }

At the top of your project templates, load the custom template tags with:

    {% load omnituretags %}

In the head of your project templates, load the Omniture object. Replace PAGE NAME HERE with a name that properly identifies the page the user is viewing:

    {% block omniture %}
        {% omnitag request '' 'PAGE NAME HERE' %}
    {% endblock %}

In the footer of your project templates, load the Omniture third party script, and pass your domain (do not include a subdomain). By default, the third party navigation and SSOR tracking are disabled. The metrics team recommends disabling the SSOR tracking if page speed is a concern:

    {% omniscript 'chicagotribune.com' %}

Implementation with Tarbell (Jinja2) projects
---------------------------------------------

In your Tarbell config, update the DEFAULT_CONTEXT dictionary so it includes a nested Omniture dictionary, like this:

    DEFAULT_CONTEXT = {
        'OMNITURE': {
            'domain': 'nfldraft.chicagotribune.com',
            'sitename': 'Chicago Tribune',
            'section': 'sports',
            'subsection': 'bears',
            'subsubsection': '',
            'title': 'NFL Draft',
            'type': 'dataproject',
        }
    }

In the head of your project templates, load the Omniture object. Replace PAGE NAME HERE with a name that properly identifies the page the user is viewing:

    {% omnitag request OMNITURE None 'PAGE NAME HERE' %}

In the footer of your project templates, load the Omniture third party script, and pass your domain (do not include a subdomain). By default, the third party navigation and SSOR tracking are disabled. The metrics team recommends disabling the SSOR tracking if page speed is a concern:

    {% omniscript 'chicagotribune.com' %}
