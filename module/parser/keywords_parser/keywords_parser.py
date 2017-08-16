import nltk
from .keywords_provider import KeywordsProvider


class KeywordsParser:

    def __init__(self):
        keyword_by_token_phrase_variation = KeywordsProvider().get_keywords()
        self.token_lengths = {len(variation) for variation in keyword_by_token_phrase_variation}
        self.keyword_by_token_str_variation = self.token_to_str(keyword_by_token_phrase_variation)

    def parse(self, soup):
        text_str_tokens = self.text_to_tokens(soup)
        common_str_tokens = text_str_tokens & self.keyword_by_token_str_variation.keys()
        return {self.keyword_by_token_str_variation[cst] for cst in common_str_tokens}

    def _to_str_keyword(self, tuple_variation):
        return '_'.join(tuple_variation)

    def token_to_str(self, keyword_by_token_phrase_variation):
        keyword_by_token_str_variation = {}
        for tuple_variation, keyword in keyword_by_token_phrase_variation.items():
            keyword_by_token_str_variation[self._to_str_keyword(tuple_variation)] = keyword
        return keyword_by_token_str_variation

    def text_to_tokens(self, soup):
        text = soup.body.text
        text_tokens = nltk.word_tokenize(text)
        all_text_tokens = set()
        for k in self.token_lengths:
            all_text_tokens.update({tuple(text_tokens[i: i + k]) for i in range(len(text_tokens) - k + 1)})
        text_str_tokens = {self._to_str_keyword(token) for token in all_text_tokens}
        return text_str_tokens

