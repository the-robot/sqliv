sql_errors = {
    'SQL syntax error': "error in your SQL syntax",
    'Query failed': "Query failed",
    'Bad argument': "supplied argument is not a valid MySQL result resource in",
    'JET DBE error': "Microsoft JET Database Engine error '80040e14'",
    'Unknown error': "Error:unknown",
    'Fatal error': "Fatal error",
    'MySQL fetch': "mysql_fetch",
    'Syntax error': "Syntax error"
}


def check(html):
    """check SQL error is in HTML or not"""

    for error in sql_errors.values():
        if error in html:
            return True
    return False
