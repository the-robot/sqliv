# This is a universal google dorker
# You can use this for getting urls of every dork you know.
# Just input the dork and number of pages,
# the script will take care of the rest.

# -----------------------------------------------------
# Name : Google Dorker.py
# Version : beta
# Author : Anubis
# Contact : z3r0.mhu@gmail.com
# Facebook : www.facebook.com/zerouplink
# -----------------------------------------------------

###########################################################

import time
import sys

try:
    from pygoogle import pygoogle
except ImportError:
    print "[!] Pygoogle file not found!"
    print "[!] Program can't continue"
    print "[!] Get pygoogle file from this link"
    print "[ http://pastebin.com/Q0xVF2nV ]"


class dorker():
    def __init__(self):

        search_dork = raw_input("\nEnter Dork : ")
        pages = input("Enter number of pages : ")
        print
        f_output = "sites.txt"

        if search_dork != '' and pages != '':
            self.dork(search_dork, pages, f_output)

    def dork(self, search_term, p, output):
        print "[+] Searching for %s " % search_term
        gs = pygoogle(search_term)
        gs.pages = p
        print "[+] Results Found : %s " % (gs.get_result_count())
        if gs.get_result_count() == 0:
            print "[-] No Results Found"
            time.sleep(1)
            sys.exit()

        print "[+] Fetching [%s] Results" % (gs.get_result_count())
        url_list = gs.get_urls()

        if len(url_list) == 0:
            print "[!] Got 0 URLs"
            print "[!] Nothing to save"
            time.sleep(1)
            sys.exit()

        elif len(url_list) > 1:
            print "[+] Got [%s] URLs" % (len(url_list))
            print "[+] Writing URLs to [%s] " % (output)

            with open(output, 'w') as w_file:
                for i in url_list:
                    w_file.write(i + '\n')
            print "[+] URLs saved to [%s] " % (output)

            time.sleep(2)


def main():
    dorker()


if __name__ == '__main__':
    main()
