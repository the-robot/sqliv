import sys
import urllib2
from urlparse import urlparse

import sqlerrors
import useragents


def getHTML(url):
    """return HTML of the given url"""
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    header = useragents.get()
    request = urllib2.Request(url, None, header)

    try:
        reply = urllib2.urlopen(request)

    except urllib2.HTTPError, e:
        print >> sys.stderr, "[{}] HTTP error".format(e.code)

    except urllib2.URLError, e:
        print >> sys.stderr, "URL error, {}".format(e.reason)

    except:
        print >> sys.stderr, "HTTP exception"

    else:
        return reply.read()

    return False

def scan(url):
    """check SQL injection vulnerability"""
    domain = url.split("?")[0]  # domain with path without queries
    queries = urlparse(url).query.split("&")

    # no queries in url
    if not any(queries):
        return False

    for query in range(len(queries)):
        queries_temp = queries[:]  # clone queries for temp
        queries_temp[query] = queries_temp[query] + "'"
        website = domain + "?"

        for each in queries_temp:
            if each != queries_temp[-1]:
                website += each + "&"
            else:
                website += each

        html = getHTML(website)
        if html and sqlerrors.check(html):
            return True

    return False
