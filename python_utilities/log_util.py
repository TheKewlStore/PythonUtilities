# coding=utf-8
""" Convenience functions to simplify python logging module, and extend it's functionality.

Author: Ian Davis
"""

import logging
import re
import sre_constants
import sys

from colorlog import ColoredFormatter

from python_utilities import os_util


def initialize(name, filepath, level, console_output=False, log_colors=None, regex_filter=None):
    """ Initialize logger settings for the logger name specified.

        :param name: The name of the logger to initialize (can be None to configure the root logger).
        :param filepath: The path to the logfile to use.
        :param level: The level to use for logging.
        :param console_output: Flag to indicate whether or not to reflect log to console or not.
        :param log_colors: Custom dictionary mapping level names to color types.
        :param regex_filter: Should be a regular expression string that will be matched against any records logged.
    """
    os_util.clear_file(filepath)

    logger = logging.getLogger(name)
    logger.propagate = False

    if not log_colors:
        log_colors = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'}

    colored_formatter = ColoredFormatter('%(log_color)s[%(levelname)s-%(asctime)s]: %(message)s',
                                         datefmt="%Y-%m-%d %H:%M:%S",
                                         reset=True,
                                         log_colors=log_colors)

    file_formatter = logging.Formatter('[%(levelname)s-%(asctime)s]: %(message)s',
                                       datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(filepath, mode='w')
    stream_handler = logging.StreamHandler(sys.stdout)

    file_handler.setFormatter(file_formatter)
    stream_handler.setFormatter(colored_formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)

    if regex_filter:
        logger.addFilter(RegexFilter(regex_filter))

    if console_output:
        logger.addHandler(stream_handler)


class RegexFilter(object):
    def __init__(self, regex_pattern):
        try:
            self.pattern = re.compile(regex_pattern)
        except sre_constants.error:
            raise ValueError('Logging filter expression invalid!')

    def filter(self, record):
        return bool(self.pattern.match(record.getMessage()))
