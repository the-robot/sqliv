from urlparse import urlparse

import sqlerrors
import html


def scan(url):
    """check SQL injection vulnerability"""

    domain = url.split("?")[0]  # domain with path without queries
    queries = urlparse(url).query.split("&")

    # no queries in url
    if not any(queries):
        return False

    website = domain + "?" + ("&".join([param + "'" for param in queries]))
    result = html.getHTML(website)
    if result and sqlerrors.check(result):
        return True

    return False
