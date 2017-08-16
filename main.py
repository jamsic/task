import csv
from module import Crawler, Parser, UrlsProvider


import nltk
nltk.download('punkt')

filename = 'answer.csv'

crawler = Crawler()
parser = Parser()
url_provider = UrlsProvider()

urls = list(url_provider.get_urls())
crawler.crawl(urls)

pages = list(crawler.get_pages())
pages = list(filter(lambda x: x[1] in urls, pages))
results = parser.parse(pages)
with open(filename, 'a', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    data = []
    for url in results:
        data.append([url, results[url].company_name, ', '.join(results[url].tools), results[url].website])
    a.writerows(data)

