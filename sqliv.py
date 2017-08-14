# SQLiv v2.0
# 09/08/2017
# Ghost (github.com/Hadesy2k | www.hadesy2k.github.io)
# official.ghost@tuta.io
# GNU GPL <3.0>


import argparse
from urlparse import urlparse

from src import io
from src import search
from src import scanner
from src import crawler
from src import reverseip
from src import serverinfo


"""
README
src/io
- io.stdout, io.stderr are used to show normal and error messages
- io.stdin is used to get input from user
- their printing format '[CODE] [CURRENTTIME] [MESSAGE]'
"""

# search engine instance
google = search.Google()


def singleScan(url):
    """instance to scan single targeted domain"""

    if urlparse(url).query != '':
        if scanner.scan(url):
            # scanner.scan print if vulnerable
            # therefore exit here
            exit(0)

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
    urls = crawler.crawl(url)

    if not urls:
        io.stdout("found no suitable urls to test SQLi")
        #io.stdout("you might want to do reverse domain")
        return False

    io.stdout("found {} urls from crawling".format(len(urls)))
    vulnerables = scanner.multiScan(urls)

    if vulnerables == []:
        io.stdout("no SQL injection vulnerability found")
        return False

    return vulnerables


def getServerInfo(urls):
    """get server information of given url and return as array"""

    table_data = []
    skip = False  # skip getting server info

    for each in urls:
        if not skip:
            try:
                server_info = serverinfo.check(each)
            except KeyboardInterrupt:
                skip = True
                io.stdout("skipping server info scanning process")
                server_info = ['-', '-']
        else:
            server_info = ['-', '-']

        table_data.append([each, server_info[0], server_info[1]])

    return table_data


def showDomainInfo(urls):
    """return array of urls with server info"""

    io.stdout("getting server info of domains can take a few mins")
    domains_info = []

    for each in urls:
        try:
            server_info = serverinfo.check(each)
        except KeyboardInterrupt:
            server_info = ["-", "-"]

        domains_info.append([each, server_info[0], server_info[1]])

    # print in table
    io.printServerInfo(domains_info)


def initParser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dork", help="SQL injection dork", type=str, metavar="inurl:xxx")
    parser.add_argument("-e", dest="engine", help="search engine [Google only for now]", type=str, metavar="google")
    parser.add_argument("-p", dest="page", help="number of websites to look for in search engine", type=int, default=10, metavar="100")
    parser.add_argument("-t", dest="target", help="scan target website", type=str, metavar="www.xxx.com")
    parser.add_argument('-r', dest="reverse", help="reverse domain", action='store_true')


if __name__ == "__main__":
    initParser()
    args = parser.parse_args()

    # find random SQLi by dork
    if args.dork != None and args.engine != None:
        io.stdout("searching for websites with given dork")

        # get websites based on search engine
        if args.engine == "google":
            websites = google.search(args.dork, args.page)
        else:
            io.stderr("invalid search engine")
            exit(1)

        io.stdout("{} websites found".format(len(websites)))

        vulnerables = scanner.multiScan(websites)

        if not vulnerables:
            io.stdout("you can still scan those websites by crawling or reverse domain.")
            option = io.stdin("do you want save search result? [Y/N]").upper()
            while option != 'Y' and option != 'N':
                option = io.stdin("do you want save search result? [Y/N]").upper()

            if option == 'Y':
                io.stdout("saved as searches.txt")
                io.dump(websites, "searches.txt")

            exit(0)

        io.stdout("scanning server information")
        table_data = getServerInfo(vulnerables)
        io.printVulnerablesWithInfo(table_data)


    # do reverse domain of given site
    elif args.target != None and args.reverse:
        io.stdout("finding domains with same server as {}".format(args.target))
        domains = reverseip.reverseip(args.target)

        if domains == []:
            io.stdout("no domain found with reversing ip")
            exit(0)

        # if there are domains
        io.stdout("found {} websites".format(len(domains)))

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

        io.stdout("scanning server information")
        table_data = getServerInfo(vulnerables)
        io.printVulnerablesWithInfo(table_data)


    # scan SQLi of given site
    elif args.target:
        vulnerables = singleScan(args.target)

        if not vulnerables:
            exit(0)

        # show domain information of target urls
        showDomainInfo([args.target])
        print ""  # give space between two table
        io.printVulnerables(vulnerables)
