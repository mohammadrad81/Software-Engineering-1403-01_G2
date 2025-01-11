class FileContentExtractor:
    def __init__(self):
        self.lines = []

    def get_concatenated_content(self, text_file):
        """Return the concatenated content of the lines."""
        try:
            self.lines = text_file.readlines()
        except IOError:
            print(f"Error: An IOError occurred while trying to read the file.")
        return ''.join(self.lines)