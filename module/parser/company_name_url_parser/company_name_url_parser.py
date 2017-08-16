import numpy as np

from .levenstein import Levenshtein


class CompanyNameUrlPairParser:
    LEVENSTEIN = Levenshtein()

    def url_token_distance(self, url, token):
        url_parts = url.split('.')
        url_part_len = max({len(url_part) for url_part in url_parts})
        url_parts = filter(lambda x: len(x) == url_part_len, url_parts)
        return min([self.LEVENSTEIN.distance(url_part, token) for url_part in url_parts])

    def get_best_pair(self, token_tuples, urls):
        dst = []
        for token_tuple in token_tuples:
            full_token = ''.join(token_tuple[0])
            full_lower_token = full_token.lower()
            for url in urls:
                leven_dist = self.url_token_distance(url.lower(), full_lower_token)
                dist = urls[url] * (token_tuple[1]) / np.exp(leven_dist) * len(token_tuple[0])
                dst.append((url, token_tuple[0], dist), )
        return sorted(dst, key=lambda x: -x[2])

