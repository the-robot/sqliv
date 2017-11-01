# get server information of given domain

import time
import signal
import multiprocessing
import bs4
from urlparse import urlparse

import io
from web import web


def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def check(urls):
    """get many domains' server info with multi processing"""

    domains_info = []  # return in list for termtable input
    results = {}  # store results

    childs = []  # store child processes
    max_processes = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(max_processes, init)

    for url in urls:
        def callback(result, url=url):
            results[url] = result
        childs.append(pool.apply_async(__getserverinfo, (url, ), callback=callback))

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

    # if user skipped the process, some may not have information
    # so put - for empty data
    for url in urls:
        if url in results.keys():
            data = results.get(url)
            domains_info.append([url, data[0], data[1]])
            continue

        domains_info.append([url, '', ''])

    return domains_info


def __getserverinfo(url):
    """get server name and version of given domain"""

    url = urlparse(url).netloc if urlparse(url).netloc != '' else urlparse(url).path.split("/")[0]

    info = []  # to store server info
    url = "https://aruljohn.com/webserver/" + url

    try:
        result = web.gethtml(url)
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
