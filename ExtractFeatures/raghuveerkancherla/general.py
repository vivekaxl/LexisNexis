#Note: I'm using f for file as file is a keyword and shoulden't be used.

import urllib2
import os
from urlparse import urlparse

class GeneralConverter:

    """
    This is the base class of all converters.
    """
    def __init__(self, initial_format, final_format):
        """
        The attributes get initlalized in subclasses.
        """
        self.initial_format = initial_format
        self.final_format = final_format

    def file_open(self, file_name):
        """
        Makes no distinction between file from hard disk and from urls.
        """
        try:
            obj = urllib2.urlopen(file_name)
        except ValueError:
            obj = open(file_name)
        text = obj.read()
        return text

    def _get_resultant_file_name(self, f):
        """
        Constructs the file name of the final file from initial file name
        and required output format.
        """
        chomp_length = len(self.initial_format) + 1
        name = f[ : -chomp_length]
        file_name = os.path.basename(name)
        resultant_file_name = '.'.join([file_name, self.final_format])
        return resultant_file_name
