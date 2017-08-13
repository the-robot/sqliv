import sys
import urllib2
from urlparse import urlparse

import useragents


def getHTML(url):
    """return HTML of the given url"""

    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    header = useragents.get()
    request = urllib2.Request(url, None, header)

    try:
        reply = urllib2.urlopen(request, timeout=10)

    except urllib2.HTTPError, e:
        #print >> sys.stderr, "[{}] HTTP error".format(e.code)
        pass

    except urllib2.URLError, e:
        #print >> sys.stderr, "URL error, {}".format(e.reason)
        pass

    except KeyboardInterrupt:
        raise KeyboardInterrupt

    except:
        #print >> sys.stderr, "HTTP exception"
        pass

    else:
        return reply.read()

    return False
