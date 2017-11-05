"""
moviepy.core - method module.
"""

def get_key_or_default(key, default, keys):
    """get key or default value method.
    
    >>> get_key_or_default('key', False, {'other': None})
    False

    args:
        key: (string) key name to search.
        default: (any) default value if not found
        keys: (dict) keys dict with values.
    """
    if key in keys:
        _re = keys[key]
    else:
        _re = default
    return _re
