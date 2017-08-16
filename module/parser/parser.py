from collections import Counter

from .common_urls_remover import CommonUrlsRemover
from .company_name_url_parser import UpperLetterWordsExtractor, UrlsExtractor, CompanyNameUrlPairParser
from .result import Result
from .html_cleaner import HtmlCleaner
from .keywords_parser import KeywordsParser


class Parser:
    HTML_CLEANER = HtmlCleaner()
    KEYWORD_PARSER = KeywordsParser()

    EXTRACTORS = [UpperLetterWordsExtractor(), UrlsExtractor()]
    company_name_url_finder = CompanyNameUrlPairParser()

    def get_common_urls(self, all_urls):
        urls_counter = Counter(all_urls)
        too_common_urls = {url for url in urls_counter if urls_counter[url] > 1}
        return too_common_urls

    def parse(self, pages):
        keywords_by_url = {}
        all_urls = []
        token_tuples_best_pairs = {}
        for id_, url, raw_page, datetime in pages:
            keywords = set()
            company_single_names = []
            company_name_url_pairs = []
            if raw_page:
                soup = self.HTML_CLEANER.clean(raw_page)
                keywords = self.KEYWORD_PARSER.parse(soup)
                company_single_names = self.EXTRACTORS[0].get(soup)
                urls = self.EXTRACTORS[1].get(soup)
                company_name_url_pairs = self.company_name_url_finder.get_best_pair(company_single_names, urls)[:10]
                all_urls.extend(urls)
            keywords_by_url[url] = keywords
            token_tuples_best_pairs[url] = company_single_names, company_name_url_pairs
        common_urls_remover = CommonUrlsRemover(self.get_common_urls(all_urls))

        results = {}
        for id_, url, raw_page, datetime in pages:
            result = Result(None, keywords_by_url[url], None)
            tokens, pairs = token_tuples_best_pairs[url]
            new_pairs = common_urls_remover.delete_pairs_with_common_urls(pairs)
            if new_pairs and tokens:
                if new_pairs[0][2] / tokens[0][1] > 0.5:
                    site, name, dist = new_pairs[0]
                    result = Result(' '.join(name), keywords_by_url[url], site)
                else:
                    name = tokens[0][0]
                    result = Result(' '.join(name), keywords_by_url[url], None)
            if not new_pairs and tokens:
                name = tokens[0][0]
                result = Result(' '.join(name), keywords_by_url[url], None)
            if not tokens and new_pairs:
                site, name, dist = new_pairs[0]
                result = Result(' '.join(name), keywords_by_url[url], site)
            results[url] = result
        return results

