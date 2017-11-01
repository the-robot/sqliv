# SQLiv v2.0
# Ghost (github.com/Hadesy2k)
# official.ghost@tuta.io


import argparse
from urlparse import urlparse

from src import io
from src import scanner
from src import crawler
from src import reverseip
from src import serverinfo
from src.web import search


"""
README
src/io
- io.stdout, io.stderr are used to show normal and error messages
- io.stdin is used to get input from user
- their printing format '[CODE] [CURRENTTIME] [MESSAGE]'
"""

# search engine instance
bing   = search.Bing()
google = search.Google()
yahoo = search.Yahoo()


def singlescan(url):
    """instance to scan single targeted domain"""

    if urlparse(url).query != '':
        if scanner.scan([url]) != []:
            # scanner.scan print if vulnerable
            # therefore exit
            exit(0)

        else:
            print ""  # move carriage return to newline
            io.stdout("no SQL injection vulnerability found")
            option = io.stdin("do you want to crawl and continue scanning? [Y/N]", ["Y", "N"], upper=True)

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
    vulnerables = scanner.scan(urls)

    if vulnerables == []:
        io.stdout("no SQL injection vulnerability found")
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


if __name__ == "__main__":
    initparser()
    args = parser.parse_args()

    # find random SQLi by dork
    if args.dork != None and args.engine != None:
        io.stdout("searching for websites with given dork")

        # get websites based on search engine
        if args.engine in ["bing", "google", "yahoo"]:
            websites = eval(args.engine).search(args.dork, args.page)
        else:
            io.stderr("invalid search engine")
            exit(1)

        io.stdout("{} websites found".format(len(websites)))

        vulnerables = scanner.scan(websites)

        if not vulnerables:
            io.stdout("you can still scan those websites by crawling or reverse domain.")
            option = io.stdin("do you want save search result? [Y/N]", ["Y", "N"], upper=True)

            if option == 'Y':
                io.stdout("saved as searches.txt")
                io.dump(websites, "searches.txt")

            exit(0)

        io.stdout("scanning server information")

        vulnerableurls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerableurls)
        # add db name to info
        for result, info in zip(vulnerables, table_data):
            info.insert(1, result[1])  # database name

        io.fullprint(table_data)


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
        option = io.stdin("do you want save domains? [Y/N]", ["Y", "N"], upper=True)

        if option == 'Y':
            io.stdout("saved as domains.txt")
            io.dump(domains, "domains.txt")

        # ask whether user wants to crawl one by one or exit
        option = io.stdin("do you want start crawling? [Y/N]", ["Y", "N"], upper=True)

        if option == 'N':
            exit(0)

        vulnerables = []
        for domain in domains:
            vulnerables_temp = singlescan(domain)
            if vulnerables_temp:
                vulnerables += vulnerables_temp

        io.stdout("finished scanning all reverse domains")
        if vulnerables == []:
            io.stdout("no vulnerables webistes from reverse domains")
            exit(0)

        io.stdout("scanning server information")

        vulnerableurls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerableurls)
        # add db name to info
        for result, info in zip(vulnerables, table_data):
            info.insert(1, result[1])  # database name

        io.fullprint(table_data)


    # scan SQLi of given site
    elif args.target:
        vulnerables = singlescan(args.target)

        if not vulnerables:
            exit(0)

        # show domain information of target urls
        io.stdout("getting server info of domains can take a few mins")
        table_data = serverinfo.check([args.target])

        io.printserverinfo(table_data)
        print ""  # give space between two table
        io.normalprint(vulnerables)


    # print help message, if no parameter is provided
    else:
        parser.print_help()
