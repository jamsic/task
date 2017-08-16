import requests

from .dbconnector import DbConnector


class Crawler:
    def __init__(self):
        self.db = DbConnector()

    def crawl_one(self, url):
        resp = requests.get(url)
        raw_page = resp.text
        self.db.save_page(url, raw_page)

    def crawl(self, urls):
        for url in urls:
            if not self.db.is_url_in(url):
                self.crawl_one(url)

    def get_pages(self):
        return self.db.get_pages()

