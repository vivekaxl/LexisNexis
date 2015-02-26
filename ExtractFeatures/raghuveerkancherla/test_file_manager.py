import unittest

file_manager1 = FileManager(some_input_file_path, some_output_file_path)
file_manager2 = FileManager(some_input_url, some_output_file_path)


class FileManagerTests(unittest.TestCase):

    def FileManagerOpenTests(self):
        """
        Tests whether FileManager distinguishes between file on disk and urls.
        """
        self.failUnless(isinstance(file_manager1.file_open(), str))
        self.failUnless(isinstance(file_manager2.file_open(), str))

    def FileManagerWriteTests(self):
        """
        Tests whether a proper file has been created and text is written successfully
        written on it.
        """

        self.failUnless(
            isinstance(file_manager1.output_write(input_text), file))
        self.failUnless(isinstance(file_manager2.output_read(), str))
