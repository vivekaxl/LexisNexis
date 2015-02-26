from general import GeneralConverter
from html2text import html2text

class HtmlTxt(GeneralConverter):
    """
    This class is for Html-Text conversion
    """
    def __init__(self):
        self.initial_format = 'html'
        self.final_format = 'txt'
        self.file_batch = []

    def convert(self, f):
        input_text = self.file_open(f)
        output_text = html2text(input_text)
        output_file_name = self._get_resultant_file_name(f)
        output_file = open(output_file_name, 'w+b')
        output_file.write(output_text)
        return output_file_name
