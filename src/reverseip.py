# Reverse Domain Lookup

import sys
import urllib
import urllib2
import json
from urlparse import urlparse

import useragents


def reverseip(url):
    """return domains from given the same server"""

    # get only domain name
    url = urlparse(url).netloc if urlparse(url).netloc != '' else urlparse(url).path.split("/")[0]

    source = "http://domains.yougetsignal.com/domains.php"
    useragent = useragents.get()
    contenttype = "application/x-www-form-urlencoded; charset=UTF-8"

    # POST method
    opener = urllib2.build_opener(
        urllib2.HTTPHandler(), urllib2.HTTPSHandler())
    data = urllib.urlencode([('remoteAddress', url), ('key', '')])

    request = urllib2.Request(source, data)
    request.add_header("Content-type", contenttype)
    request.add_header("User-Agent", useragent)

    try:
        result = urllib2.urlopen(request).read()

    except urllib2.HTTPError, e:
        print >> sys.stderr, "[{}] HTTP error".format(e.code)

    except urllib2.URLError, e:
        print >> sys.stderr, "URL error, {}".format(e.reason)

    except:
        print >> sys.stderr, "HTTP exception"

    obj = json.loads(result)

    # if successful
    if obj["status"] == 'Success':
        domains = []
        for domain in obj["domainArray"]:
            domains.append(domain[0])
        return domains

    print >> sys.stderr, "[ERR] {}".format(obj["message"])
    return []
