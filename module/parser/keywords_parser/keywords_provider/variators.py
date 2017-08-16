from collections import Counter


class InBracketsVariator:
    LEFT = '('
    RIGHT = ')'
    BRACKET_SYMBOLS = {LEFT, RIGHT}

    def variate(self, token_tuple):
        in_brackets = []
        if self.BRACKET_SYMBOLS.issubset(set(token_tuple)):
            in_brackets.append(token_tuple[token_tuple.index(self.LEFT) + 1:
            token_tuple.index(self.RIGHT)])
        return in_brackets


class OutBracketsVariator:
    LEFT = '('
    RIGHT = ')'
    BRACKET_SYMBOLS = {LEFT, RIGHT}

    def variate(self, token_tuple):
        out_brackets = []
        if self.BRACKET_SYMBOLS.issubset(set(token_tuple)):
            out_brackets.append(token_tuple[:token_tuple.index(self.LEFT)] +
                                token_tuple[token_tuple.index(self.RIGHT) + 1:])
        return out_brackets


class CompanyNameVariator:
    def __init__(self, keyword_tokens):
        tokens_counter = Counter()
        common_words = Counter()
        for token_tuple in keyword_tokens.values():
            for i in range(1, len(token_tuple)):
                tokens_counter.update([token_tuple[:i]])
                common_words.update([token_tuple[i:]])
        self.company_names = {token for token in tokens_counter if tokens_counter[token] > 1}
        self.too_common_words = {token for token in common_words if common_words[token] > 1}

    def _contains_words(self, token_tuple):
        return any([t.isalpha() for t in token_tuple])

    def variate(self, token_tuple):
        variations = set()
        for i in range(1, len(token_tuple)):
            if token_tuple[:i] in self.company_names:
                if token_tuple[i:] and self._contains_words(token_tuple[i:]):
                    if token_tuple[i:] not in self.too_common_words:
                        variations.add(token_tuple[i:])
        return variations
