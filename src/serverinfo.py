# get server information of given domain

import time
import signal
import multiprocessing
import bs4
from urlparse import urlparse

import io
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


def initChild():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def multiCheck(urls):
    """get many domains' server info with multi processing"""

    results = {}  # store results

    childs = []  # store child processes
    max_processes = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(max_processes, initChild)

    for url in urls:
        def callback(result, url=url):
            results[url] = result
        childs.append(pool.apply_async(check, (url, ), callback=callback))

    try:
        while True:
            time.sleep(0.5)
            if all([child.ready() for child in childs]):
                break
    except KeyboardInterrupt:
        io.stderr("skipping server info scanning process")
        pool.terminate()
        pool.join()
    else:
        pool.close()
        pool.join()

    return results
