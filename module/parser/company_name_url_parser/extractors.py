import re
from collections import Counter

import nltk
import numpy as np


class ImageTextExtractor:
    def get(self, soup):
        img_alts = [img.get('alt') for img in soup.find_all('img')]
        img_alts = ' '.join([img_alt for img_alt in img_alts if img_alt])
        return img_alts


class TitleTextExtractor:
    def get(self, soup):
        title_text = soup.head.title.text
        return title_text


class UpperLetterWordsExtractor:
    N = 4
    TEXT_WEIGHT = 5
    TEXT_EXTRACTORS = [ImageTextExtractor(), TitleTextExtractor()]

    def _consists_of_words(self, token_tuple):
        return all([token.isalpha() for token in token_tuple])

    def _lower_token(self, token_tuple):
        return tuple([t.lower() for t in token_tuple])

    def _get_tuple_counters(self, tokens):
        token_tuple_counters = {}
        for k in range(1, self.N):
            counter = Counter([tuple(tokens[i:i + k]) for i in range(0, len(tokens) - k + 1)])
            counter = {token_tuple: count for token_tuple, count in counter.items() if
                       self._consists_of_words(token_tuple)}
            token_tuple_counters[k] = counter
        return token_tuple_counters

    def starts_with_upper(self, tuple_token):
        return tuple_token[0][0].isupper()

    def get(self, soup):
        text = [soup.body.text]
        for text_extractor in self.TEXT_EXTRACTORS:
            extracted_text = text_extractor.get(soup) + ' '
            text.append(extracted_text * self.TEXT_WEIGHT)
        text = ' '.join(text)
        tokenized_page_text = nltk.wordpunct_tokenize(text)
        lower_tokenized_page_text = [token.lower() for token in tokenized_page_text]
        tuple_counters_words = self._get_tuple_counters(tokenized_page_text)
        tuple_counters_lower_words = self._get_tuple_counters(lower_tokenized_page_text)
        token_tuples = []
        for k in tuple_counters_words:
            for tuple_token, upper_cnt in tuple_counters_words[k].items():
                if self.starts_with_upper(tuple_token):
                    lower_cnt = tuple_counters_lower_words[k][self._lower_token(tuple_token)]
                    token_tuples.append((tuple_token, upper_cnt, lower_cnt), )
        token_tuples = sorted(token_tuples, key=lambda x: -x[1] * np.exp(x[1] / x[2]))
        frequencies = [t[2] for t in token_tuples]
        median = np.median(frequencies)
        if median < np.max(frequencies):
            token_tuples = list(filter(lambda token: token[2] > median, token_tuples))
        return token_tuples


class UrlsExtractor:
    URL_TEMPLATE = '[A-Za-z]+\.?[A-Za-z]+\.[A-Za-z]+'

    def __init__(self):
        self.pattern = re.compile(self.URL_TEMPLATE)

    def get(self, soup):
        urls = [link.get('href') for link in soup.find_all('a')]
        urls = [url for url in urls if url and url.startswith('http')]
        clean_urls = []
        for url in urls:
            try:
                clean_urls.append(url.split('/')[2])
            except IndexError:
                clean_urls.append(url)
        url_counter = Counter(clean_urls)
        text = soup.body.text
        text_urls = self.pattern.findall(text)
        url_counter.update(text_urls)
        return url_counter

