#!/usr/bin/env python

# 12/02/2017
# Ghost (github.com/Hadesy2k | www.hadesy2k.github.io)
# official.ghost@tuta.io
# GNU GPL <3.0>
# You can report me for bugs

from ext.useragents import getUserAgent
from ext.geturls import GetUrls
from ext.checksqli import checkSqli
from ext.filewriter import writeAsText
import os
import sys
import urllib2
from urlparse import urlparse
import time


vuln_urls = []

def showBanner():
    """ Show Banner Message """
    print """SQL Injection Vulnerability Scanner by Ghost
www.github.com/Hadesy2k
official.ghost@tuta.io

Last Update: [12/02/2017]"""


def showHelp():
    """ show commands and help message """
    print """-d to scan by giving google dork
-f <filename> to scan sites from given file
--about to see banner message """


def interruptHandler():
    os.system('clear')
    print "User interrupted the process."
    option = raw_input("Do you want to save scanned results [y/n] ")
    if option == 'y':
        # Opening the file and Saving the process.
        vulnerabilities = list(set(vuln_urls))
        iowriter = open("vulnerables.txt", 'w')

        for item in vulnerabilities:
            iowriter.write(item + "\n")
        iowriter.close()  # Closing the file
        print "Done"
    else:
        print "Scanned results will not be saved"
    exit()


class SqliScan:
    """ Main class of this script
        Includes:
          - website status checker
          - sql vulnerability scanner
          - io writer to save vulnerabilities """

    def __init__(self, urls):
        self.urlRequest(self.urlReader(urls))
        self.saveVulnerabilities()

    def urlReader(self, urls):
        """ read the url and removing newlines """
        splittedUrls = urls.split('\n')
        if '' in splittedUrls:  # Removing empty line
            splittedUrls.pop(splittedUrls.index(''))
        return splittedUrls

    def urlRequest(self, urls):
        """ check for website status, and if online scan for vulnerability """
        for site in urls:
            parsed = urlparse(site)
            url = parsed.scheme + "://" + parsed.netloc

            os.system('clear')
            print " Website Information"
            print " Domain Name : " + parsed.netloc
            print " Protocol    : " + parsed.scheme
            print " Path        : " + parsed.path
            print " Query[s]    : " + parsed.query + "\n"

            # These will check user URL whether it missed some necessary input.
            if len(parsed.scheme) == 0:
                print "Protocol not found"
                time.sleep(1); continue
            elif len(parsed.path) == 0:
                print "Path not found"
                time.sleep(1); continue
            elif len(parsed.query) == 0:
                print "Query not found"
                time.sleep(1); continue
            else:
                if self.siteStatus(url):  # True mean website is online
                    self.scanVulnerability(site)

    def siteStatus(self, url):
        """ check website online or offline status """
        header = {'User-Agent': getUserAgent()}
        request = urllib2.Request(url, None, header)

        print "Checking the website whether it's online or not."
        try:
            urllib2.urlopen(request)
            print "Connected, URL is valid."
            return True

        except urllib2.HTTPError, error:
            print error.code
            time.sleep(1)
            return False

        except urllib2.URLError, error:
            print error.reason
            time.sleep(1)
            return False

    def scanVulnerability(self, url):
        """ Scan the url by giving semi-colon on different id param """
        trigger_1 = "'"
        parsedUrl = urlparse(url)

        try:
            parms = dict([item.split("=") for item in parsedUrl[4].split("&")])
            parm_keys = parms.keys()

            if len(parms) == 1:
                vuln_test = parsedUrl.scheme + "://" + parsedUrl.netloc + parsedUrl.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1
                print "Testing: " + vuln_test
                self.verifyVulnerability(vuln_test)

            elif len(parms) == 2:
                vuln_test = parsedUrl.scheme + "://" + parsedUrl.netloc + parsedUrl.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "=" + parms[parm_keys[1]]
                print "Testing: " + vuln_test
                self.verifyVulnerability(vuln_test)

                vuln_test = parsedUrl.scheme + "://" + parsedUrl.netloc + parsedUrl.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1
                print "Testing: " + vuln_test
                self.verifyVulnerability(vuln_test)

            elif len(parms) == 3:
                vuln_test = parsedUrl.scheme + "://" + parsedUrl.netloc + parsedUrl.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" + parms[parm_keys[2]]
                print "Testing:" + vuln_test
                self.verifyVulnerability(vuln_test)

                vuln_test = parsedUrl.scheme + "://" + parsedUrl.netloc + parsedUrl.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1 + "&" + parm_keys[2] + "=" + parms[parm_keys[2]]
                print "Testing: " + vuln_test
                self.verifyVulnerability(vuln_test)

                vuln_test = parsedUrl.scheme + "://" + parsedUrl.netloc + parsedUrl.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" + parms[parm_keys[2]] + trigger_1
                print "Testing: " + vuln_test
                self.verifyVulnerability(vuln_test)

        except ValueError:
            print "Query Not Found"
        except IndexError:
            print "Query Not Found"
    
    def verifyVulnerability(self, url):
        """ verify website vulnerability and add to vulnerabilities list if found """
        global vuln_urls
        try:
            header = {'User-Agent': getUserAgent()}
            request = urllib2.Request(url, None, header)
            http_request = urllib2.urlopen(request)
            html = http_request.read()
            scannedResult = checkSqli(html)  # return dictionary

            for resp in scannedResult.itervalues():
                try:
                    resp.group()
                    print "SQL injection error found."
                    time.sleep(1)
                    vuln_urls.append(url)
                except:
                    pass

        except urllib2.HTTPError, error:
            print 'Failed with error code - %s.' % error.code
    
    def saveVulnerabilities(self):
        """ save the vulnerabilities to text file """
        urls = list(set(vuln_urls))
        os.system('clear')
        if len(urls) != 0:
            writeAsText('vulnerabilities.txt', urls)
        else:
            print "No Vulnerable URLs found."
        print "Process complete."


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        urls = GetUrls().dorkScanner()

    elif len(sys.argv) == 2 and sys.argv[1] == '--about':
        showBanner()
        exit()

    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        showHelp()
        exit()

    elif len(sys.argv) == 3 and sys.argv[1] == '-f':
        urls = GetUrls().fileReader(sys.argv[2])

    else:
        print "invalid option"
        exit()

    try:
        SqliScan(urls)
    except KeyboardInterrupt:
        interruptHandler()