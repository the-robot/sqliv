import sys
from urlparse import urlparse

import sqlerrors
import html


def scan(url):
    """check SQL injection vulnerability"""

    domain = url.split("?")[0]  # domain with path without queries
    queries = urlparse(url).query.split("&")

    # no queries in url
    if not any(queries):
        return False

    for query in range(len(queries)):
        queries_temp = queries[:]  # copy queries for temp
        queries_temp[query] = queries_temp[query] + "'"
        website = domain + "?"

        for each in queries_temp:
            if each != queries_temp[-1]:
                website += each + "&"
            else:
                website += each

        result = html.getHTML(website)
        if result and sqlerrors.check(result):
            return True

    return False
