from bs4 import BeautifulSoup


class HtmlCleaner:
    STRING_REPLACEMENTS = {('>', '> '), ('<', ' <')}
    TAGS_TO_EXTRACT = ['style', 'script']

    def _replace(self, html):
        for replacement in self.STRING_REPLACEMENTS:
            html = html.replace(*replacement)
        return html

    def _extract(self, soup):
        for x in soup.find_all(self.TAGS_TO_EXTRACT):
            x.extract()

    def clean(self, html):
        html = self._replace(html)
        soup = BeautifulSoup(html)
        self._extract(soup)
        return soup

