#Note: I'm using f for file as file is a keyword and shoulden't be used.
from general import GeneralConverter
from xhtml2pdf import pisa

class HtmlPdf(GeneralConverter):
    """
    This class is for Html-Pdf conversion.
    """
    def __init__(self):
        self.initial_format = 'html'
        self.final_format = 'pdf'
        self.file_batch = []

    def convert(self, f):
        output_file_name = self._get_resultant_file_name(f)
        output_file = open(output_file_name, 'w+b')
        input_file = self.file_open(f)
        pisa.CreatePDF(input_file, dest=output_file)
        return output_file_name
