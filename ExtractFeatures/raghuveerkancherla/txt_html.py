from general import GeneralConverter
import markdown2

class TxtHtml(GeneralConverter):
    """
    This class is for Txt-Html conversion.
    """

    def __init__(self):
        self.initial_format = 'txt'
        self.final_format = 'html'
        self.file_batch = []

    def convert(self, f):
        input_text = self.file_open(f)
        output_text = markdown2.markdown(input_text)
        output_file_name = self._get_resultant_file_name(f)
        output_file = open(output_file_name, 'w+b')
        output_file.write(output_text)
        return output_file_name
