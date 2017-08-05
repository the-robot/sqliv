# Reverse Domain Lookup

import re
from urlparse import urlparse

from scanner import getHTML


def reverseip(url):
    domain = urlparse(url).netloc if urlparse(url).netloc != '' else urlparse(url).path.split("/")[0]
    sites = re.findall("<td>(.*?)</td>", getHTML("http://viewdns.info/reverseip/?host=%s&t=1"%(domain)))[3:]
    return sites
