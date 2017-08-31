# Unofficial Simple Yahoo Scraper by Ghost
# official.ghost@tuta.io

import urllib2
import bs4


DEFAULT_CONTENTYPE = "application/x-www-form-urlencoded; charset=UTF-8"
DEFAULT_USERAGENT = "yahoo search"


class Yahoo:
    """yahoo search engine scraper"""

    def __init__(self):
        self.yahoosearch = "https://search.yahoo.com/search;?p=%s&n=%s&b=%s"
        self.init_header()

    def init_header(self, contenttype=DEFAULT_CONTENTYPE, useragent=DEFAULT_USERAGENT):
        """initialize header"""

        self.contenttype = contenttype
        self.useragent = useragent

    def search(self, query, per_page=10, pages=1):
        """search urls from yahoo search"""

        # store searched urls
        urls = []

        for page in range(pages):
            yahoosearch = self.yahoosearch % (query, per_page, (pages+1)*10)

            request = urllib2.Request(yahoosearch)
            request.add_header("Content-type", self.contenttype)
            request.add_header("User-Agent", self.useragent)

            result = urllib2.urlopen(request).read()
            urls += self.parse_links(result)

        return urls

    def parse_links(self, html):
        """scrape results (url) from html"""

        # init with empty list
        links = []

        soup = bs4.BeautifulSoup(html, "lxml")
        for span in soup.findAll('div'):
            links += [a['href'] for a in span.findAll('a', {"class": " ac-algo fz-l ac-21th lh-24"}, href=True)\
                      if a['href'] not in links]

        return links

if __name__ == "__main__":
    yahoo = Yahoo()
    urls = yahoo.search("hello world", pages=1)

    print urls
