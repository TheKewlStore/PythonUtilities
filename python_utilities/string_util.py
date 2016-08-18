# coding=utf-8
""" Convenience functions for dealing with common python string operations.

Author: Ian Davis
"""

import string
import random


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    """ Return a string of characters generated at random.

        :param size: The length of the string to generate. 
        :param chars: The set of characters to pick from (defaults to uppercase ascii and digits).
        :return: The generated string.
    """
    random_characters = (random.choice(chars) for _ in xrange(size))
    return ''.join(random_characters)


def quoted(string_):
    """ Wrap the given string in double quotes.

    :param string_: The string to quote.
    :return: The quoted string.
    """
    return '"{0}"'.format(string_)
