# get server information of given domain

import bs4
from urlparse import urlparse

import html


def check(url):
    """get server name and version of given domain"""

    url = urlparse(url).netloc if urlparse(url).netloc != '' else urlparse(url).path.split("/")[0]

    info = []  # to store server info
    url = "https://aruljohn.com/webserver/" + url

    try:
        result = html.getHTML(url)
    except KeyboardInterrupt:
        raise KeyboardInterrupt

    try:
        soup = bs4.BeautifulSoup(result, "lxml")
    except:
        return ['', '']

    if soup.findAll('p', {"class" : "err"}):
        return ['', '']

    for row in soup.findAll('tr'):
        if row.findAll('td', {"class": "title"}):
            info.append(row.findAll('td')[1].text.rstrip('\r'))

    return info
