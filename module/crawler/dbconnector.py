import os
import sqlite3


class DbConnector:
    FOLDER = 'data'
    DB_NAME = 'data.db'

    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__), self.FOLDER)
        if not os.path.exists(filename):
            os.mkdir(filename)
        filename = os.path.join(filename, self.DB_NAME)
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''PRAGMA foreign_keys = ON;''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS sites(
                                id INTEGER PRIMARY KEY,
                                url TEXT NOT NULL UNIQUE,
                                raw_page TEXT NOT NULL,
                                datetime DATETIME DEFAULT CURRENT_TIMESTAMP
                                );''')
        self.db.commit()

    def __del__(self):
        self.db.close()

    def commit_all(self):
        self.db.commit()

    def _get_ans(self, query):
        self.cur.execute(*query)
        ans = self.cur.fetchall()
        return ans

    def is_url_in(self, url):
        query = 'SELECT * FROM sites WHERE url=?', (url,)
        ans = self._get_ans(query)
        res = len(ans) > 0
        return res

    def save_page(self, url, raw_page):
        query = 'INSERT INTO sites(url, raw_page) VALUES (?, ?)', (url, raw_page)
        self.cur.execute(*query)
        self.commit_all()

    def get_pages(self):
        query = 'SELECT * FROM sites',
        ans = self._get_ans(query)
        return ans

