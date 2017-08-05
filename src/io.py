import time
from termcolor import colored, cprint


def stdin(message):
    """ask for option/input from user"""
    symbol = colored("[OPT]", "magenta")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    return raw_input("{} {} {}: ".format(symbol, currentime, message))


def stdout(message):
    """print a message for user in console"""
    symbol = colored("[MSG]", "yellow")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    print "{} {} {}".format(symbol, currentime, message)


def stderr(message):
    """print n error for user in console"""
    symbol = colored("[ERR]", "red")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    print "{} {} {}".format(symbol, currentime, message)


def dump(array, filename):
    """save the given array into a file"""
    with open(filename, 'w') as output:
        for data in array:
            output.write(data + "\n")
