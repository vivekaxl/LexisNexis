import sys
sys.path.insert(0, 'converters/')

from general import GeneralConverter
from utilities import convert


class DocumentConverter(GeneralConverter):

    def __init__(self, output_format, *input_files):
        self.file_batch = [input_file for input_file in input_files]
        self.output_format = output_format

    def batch_convert(self):
        file_batch, output_format = self.file_batch, self.output_format
        output_files = [convert(input_file, output_format) for input_file in file_batch]
        return output_files
