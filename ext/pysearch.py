#!/usr/bin/env python

# 30/11/2016
# Ghost (github.com/Hadesy2k)
# official.ghost@tuta.io
# GNU GPL <3.0>

import sys
from google import search
from urllib2 import HTTPError


class main:
    """ This class used to search vulnerable website
        by searching on Google with SQLi dork given from user
    """

    def __init__(self):
        print "\nEnter SQLi Dork without 'inurl:'"
        query = raw_input("Dork: ")
        query = "inurl:" + query
        pages = input("Enter number of pages: ")
        print  # printing empty new line
        filename = "sites.txt"  # file will save as 'sites.txt'

        if query != '' and pages != '':
            self.dork(query, pages, filename)

    def dork(self, query, pages, filename):
        print "[+] Googling for %s " % query
        urlList = []

        try:
            for url in search(query, stop=pages):
                urlList.append(url)
        except HTTPError:
            print "[HTTP Error 503] Service Unreachable"
            print "Try other dork, if an error still continue use VPN"
            exit(1)

        if len(urlList) != 0:
            print "Result: %i" % len(urlList)
            output = file(filename, "w")
            for url in urlList:
                output.write(url + "\n")
            output.close()
        else:
            print "No result found"
            sys.exit()
