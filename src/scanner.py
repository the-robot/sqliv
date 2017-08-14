import time
import signal
import multiprocessing
from urlparse import urlparse

import io
import sqlerrors
import html


def scan(url):
    """check SQL injection vulnerability"""

    io.stdout("scanning {}".format(url), end="")

    domain = url.split("?")[0]  # domain with path without queries
    queries = urlparse(url).query.split("&")

    # no queries in url
    if not any(queries):
        return False

    website = domain + "?" + ("&".join([param + "'" for param in queries]))
    result = html.getHTML(website)
    if result and sqlerrors.check(result):
        io.showsign(" vulnerable")
        return True

    print ""  # move cursor to new line
    return False


def initChild():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def multiScan(urls):
    """scan multiple websites with multi processing"""

    vulnerables = []
    results = {}  # store scanned results

    childs = []  # store child processes
    max_processes = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(max_processes, initChild)

    for url in urls:
        def callback(result, url=url):
            results[url] = result
        childs.append(pool.apply_async(scan, (url, ), callback=callback))

    try:
        while True:
            time.sleep(0.5)
            if all([child.ready() for child in childs]):
                break
    except KeyboardInterrupt:
        io.stderr("stopping sqli scanning process")
        pool.terminate()
        pool.join()
    else:
        pool.close()
        pool.join()

    for url, result in results.items():
        if result == True:
            vulnerables.append(url)

    return vulnerables
