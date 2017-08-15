import re
from urlparse import urlparse

import html


def crawl(url):
    """crawl the links of the same given domain"""

    links = []

    try:
        result = html.getHTML(url)
    except KeyboardInterrupt:
        return links

    if result:
        # get only domain name
        domain = urlparse(url).netloc if urlparse(url).netloc != '' else urlparse(url).path.split("/")[0]

        for link in re.findall('<a href="(.*?)"', result):
            # www.example.com/index.(php|aspx|jsp)?query=1
            if re.search('(.*?)(.php\?|.asp\?|.apsx\?|.jsp\?)(.*?)=(.*?)', link):

                if link.startswith(("http", "www")) or domain in urlparse(link).path:
                    links.append(link)
                else:
                    links.append(domain + link if link.startswith("/") else domain + "/" + link)

    return links
