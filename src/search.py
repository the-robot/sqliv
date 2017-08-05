# search vulnerabilities by dock

import sys
from libs import google
from urllib2 import HTTPError


class Search:
    """basic search class that can be inherited by other search agents like Google, Yandex"""

    def dump(self, array, filename):
        """save the given searched result [list]"""
        with open(filename, 'w') as output:
            for data in array:
                output.write(data + "\n")


class Google(Search):
    """search vulnerabilities by Google's dock"""

    def search(self, query, pages=1):
        """search and return an array of urls"""
        urls = []

        try:
            for url in google.search(query, stop=pages):
                urls.append(url)
        except HTTPError:
            exit("[503] Service Unreachable")
        except:
            exit("Unexpected error:", sys.exc_info()[0])

        return urls
