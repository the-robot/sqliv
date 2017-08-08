# SQLiv v2.0
# 09/08/2017
# Ghost (github.com/Hadesy2k | www.hadesy2k.github.io)
# official.ghost@tuta.io
# GNU GPL <3.0>


import argparse
from urlparse import urlparse

from src import search
from src import scanner
from src import crawler
from src import reverseip
from src import io


"""
README
src/io
- io.stdout, io.stderr are used to show normal and error messages
- io.stdin is used to get input from user
- their printing format '[CODE] [CURRENTTIME] [MESSAGE]'
"""

# search engine instance
google = search.Google()


def massivescan(websites):
    """scan multiple websites / urls"""

    # scan each website one by one
    vulnerables = []
    for website in websites:
        io.stdout("scanning {}".format(website))
        if scanner.scan(website):
            io.stdout("SQL injection vulnerability found")
            vulnerables.append(website)

    if vulnerables:
        return vulnerables

    io.stdout("no vulnerable websites found")
    return False


def singleScan(url):
    """instance to scan single targeted domain"""

    if urlparse(url).query != '':
        io.stdout("scanning {}".format(url))

        if scanner.scan(url):
            print "[VUL] SQL injection vulnerability found"

        else:
            io.stdout("no SQL injection vulnerability found")

            option = io.stdin("do you want to crawl and continue scanning? [Y/N]").upper()
            while option != 'Y' and option != 'N':
                option = io.stdin("do you want to crawl and continue scanning? [Y/N]").upper()

            if option == 'N':
                return False

    # crawl and scan the links
    # if crawl cannot find links, do some reverse domain
    io.stdout("crawling {}".format(url))
    websites = crawler.crawl(url)
    if not websites:
        io.stdout("found no suitable urls to test SQLi")
        #io.stdout("you might want to do reverse domain")
        return False

    io.stdout("found {} urls from crawling".format(len(websites)))
    vulnerables = massivescan(websites)

    if vulnerables == []:
        io.stdout("no SQL injection vulnerability found")
        return False

    return vulnerables


def initParser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="SQL injection dork", type=str)
    parser.add_argument("-e", help="search engine [Google only for now]", type=str)
    parser.add_argument("-p", help="number of websites to look for in search engine", type=int, default=10)
    parser.add_argument("-t", help="scan target website", type=str)
    parser.add_argument('-r', help="reverse domain", action='store_true')


if __name__ == "__main__":
    initParser()
    args = parser.parse_args()

    # find random SQLi by dork
    if args.d is not None and args.e is not None:
        io.stdout("searching for website with given dork")

        # get websites based on search engine
        if args.e == "google":
            websites = google.search(args.d, args.p)
        else:
            io.stderr("invalid search engine")
            exit(1)

        io.stdout("{} websites found".format(len(websites)))

        vulnerables = massivescan(websites)

        if not vulnerables:
            io.stdout("you can still scan those websites by crawling or reverse domain.")
            option = io.stdin("do you want save search result? [Y/N]").upper()
            while option != 'Y' and option != 'N':
                option = io.stdin("do you want save search result? [Y/N]").upper()

            if option == 'Y':
                io.stdout("saved as searches.txt")
                io.dump(websites, "searches.txt")

            exit(0)

        io.stdout("vulnerable websites")
        for url in vulnerables:
            print("- " + url)


    # do reverse domain of given site
    elif args.t is not None and args.r:
        io.stdout("finding domains with same server as {}".format(args.t))
        domains = reverseip.reverseip(args.t)

        if domains == []:
            io.stdout("no domain found with reversing ip")
            exit(0)

        # if there are domains
        io.stdout("found {} websites".format(len(domains)))
        for domain in domains: print("- " + domain)

        # ask whether user wants to save domains
        io.stdout("scanning multiple websites with crawling will take long")
        option = io.stdin("do you want save domains? [Y/N]").upper()
        while option != 'Y' and option != 'N':
            option = io.stdin("do you want save domains? [Y/N]").upper()

        if option == 'Y':
            io.stdout("saved as domains.txt")
            io.dump(domains, "domains.txt")

        # ask whether user wants to crawl one by one or exit
        option = io.stdin("do you want start crwaling? [Y/N]").upper()
        while option != 'Y' and option != 'N':
            option = io.stdin("do you want start crwaling? [Y/N]").upper()

        if option == 'N':
            exit(0)

        vulnerables = []
        for domain in domains:
            vulnerables_temp = singleScan(domain)
            if vulnerables_temp:
                vulnerables += vulnerables_temp

        io.stdout("finished scanning all reverse domains")
        if vulnerables == []:
            io.stdout("no vulnerables webistes from reverse domains")
            exit(0)

        io.stdout("vulnerable websites")
        for url in vulnerables:
            print("- " + url)


    # scan SQLi of given site
    elif args.t is not None:
        vulnerables = singleScan(args.t)

        if not vulnerables:
            exit(0)

        io.stdout("vulnerable websites")
        for url in vulnerables:
            print("- " + url)
