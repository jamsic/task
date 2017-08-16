import os


class RawKeywordsProvider:
    FOLDER = 'data'
    FILENAME = 'techs_keywords.csv'

    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__), self.FOLDER)
        filename = os.path.join(filename, self.FILENAME)
        self.raw_keywords = open(filename).read().split('\n')

    def get_keywords(self):
        return self.raw_keywords
