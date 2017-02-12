import re
from sqlierrors import getSqliErrors

def checkSqli(html):
    """ check for sql error message in given html """
    errors = getSqliErrors()
    results = {}
    for error, message in errors.iteritems():
        results[error] = re.search(message, html)
    return results