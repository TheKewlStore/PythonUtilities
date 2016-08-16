# coding=utf-8
""" config is an API-Like module used currently by HTe that abstracts an
    interface around ConfigParser to manage an application-wide configuration
    file.

Author: Ian Davis
"""

from ConfigParser import ConfigParser

import os_util


class InvalidSectionError(Exception):
    """ InvalidSectionError is raised from class Configuration
        when a section or option that does not exist is attempted
        to be accessed from [] notation.
    """
    pass


class InvalidOptionError(Exception):
    """ InvalidOptionError is raised from class ConfigurationSection
        when an option that does not exist is attempted
        to be accessed from [] notation.
    """
    pass


class ConfigurationSection(object):
    """ ConfigurationSection handles the data stored in one
        section of a configuration file.
    """

    def __init__(self, name, options=None):
        """ ConfigurationSection constructor.

            param name: Name of the section
            param options: Optional parameter that should be
                a dictionary of option_name: option_value for
                this configuration section.
        """
        self.name = name
        self.options = options

    def _verify_section_exists(self, config_parser):
        """ Private method used by the write method to assert
            that our section exists in the given ConfigParser
            before trying to write options to it.
        """
        if not config_parser.has_section(self.name):
            config_parser.add_section(self.name)

    def write(self, config_parser):
        """ Given a ConfigParser instance, add all of our option-values
            to our section to be written to file.
        :param config_parser:
        """
        self._verify_section_exists(config_parser=config_parser)

        for option_name, option_value in self.options.items():
            config_parser.set(self.name, option_name, option_value)

    def read_options(self, config_parser):
        """ Given a ConfigParser instance, read in all of the option value pairs
            for our section to our internal dictionary.
        :param config_parser:
        """
        self.options = {}

        for option_name, option_value in config_parser.items(self.name):
            self.options[option_name] = option_value

    def __getitem__(self, key):
        """ Python builtin handler for dictionary notation access
            ConfigurationSection[key] == ConfigurationSection.__getitem__(key)
        """
        if key in self.options:
            return self.options[key]

        raise InvalidOptionError(key)

    def __setitem__(self, key, value):
        """ Python builtin handler for dictionary notation access
            (ConfigurationSection[key] = value) ==
                ConfigurationSection.__setitem__(key, value)
        """
        if key in self.options:
            self.options[key] = value
            return

        raise InvalidOptionError(key)


class Configuration(object):
    """ Configuration is an abstraction over the python
        ConfigParser class, built to handle an app level
        configuration file, and reading and writing values
        to said file.
    """

    def __init__(self, file_path, sections=None):
        self.file_path = file_path
        self.sections = {}

        self.config_parser = ConfigParser()

        if not os_util.is_file(self.file_path):
            if not self.sections:
                self._setup_default_sections()

            self.write()

        if not self.sections:
            self.read()

        if sections:
            self.add_sections(sections=sections)

    def _verify_section_integrity(self):
        """ Verify that all sections and their default options exist in the configuration file.

            Abstract implementation here as no default sections are defined.

        """
        pass

    def _setup_default_sections(self):
        """ Setup all default sections and their values for a first init.

            Abstract implementation here as no default sections are defined.

        """
        pass

    def add_sections(self, sections):
        """ Interface method to add multiple sections to our configuration
            file at once, call this to ensure that the sections are added
            to all data structures properly.
        :param sections:
        """
        for section_name, section in sections.items():
            self.sections[section_name] = section

            self.config_parser.add_section(section_name)
            section.write(config_parser=self.config_parser)

    def add_section(self, name, options=None):
        """ Interface method to add a section to our configuration
            file at once, call this to ensure that the section is added
            to all data structures properly.
        :param name:
        :param options:
        """
        section = ConfigurationSection(name=name, options=options)
        self.sections[name] = section

        self.config_parser.add_section(name)
        section.write(config_parser=self.config_parser)

        self.write()

    def write(self):
        """ Could be considered a private method, this is called by
            the constructor if the configuration file doesn't exist,
            but could also be called by outside code to force a rewrite
            of the configuration file.
        """
        for section in self.sections.itervalues():
            section.write(self.config_parser)

        with open(self.file_path, 'wb') as config_file:
            self.config_parser.write(config_file)

    def read(self):
        """ Could be considered a private method, this is called by
            the constructor if the configuration file exists and
            no sections are specified at the code level to synchronize
            our data structures with that of the file, but could also
            be called by outside code to force an Object->File synchronization.
        """
        if not os_util.is_file(self.file_path):
            return

        self.sections = {}
        self.config_parser.read(self.file_path)

        for section_name in self.config_parser.sections():
            section = ConfigurationSection(name=section_name)
            section.read_options(config_parser=self.config_parser)

            self.sections[section_name] = section

    def __getitem__(self, key):
        """ Python builtin handler for dictionary notation access
            Configuration[key] == Configuration.__getitem__(key)
        """
        if key in self.sections:
            return self.sections[key]

        raise InvalidSectionError(key)

    def __setitem__(self, key, value):
        """ Python builtin handler for dictionary notation access
            (Configuration[key] = value) ==
                Configuration.__setitem__(key, value)
        """
        if key in self.sections:
            self.sections[key] = value
            return

        raise InvalidSectionError(key)
