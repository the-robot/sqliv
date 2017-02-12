def getSqliErrors():
    """ return a dictionary of sqli errors """
    return {
        "mysql_error_1": "You have an error in your SQL syntax",
        "mysql_error_2": "supplied argument is not a valid MySQL result resource",
        "mysql_error_3": "check the manual that corresponds to your MySQL",
        "mysql_error_4": "mysql_fetch_array(): supplied argument is not a valid MySQL",
        "mysql_error_5": "function fetch_row()",
        "mssql_error_1": "Microsoft OLE DB Provider for ODBC Drivers error"
    }