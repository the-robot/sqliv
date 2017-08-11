from __future__ import print_function

import time
from termcolor import colored, cprint
from terminaltables import SingleTable


def stdin(message):
    """ask for option/input from user"""

    symbol = colored("[OPT]", "magenta")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    return raw_input("{} {} {}: ".format(symbol, currentime, message))


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


def printServerInfo(data):
    """show vulnerable websites in table"""

    # check if table column and data columns are the same
    if not all(isinstance(item, list) for item in data):
        stderr("program err, data must be two dimentional array")
        return

    title = " DOMAINS "
    table_data = [["website", "server", "technology"]] + data

    table = SingleTable(table_data, title)
    print(table.table)


def printVulnerables(data):
    """show vulnerable websites in table"""

    title = " VULNERABLE URLS "
    table_data = [["index", "url"]]
    # add into table_data by one by one
    for index, url in  enumerate(data):
        table_data.append([index+1, url])

    table = SingleTable(table_data, title)
    print(table.table)
