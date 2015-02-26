from general import GeneralConverter
from subprocess import call
import urlparse
import os

class PdfHtml(GeneralConverter):
    """
    This class is for Pdf-Html conversion.
    """
    def __init__(self):
        self.initial_format = 'pdf'
        self.final_format = 'html'
        self.file_batch = []

    def convert(self, f):
        os.system('pdf2htmlEX %s'%f)
        output_file_name = self._get_resultant_file_name(f)
        return output_file_name
        

