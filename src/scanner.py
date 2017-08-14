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


def multiScan(urls):
    """scan multiple websites with multi processing"""

    vulnerables = []  # store vulnerable websites
    max_processes = multiprocessing.cpu_count() * 2
    data = multiprocessing.Pool(max_processes).map(scan, urls)

    for each in zip(data, urls):
        if each[0] == True:
            vulnerables.append(each[1])

    return vulnerables
