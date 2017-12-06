from __future__ import print_function

import time
import json
from termcolor import colored, cprint
from terminaltables import SingleTable


def stdin(message, params, upper=False, lower=False):
    """ask for option/input from user"""

    symbol = colored("[OPT]", "magenta")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")

    option = raw_input("{} {} {}: ".format(symbol, currentime, message))

    if upper:
        option = option.upper()
    elif lower:
        option = option.lower()

    while option not in params:
        option = raw_input("{} {} {}: ".format(symbol, currentime, message))

        if upper:
            option = option.upper()
        elif lower:
            option = option.lower()

    return option

def stdout(message, end="\n"):
    """print a message for user in console"""

    symbol = colored("[MSG]", "yellow")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    print("{} {} {}".format(symbol, currentime, message), end=end)

def stderr(message, end="\n"):
    """print an error for user in console"""

    symbol = colored("[ERR]", "red")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    print("{} {} {}".format(symbol, currentime, message), end=end)

def showsign(message):
    """show vulnerable message"""

    print(colored(message, "magenta"))

def dump(array, filename):
    """save the given array into a file"""

    with open(filename, 'w') as output:
        for data in array:
            output.write(data + "\n")

def dumpjson(array, filename='wtf.json'):
    """save the scanned result into a file as"""
    jsondata = {}

    for index, result in enumerate(array):
        jsondata[index] = {
            'url': result[0].encode('utf-8'),
            'db': result[1].encode('utf-8'),
            'server': result[2].encode('utf-8'),
            'lang': result[3].encode('utf-8')
        }

    with open(filename, 'w') as output:
        output.write(json.dumps(jsondata, indent=4))

def printserverinfo(data):
    """show vulnerable websites in table"""

    # [
    #   ["website", "server", "lang"],
    #   [sql.com", "apache", "php/5.5xxxx"]
    # ]

    # check if table column and data columns are the same
    if not all(isinstance(item, list) for item in data):
        stderr("program err, data must be two dimentional array")
        return

    title = " DOMAINS "
    table_data = [["website", "server", "lang"]] + data

    table = SingleTable(table_data, title)
    print(table.table)

def normalprint(data):
    """show vulnerable websites in table"""

    # [
    #   ["index", "url"],
    #   ["1", "sql.com"]
    # ]

    title = " VULNERABLE URLS "
    table_data = [["index", "url", "db"]]
    # add into table_data by one by one
    for index, url in enumerate(data):
        table_data.append([index+1, url[0], url[1]])

    table = SingleTable(table_data, title)
    print(table.table)

def fullprint(data):
    """show vulnerable websites in table with server info"""

    # [
    #   ["index", "url", "db", server", "lang"],
    #   ["1", "sql.com", "mysql", apache", "php/5.5xxx"]
    # ]

    title = " VULNERABLE URLS "
    table_data = [["index", "url", "db", "server", "lang"]]
    # add into table_data by one by one
    for index, each in enumerate(data):
        table_data.append([index+1, each[0], each[1], each[2][0:30], each[3][0:30]])

    table = SingleTable(table_data, title)
    print(table.table)
