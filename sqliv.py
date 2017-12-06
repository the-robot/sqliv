# SQLiv v2.0
# Ghost (github.com/Hadesy2k)
# official.ghost@tuta.io

import sys
import argparse
from urlparse import urlparse

from src import std
from src import scanner
from src import reverseip
from src import serverinfo
from src.web import search
from src.crawler import Crawler


# search engine instance
bing   = search.Bing()
google = search.Google()
yahoo = search.Yahoo()

# crawler instance
crawler = Crawler()


def singlescan(url):
    """instance to scan single targeted domain"""

    if urlparse(url).query != '':
        result = scanner.scan([url])
        if result != []:
            # scanner.scan print if vulnerable
            # therefore exit
            return result

        else:
            print ""  # move carriage return to newline
            std.stdout("no SQL injection vulnerability found")
            option = std.stdin("do you want to crawl and continue scanning? [Y/N]", ["Y", "N"], upper=True)

            if option == 'N':
                return False

    # crawl and scan the links
    # if crawl cannot find links, do some reverse domain
    std.stdout("going to crawl {}".format(url))
    urls = crawler.crawl(url)

    if not urls:
        std.stdout("found no suitable urls to test SQLi")
        #std.stdout("you might want to do reverse domain")
        return False

    std.stdout("found {} urls from crawling".format(len(urls)))
    vulnerables = scanner.scan(urls)

    if vulnerables == []:
        std.stdout("no SQL injection vulnerability found")
        return False

    return vulnerables


def initparser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dork", help="SQL injection dork", type=str, metavar="inurl:example")
    parser.add_argument("-e", dest="engine", help="search engine [Bing, Google, and Yahoo]", type=str, metavar="bing, google, yahoo")
    parser.add_argument("-p", dest="page", help="number of websites to look for in search engine", type=int, default=10, metavar="100")
    parser.add_argument("-t", dest="target", help="scan target website", type=str, metavar="www.example.com")
    parser.add_argument('-r', dest="reverse", help="reverse domain", action='store_true')
    parser.add_argument('-o', dest="output", help="output result into json", type=str, metavar="result.json")


if __name__ == "__main__":
    initparser()
    args = parser.parse_args()

    # find random SQLi by dork
    if args.dork != None and args.engine != None:
        std.stdout("searching for websites with given dork")

        # get websites based on search engine
        if args.engine in ["bing", "google", "yahoo"]:
            websites = eval(args.engine).search(args.dork, args.page)
        else:
            std.stderr("invalid search engine")
            exit(1)

        std.stdout("{} websites found".format(len(websites)))

        vulnerables = scanner.scan(websites)

        if not vulnerables:
            std.stdout("you can still scan those websites by crawling or reverse domain.")
            option = std.stdin("do you want save search result? [Y/N]", ["Y", "N"], upper=True)

            if option == 'Y':
                std.stdout("saved as searches.txt")
                std.dump(websites, "searches.txt")

            exit(0)

        std.stdout("scanning server information")

        vulnerableurls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerableurls)
        # add db name to info
        for result, info in zip(vulnerables, table_data):
            info.insert(1, result[1])  # database name

        std.fullprint(table_data)


    # do reverse domain of given site
    elif args.target != None and args.reverse:
        std.stdout("finding domains with same server as {}".format(args.target))
        domains = reverseip.reverseip(args.target)

        if domains == []:
            std.stdout("no domain found with reversing ip")
            exit(0)

        # if there are domains
        std.stdout("found {} websites".format(len(domains)))

        # ask whether user wants to save domains
        std.stdout("scanning multiple websites with crawling will take long")
        option = std.stdin("do you want save domains? [Y/N]", ["Y", "N"], upper=True)

        if option == 'Y':
            std.stdout("saved as domains.txt")
            std.dump(domains, "domains.txt")

        # ask whether user wants to crawl one by one or exit
        option = std.stdin("do you want start crawling? [Y/N]", ["Y", "N"], upper=True)

        if option == 'N':
            exit(0)

        vulnerables = []
        for domain in domains:
            vulnerables_temp = singlescan(domain)
            if vulnerables_temp:
                vulnerables += vulnerables_temp

        std.stdout("finished scanning all reverse domains")
        if vulnerables == []:
            std.stdout("no vulnerables webistes from reverse domains")
            exit(0)

        std.stdout("scanning server information")

        vulnerableurls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerableurls)
        # add db name to info
        for result, info in zip(vulnerables, table_data):
            info.insert(1, result[1])  # database name

        std.fullprint(table_data)


    # scan SQLi of given site
    elif args.target:
        vulnerables = singlescan(args.target)

        if not vulnerables:
            exit(0)

        # show domain information of target urls
        std.stdout("getting server info of domains can take a few mins")
        table_data = serverinfo.check([args.target])

        std.printserverinfo(table_data)
        print ""  # give space between two table
        std.normalprint(vulnerables)
        exit(0)

    # print help message, if no parameter is provided
    else:
        parser.print_help()

    # dump result into json if specified
    if args.output != None:
        std.dumpjson(table_data, args.output)
        std.stdout("Dumped result into %s" % args.output)

