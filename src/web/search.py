# search vulnerabilities by dock

import sys

from lib import bing
from lib import google
from lib import yahoo
from urllib2 import HTTPError, URLError

bingsearch = bing.Bing()
yahoosearch = yahoo.Yahoo()

class Search:
    """basic search class that can be inherited by other search agents like Google, Yandex"""
    pass

class Google(Search):
    def search(self, query, pages=10):
        """search and return an array of urls"""

        urls = []

        try:
            for url in google.search(query, start=0, stop=pages):
                urls.append(url)
        except HTTPError:
            exit("[503] Service Unreachable")
        except URLError:
            exit("[504] Gateway Timeout")
        except:
            exit("Unknown error occurred")
        else:
            return urls

class Bing(Search):
    def search(self, query, pages=10):
        try:
            return bingsearch.search(query, stop=pages)
        except HTTPError:
            exit("[503] Service Unreachable")
        except URLError:
            exit("[504] Gateway Timeout")
        except:
            exit("Unknown error occurred")

class Yahoo(Search):
    def search(self, query, pages=1):
        try:
            return yahoosearch.search(query, pages)
        except HTTPError:
            exit("[503] Service Unreachable")
        except URLError:
            exit("[504] Gateway Timeout")
        except:
            exit("Unknown error occurred")
