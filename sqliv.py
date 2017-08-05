import argparse

from src import search
from src import scanner
from src import crawler
from src import reverse
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
            print "[VUL] SQL injection vulnerability found"
            vulnerables.append(website)

    if vulnerables:
        io.stdout("vulnerable websites")
        for each in vulnerables: print("- " + each)
        return True

    io.stdout("no vulnerable websites found")
    return False


def initParser():
    """initialize parser arguments"""

    global parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="SQL injection dork", type=str)
    parser.add_argument("-e", help="search engine [Google | Yandex]", type=str)
    parser.add_argument("-p", help="number of websites to look for in search engine", type=int, default=10)
    parser.add_argument("-t", help="scan target website", type=str)
    parser.add_argument('-s', action='store_true')


if __name__ == "__main__":
    initParser()
    args = parser.parse_args()

    try:
        if args.d is not None and args.e is not None:
            io.stdout("searching for website with given dork")

            # get websites based on search engine
            if args.e == "google":
                websites = google.search(args.d, args.p)
            else:
                io.stderr("invalid search engine")
                exit(1)

            io.stdout("{} websites found".format(len(websites)))

            if not massivescan(websites):
                io.stdout("you can still scan those websites by crawling or reverse domain.")
                option = io.stdin("do you want save search result? [Y/N]").upper()
                while option != 'Y' and option != 'N':
                    option = io.stdin("do you want save search result? [Y/N]").upper()

                if option == 'Y':
                    io.stdout("saved as searches.txt")
                    io.dump(websites, "searches.txt")
                    exit(0)

        elif args.t is not None and args.s:
            io.stdout("scanning {}".format(args.t))

            if scanner.scan(args.t):
                print "[VUL] SQL injection vulnerability found"

            else:
                option = io.stdin("do you want to crawl and continue scanning? [Y/N]").upper()
                while option != 'Y' and option != 'N':
                    option = io.stdin("do you want to crawl and continue scanning? [Y/N]").upper()

                if option == 'N':
                    exit(0)

                # crawl and scan the links
                # if crawl cannot find links, do some reverse domain
                urls = crawler.crawl(args.t)
                if not massivescan(urls):
                    print "TODO: IMPLEMENT REVERSE DOMAIN"
                    exit(0)

    except KeyboardInterrupt:
        io.stderr("exiting program...")
        exit(1)
