#!/usr/bin/env python

# 30/11/2016
# Ghost (github.com/Hadesy2k)
# official.ghost@tuta.io
# GNU GPL <3.0>
# You can report me for bugs

from ext.geturls import GetUrls
from ext.useragents import getUserAgents
import os
import sys
import re
import urllib2
import random
from urlparse import urlparse
import time


vuln_urls = []
# You can add more SQL error message at line 166

def banner():
    print """SQL Injection Vulnerability Scanner by Ghost
www.github.com/Hadesy2k
official.ghost@tuta.io\n"""


def interruptHandler():
    os.system('clear')
    print "User interrupted the process."
    option = raw_input("Do you want to save scanned results [y/n] ")
    if option == 'y':
        print "Saving the scanned result into vulnerables.txt....."
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


class Main:
    def __init__(self, urls):
        self.user_agents = getUserAgents('./data/useragents.txt')
        self.urlReq(self.urlReader(urls))
        self.saveVulnerabilities()

    def urlReader(self, urls):
        """ split the url by newline """
        splittedUrls = urls.split('\n')
        if '' in splittedUrls:  # Removing empty line
            splittedUrls.pop(splittedUrls.index(''))
        return splittedUrls

    def urlReq(self, urls):
        for site in urls:
            parsed = urlparse(site)
            # These will check user URL whether it missed some necessary input.
            if len(parsed.scheme) == 0:
                pass
            elif len(parsed.path) == 0:
                pass
            elif len(parsed.query) == 0:
                pass

            # url variable is going use in upordown()
            # to check whether site is online or offline.
            url = parsed.scheme + "://" + parsed.netloc

            os.system('clear')
            print " Website Information"
            print " Domain Name : " + parsed.netloc
            print " Protocol    : " + parsed.scheme
            print " Path        : " + parsed.path
            print " Query[s]    : " + parsed.query + "\n"

            if (self.siteStatus(url)):  # True mean website is online
                self.scanVulnerability(site)

    def siteStatus(self, url):
        """ check website online or offline status """
        header = {'User-Agent': random.choice(self.user_agents)}
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
        # List the Items in Query of Provided URL with
        # it's id, using dict()

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

        except IndexError, ValueError:
            print "Query Not Found"
    
    def verifyVulnerability(self, url):
        global vuln_urls
        try:
            header = {'User-Agent': random.choice(self.user_agents)}
            request = urllib2.Request(url, None, header)
            http_request = urllib2.urlopen(request)
            sourcecode = http_request.read()

            # You can add more SQL error messages
            # changes need to be made in result{} too
            error_msg = {
                "mysql_error_1": "You have an error in your SQL syntax",
                "mysql_error_2": "supplied argument is not a valid MySQL result resource",
                "mysql_error_3": "check the manual that corresponds to your MySQL",
                "mysql_error_4": "mysql_fetch_array(): supplied argument is not a valid MySQL",
                "mysql_error_5": "function fetch_row()",
                "mssql_error_1": "Microsoft OLE DB Provider for ODBC Drivers error"
                }

            result = {
                "mysql_error1": re.search(error_msg["mysql_error_1"], sourcecode),
                "mysql_error2": re.search(error_msg["mysql_error_2"], sourcecode),
                "mysql_error3": re.search(error_msg["mysql_error_3"], sourcecode),
                "mysql_error4": re.search(error_msg["mysql_error_4"], sourcecode),
                "mysql_error5": re.search(error_msg["mysql_error_5"], sourcecode),
                "mssql_error1": re.search(error_msg["mssql_error_1"], sourcecode)
                }

            for resp in result.itervalues():
                try:
                    resp.group()
                    print "SQL error found."
                    time.sleep(1)
                    vuln_urls.append(url)
                except:
                    pass

        except urllib2.HTTPError, error:
            print 'Failed with error code - %s.' % error.code
    
    def saveVulnerabilities(self):
        # Remove Duplicate Vuln URLs
        vulns = list(set(vuln_urls))
        os.system('clear')
        if len(vulns) != 0:
            # Printing out vulnerable URLs.
            print "[!] Vulnerable URLs"
            vulnwrite = open("vulnerables.txt", 'w')
            for item in vulns:
                print item
                vulnwrite.write(item + "\n")
            vulnwrite.close()
            print "Vulnerables saved into vulnerables.txt."
        else:
            print "No Vulnerable URLs found."
        print "Process complete."


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        urls = GetUrls().dorkScanner()
    elif len(sys.argv) == 3 and sys.argv[1] == '-f':
        urls = GetUrls().fileReader(sys.argv[2])
    else:
        print "invalid option"
        exit()

    try:
        Main(urls)
    except KeyboardInterrupt:
        interruptHandler()