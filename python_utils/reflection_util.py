# coding=utf-8
""" Convenience functions for common python reflection operations.

Author: Ian Davis
Last Updated: 11/17/2015
"""


def protected_method(name):
    """ Determine whether or not a given attribute name is considered protected or builtin (Starts with an _).

        :param name: The name of the attribute to check.
        :return: True or False, indicating whether the attribute's name is protected.
    """
    if name.startswith('_'):
        return True

    return False


def attribute_list(obj):
    """ Return a tuple of (name, value) tuples of all the attributes of the given python object.
    
        :param obj: The python object to list attributes.
    """
    return obj.__dict__.iteritems()
