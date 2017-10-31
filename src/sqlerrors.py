import re

sql_errors = {
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r".*MySQL Query fail.*", r"Fatal error.*:.*"),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*"),
    "Microsoft SQL Server": (r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string"),
    "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine", r"Fatal error.*Uncaught exception.*"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error"),
    "SQLite": (r"SQLite/JDBCDriver",r"System.Data.SQLite.SQLiteException"),
    "MariaDB": (r".*SQL syntax;.*MariaDB.*"),
    #"Sybase": (r"(?\i)Warning.*sybase.*")
}


def check(html):
    """check SQL error is in HTML or not"""
    for db, errors in sql_errors.items():
        for error in errors:
            regexp = re.compile(error)
            if regexp.search(html):
                #print "\n" + db
                return True, db
    return False
