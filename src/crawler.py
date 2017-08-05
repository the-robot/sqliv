import re
from urlparse import urlparse

from scanner import getHTML


def crawl(url):
    """crawl the links of the same given domain"""

    links = []
    html = getHTML(url)

    if html:
        domain = urlparse(url).netloc if urlparse(url).netloc != '' else urlparse(url).path.split("/")[0]
        print "Domain: " + domain

        for link in re.findall('<a href="(.*?)"', html):

            # www.example.com/index.(php|aspx|jsp)?query=1
            if re.search('(.*?)(.php\?|.asp\?|.apsx\?|.jsp\?)(.*?)=(.*?)', link):

                if link.startswith(("http", "www")) and domain in urlparse(link).path:
                    links.append(link)
                else:
                    links.append(domain + link if link.startswith("/") else domain + "/" + link)

    return links
