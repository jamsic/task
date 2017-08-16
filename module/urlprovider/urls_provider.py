import os

class UrlsProvider:

    FOLDER = 'data'
    FILENAME = 'urls.txt'

    def get_urls(self):
        filename = os.path.join(os.path.dirname(__file__), self.FOLDER)
        filename = os.path.join(filename, self.FILENAME)
        with open(filename) as handle:
            for line in handle:
                yield line.strip()

