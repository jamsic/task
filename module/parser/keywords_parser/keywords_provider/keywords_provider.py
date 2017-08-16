import nltk

from .raw_keywords_provider import RawKeywordsProvider
from .variators import InBracketsVariator, OutBracketsVariator, CompanyNameVariator


class KeywordsProvider:
    def __init__(self):
        keywords = RawKeywordsProvider().get_keywords()
        token_phrases_by_keywords = self._tokenize(keywords)
        variators = [InBracketsVariator(), OutBracketsVariator(),
                     CompanyNameVariator(token_phrases_by_keywords)]
        variations = self._get_variations(variators, token_phrases_by_keywords)
        self.keyword_by_token_phrase_variation = variations

    def _tokenize(self, raw_keywords):
        return {raw_kwd: tuple(nltk.word_tokenize(raw_kwd)) for raw_kwd in raw_keywords}

    def get_keywords(self):
        return self.keyword_by_token_phrase_variation

    def _get_variations(self, variators, token_phrases):
        keyword_by_token_phrase_variation = {}
        too_common_variations = set()
        for keyword, token_phrase in token_phrases.items():
            keyword_by_token_phrase_variation[token_phrase] = keyword
            for variator in variators:
                variations = variator.variate(token_phrase)
                for variation in variations:
                    if variation not in keyword_by_token_phrase_variation or keyword == \
                            keyword_by_token_phrase_variation[variation]:
                        keyword_by_token_phrase_variation[variation] = keyword
                    else:
                        old_keyword = keyword_by_token_phrase_variation[variation]
                        if keyword in old_keyword:
                            keyword_by_token_phrase_variation[variation] = keyword
                            continue
                        if old_keyword in keyword:
                            continue
                        too_common_variations.add(variation)
        for too_common_variation in too_common_variations:
            del keyword_by_token_phrase_variation[too_common_variation]
        return keyword_by_token_phrase_variation
