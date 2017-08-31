import re
from urlparse import urlparse

import html

def parameterControl(URL):
    for site in links:
        if URL.split("=")[0] in site:
            return False
                        
    return True

def crawl(url):
    """crawl the links of the same given domain"""
    global links

    links = []

    try:
        result, URL = html.getHTML(url, lastURL=True)
    except:
        return None

    if result:
        # get only domain name
        domain = 'http://' + '/'.join(URL.split('/')[2:-1]) + '/' if len(URL.split('/')) >= 4 else URL.rstrip('/') + '/'

        for link in re.findall('<a href="(.*?)"', result):
            # www.example.com/index.(php|aspx|jsp)?query=1
            if re.search('(.*?)(.php\?|.asp\?|.apsx\?|.jsp\?)(.*?)=(.*?)', link):
                if parameterControl(link) == True:
                    if link.startswith(("http", "www")) or domain in urlparse(link).path:
                        links.append(link)
                    else:
                        links.append(domain + link if link.startswith("/") else domain + link)

    return links
