#!/usr/bin/env python

# 09/07/2016
# Hades.y2k (github.com/Hadesy2k)
# official.hadesy2k@protonmail.com
# GPL <3.0>
# You can report me for bugs

import pydorker
import os
import sys
import re
import urllib2
import random
from urlparse import urlparse
import time


# You Can Add Other If You Want To
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
    ]

header = ""
vuln_urls = []


class netorlocal():
    def __init__(self):
        global readfile
        print "[!] You can scan vulnerables from local or Google Dorks."
        askusr = raw_input("[!] From Local or Net [local/net]: ")

        if askusr == 'local':
            print
            os.system('pwd')
            print "This is your files in current directory."
            os.system('ls')

            try:
                filename = raw_input("[!] Please Enter file name: ")
                openfile = open(filename, 'r')
                readfile = openfile.read()
                openfile.close()

            except KeyboardInterrupt:
                print "\n\n[!] Process Interrupted."
                sys.exit()

            except:
                print "\n[!] File does not exist."
                sys.exit()

        elif askusr == 'net':
            pydorker.main()
            openfile = open("sites.txt", 'r')
            readfile = openfile.read()
            print readfile
            openfile.close()


class sqlscan():
    def __init__(self):
        self.urlreq(self.readfile())
        self.printvuln()

    def readfile(self):
        filelist = readfile.split('\n')
        # Removing empty line
        if '' in filelist:
            filelist.pop(filelist.index(''))
        os.system('clear')
        return filelist

    def urlreq(self, urlList):
        for site in urlList:
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

            self.upordown(url)
            self.scanurl(site)

    def printvuln(self):
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
            print "\nVulnerables saved into vulnerables.txt."
        else:
            print "\nNo Vulnerable URLs found."

        print "[+] Process complete."

    def upordown(self, url):
        header = {'User-Agent': random.choice(user_agents)}
        request = urllib2.Request(url, None, header)

        print "Checking the Website whether it's up or down."
        try:
            urllib2.urlopen(request)
            print "[+] Connected, URL is valid.\n"

        except urllib2.HTTPError, e:
            print e.code
            sys.exit()

        except urllib2.URLError, e:
            print e.reason
            sys.exit()

    def verify(self, url):
        global vuln_urls
        try:
            header = {'User-Agent': random.choice(user_agents)}
            request = urllib2.Request(url, None, header)
            http_request = urllib2.urlopen(request)
            sourcecode = http_request.read()

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

            for key, resp in result.iteritems():
                try:
                    resp.group()
                    print "[+] SQL error found."
                    time.sleep(2)
                    vuln_urls.append(url)
                except:
                    pass

        except urllib2.HTTPError, e:
            print 'We failed with error code - %s.' % e.code

    def scanurl(self, url):
        trigger_1 = "'"

        parsed_url = urlparse(url)
        # List the Items in Query of Provided URL with
        # it's id, using dict()
        parms = dict([item.split("=") for item in parsed_url[4].split("&")])
        parm_keys = parms.keys()

        # initx = 0
        if len(parms) == 1:
            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1
            print "[!] Testing: " + vuln_test
            self.verify(vuln_test)

        elif len(parms) == 2:
            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "=" + parms[parm_keys[1]]
            print "[!] Testing: " + vuln_test
            self.verify(vuln_test)

            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1
            print "[!] Testing: " + vuln_test
            self.verify(vuln_test)

        elif len(parms) == 3:

            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc +\
                parsed_url.path + "?" + parm_keys[0] + "=" +\
                parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "="\
                + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" +\
                parms[parm_keys[2]]

            print "[!] Testing:" + vuln_test
            self.verify(vuln_test)

            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1 + "&" + parm_keys[2] + "=" + parms[parm_keys[2]]
            print "[!] Testing: " + vuln_test
            self.verify(vuln_test)

            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" + parms[parm_keys[2]] + trigger_1
            print "[!] Testing: " + vuln_test
            self.verify(vuln_test)


if __name__ == "__main__":
    # I used try, except to prevent interpreter from printing out
    # many error message when KeyboardInterrupt raised.
    try:
        netorlocal()
        sqlscan()

    except KeyboardInterrupt:
        os.system('clear')
        print "[!] User interrupted the process."

        lastask = raw_input("Do you want to save scanned results [y/n] ")
        if lastask == 'y':
            print "Saving the scanned result into vulnerables.txt....."
            # Opening the file and Saving the process.
            vulns = list(set(vuln_urls))
            vulnwrite = open("vulnerables.txt", 'w')

            for item in vulns:
                vulnwrite.write(item + "\n")
            vulnwrite.close()  # Closing the file
            print "Done"
            sys.exit()

        else:
            print "Scanned results will not be saved"
            sys.exit()
