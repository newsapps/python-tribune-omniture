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