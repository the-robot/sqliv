# This is a universal google dorker
# You can use this for getting urls of every dork you know.
# Just input the dork and number of pages,
# the script will take care of the rest.

#-----------------------------------------------------
# Name : Google Dorker.py
# Version : beta
# Author : Anubis
# Contact : z3r0.mhu@gmail.com
# Facebook : www.facebook.com/zerouplink
#-----------------------------------------------------

###########################################################

import time,sys

class bcolors:
    RED = '\033[91m'
    BOLD = '\033[1m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    WARNING = '\033[93m'

RED = bcolors.RED
WHITE = bcolors.BOLD
GREEN = bcolors.OKGREEN
YELLOW = bcolors.WARNING
END = bcolors.ENDC

try:
    from pygoogle import pygoogle
except ImportError:
    print "[!] Pygoogle file not found!"
    print "[!] Program can't continue"
    print "[!] Get pygoogle file from this link"
    print "\n\t\t[ http://pastebin.com/Q0xVF2nV ]"

class dorker():

    def __init__(self):

        search_dork = raw_input(WHITE + "\nEnter Dork : " + END)
        pages = input(WHITE + "Enter number of pages : " + END)
        print
        f_output = "googled.txt"

        if search_dork != '' and pages != '':
            self.dork(search_dork,pages,f_output)

    def dork(self,search_term,p,output):
        print YELLOW + "[+] " + END + WHITE + "Searching for " + END + "%s " % search_term
        gs = pygoogle(search_term)
        gs.pages = p
        print YELLOW + "[+] " + END + WHITE + "Results Found : " + END + "%s " % (gs.get_result_count())
        if gs.get_result_count() == 0: print RED + "[-] " + END + WHITE + "No Results Found" + END; time.sleep(1); sys.exit()

        print YELLOW + "[+] " + END + WHITE + "Fetching " + END + "[%s] Results " % (gs.get_result_count())
        url_list = gs.get_urls()

        if len(url_list) == 0:
            print YELLOW + "[!] " + END + WHITE + "Got 0 URLs" + END
            print RED + "[!] " + END + WHITE + "Nothing to save" + END
            time.sleep(1)
            sys.exit()
            
        elif len(url_list) > 1:
            print YELLOW + "[+] " + END + WHITE + "Got " + END + "[%s] URLs" % (len(url_list))
            print YELLOW + "[+] " + END + WHITE + "Writing URLs to " + END + "[%s] " % (output)

            with open(output,'w') as w_file:
                for i in url_list: w_file.write(i+'\n')
            print YELLOW + "[+] " + END + WHITE + "URLs saved to " + END + "[%s] " % (output)

            time.sleep(2)


def main():
    google = dorker()


if __name__ == '__main__':
    main()
