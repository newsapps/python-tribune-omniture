import re

def to_camelcase(s):
    """
    Convert underscores in a string to camelcase.

    >>> to_camelcase('page_name')
    'pageName'
    """

    def to_uppercase(m):
        if m.group(1):
            return m.group(1).upper()
        else:
            return m.group(0)

    s = re.sub(r'_([^_])', to_uppercase, s)

    return s

PROPERTY_TO_ABBREV = {
    'LA Times': 'lat',
    'Chicago Tribune': 'ct',
    'Morning Call': 'amc',
    'Orlando Sentinel': 'os',
    'Hartford Courant': 'hc',
    'Sun-Sentinel': 'sfss',
    'Baltimore Sun': 'bs',
    'Daily Press': 'hrdp',
    'RedEye Chicago': 'rec',
    'Gary Post-Tribune': 'ptb',
}

def property_abbrev(prop):
    """
    Get the abbreviation for a Tribune media property

    Args:
        prop (str): Name of Tribune media property, e.g. "Chicago Tribune"

    Returns:
        String containing abbreviation for the named property.

    """
    return PROPERTY_TO_ABBREV[prop]

def slugify(s):
    """
    Create a slug version of the string, suitable for being used as part
    of the pageName property
    """
    slug = s.strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug
