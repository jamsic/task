class CommonUrlsRemover:
    def __init__(self, urls):
        self.too_common_urls = urls

    def delete_pairs_with_common_urls(self, best_pairs):
        return list(filter(lambda x: x[0] not in self.too_common_urls, best_pairs))

