from setuptools import setup

# PyPI only supports nicely-formatted README files in reStructuredText.
# Newsapps seems to prefer Markdown.  Use a version of the pattern from
# https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
# to convert the Markdown README to rst if the pypandoc package is
# present.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()

# Load the version from the version module
exec(open('tribune_omniture/version.py').read())

setup(
    name='tribune_omniture',
    version=__version__,
    packages=['tribune_omniture'],
    install_requires=[
    ],
    tests_require=[
        'nose',
        'Django',
    ],
    test_suite='nose.collector',
)
