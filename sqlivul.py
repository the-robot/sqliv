# 10/06/2015
# Hades.y2k
# GPL <2.0>
# You can report me for bugs
# Credit to Xero who wrote pydorker.py (it's used as part of the function in my work)

import pydorker
import os, sys, re, urllib2, time, random
from urlparse import urlparse

# You Can Add Other If You Want To
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']

vuln_urls = [] # the list to collect vulnerable urls.
header = ""

# Colors
RED     = '\033[91m'
WHITE   = '\033[1m'
GREEN   = '\033[92m'
YELLOW  = '\033[93m'
END     = '\033[0m'

command = "clear" if 'nux' in sys.platform else "cls"

class banner():
    print RED + "\t\t________________________________________" + END
    print RED + "\t\t---- " + END + WHITE + "SQLi Vulnerable Scanner v2.0 " + END + RED +"------" + END
    print RED + "\t\t-------------------------- " + END + WHITE + "Hades.y2k " + END + RED +"---" + END
    print RED + "\t\t________________________________________" + END

class netorlocal():
    def __init__(self):
        self.askornot()

    def askornot(self):
        global readfile
        print YELLOW + "\n[!] " + END + WHITE + "You can scan vulnerables from local file or with Google Dorks."
        askusr = raw_input(YELLOW + "[!] " + END + WHITE + "From Local or Net [local/net]: ")
        if askusr == 'local':
            print WHITE + "\nThis is your files in current directory." + END
            os.system('pwd')
            os.system('ls')
            try:
                filename = raw_input(YELLOW + "[!] " + END + WHITE + "Please Enter file name: " + END)
                openfile = open(filename, 'r')
                readfile = openfile.read()
                openfile.close()
            except KeyboardInterrupt:
                print RED + "\n[!] " + END + WHITE + "Process Interrupted." + END
                print WHITE + "Exiting..." + END
                time.sleep(1)
                sys.exit()
            except:
                print RED + "\n[!] " + END + WHITE + "File does not exist." + END
                print WHITE + "Exiting..." + END
                time.sleep(1)
                sys.exit()
        elif askusr == 'net':
            pydorker.main()
            openfile = open("sites.txt", 'r')
            readfile = openfile.read()
            openfile.close()


class sqlscan():
    def __init__(self):
        self.readfile()
        self.urlreq(filels)
        self.printvuln()

    def errorprint(self):
        print RED + "\t\t------------------------------------" + END
        print RED + "\t\t--- " + END + WHITE + "An Error occured in process " + END + RED + "----" + END
        print RED + "\t\t------------------------------------" + END
        print WHITE + "\t\t            Exiting....\n\n" + END

    def readfile(self):
        filelist = [i for i in readfile.split('\n') if i != '']
        global filels
        filels = filelist
        os.system(command)

    def urlreq(self, thelist):
        for item in thelist:
            site = item
            parsed = urlparse(site)

            # These will check user URL whether it missed some necessary input.
            if len(parsed.scheme) == 0:
                time.sleep(1)
                pass
            elif len(parsed.path) == 0:
                time.sleep(1)
                pass
            elif len(parsed.query) == 0:
                time.sleep(1)
                pass

            global sqlsite
            sqlsite = site

            # url variable is going to use in upordown()
            # to check whether site is online or offline.
            url = parsed.scheme + "://" + parsed.netloc
            global target
            target = url

            print WHITE + "\t\t______________________________________" + END
            print YELLOW + "\t\t     [+] Website Information." + END
            print YELLOW + "\t\t Domain Name : "  + END + parsed.netloc
            print YELLOW + "\t\t Protocol    : "  + END + parsed.scheme
            print YELLOW + "\t\t Path        : "  + END + parsed.path
            print YELLOW + "\t\t Query[s]    : "  + END + parsed.query
            print WHITE + "\t\t______________________________________\n" + END
            time.sleep(1)
            self.upordown(target)
            self.scanurl(sqlsite)


    def upordown(self, url):
        header = {'User-Agent':random.choice(user_agents)}
        request = urllib2.Request(url, None, header)

        print YELLOW + "[+] " + END + WHITE + "Checking the Website whether it's up or down." + END
        try:
            http_request = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print RED + "[!] " + END + WHITE + "An Error Occured in Connection." + END
            print RED + "[!]" + END , e.code
            print RED + "[!] " + END + WHITE + "Exiting......\n\n" + END
            sys.exit()
        except urllib2.URLError, e:
            print RED + "[!] " + END + WHITE + "An Error Occured in Connection." + END
            print RED + "[!]" + END, e.reason
            print RED + "[!] " + END + WHITE + "Exiting......\n\n" + END
            sys.exit()
        else:
            print GREEN + "[+] " + END + WHITE + "Connected, URL is valid.\n" + END
    def verify(self,url):
        global vuln_urls
        try:
            header = {'User-Agent':random.choice(user_agents)}
            request = urllib2.Request(url, None, header)
            http_request = urllib2.urlopen(request)
            sourcecode = http_request.read()

            error_msg = {
                        "mysql_error_1":"You have an error in your SQL syntax",
                        "mysql_error_2":"supplied argument is not a valid MySQL result resource",
                        "mysql_error_3":"check the manual that corresponds to your MySQL"
                        "mysql_error_4":"mysql_fetch_array(): supplied argument is not a valid MySQL",
                        "mssql_error_1":"Microsoft OLE DB Provider for ODBC Drivers error"
                        }
            result = {
                        "mysql_error1":re.findall(error_msg["mysql_error_1"],sourcecode),
                        "mysql_error2":re.findall(error_msg["mysql_error_2"],sourcecode),
                        "mysql_error3":re.findall(error_msg["mysql_error_3"],sourcecode),
                        "mysql_error4":re.findall(error_msg["mysql_error_4"],sourcecode),
                        "mssql_error1":re.findall(error_msg["mssql_error_1"],sourcecode)
                     }

            for key, resp in result:
                if len(resp) != 0:
                    print GREEN + "[+] " + END + WHITE + "SQL error found." + END
                    vuln_urls.append(vuln_test)
        
        except urllib2.HTTPError, e:
            print 'We failed with error code - %s.' % e.code
            time.sleep(2)
            os.system(command)

    def scanurl(self, url):
        trigger_1 = "'"

        parsed_url = urlparse(url)
        # List the Items in Query of Provided URL with
        # it's id, using dict()
        parms = dict([item.split("=") for item in parsed_url[4].split("&")])
        parm_keys = parms.keys()

        #initx = 0
        if len(parms) == 1:
            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1
            print YELLOW + "[!] " + END + WHITE + "Testing: " + END + vuln_test
            self.verify(vuln_test)        

        elif len(parms) == 2: # If there're 2 quaries in the URL, this will work
            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "=" + parms[parm_keys[1]]
            print YELLOW + "[!] " + END + WHITE + "Testing: " + END + vuln_test
            self.verify(vuln_test)   

            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1
            print YELLOW + "\n[!] " + END + WHITE + "Testing: " + END + vuln_test
            self.verify(vuln_test)   

        elif len(parms) == 3: # If there're 3 quaries in the URL, this will work
            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + trigger_1 + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" + parms[parm_keys[2]]
            print YELLOW + "[!] " + END + WHITE + "Testing: " + END + vuln_test
            self.verify(vuln_test)

            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + trigger_1 + "&" + parm_keys[2] + "=" + parms[parm_keys[2]]
            print YELLOW + "\n[!] " + END + WHITE + "Testing: " + END + vuln_test
            self.verify(vuln_test)
            
            vuln_test = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parm_keys[0] + "=" + parms[parm_keys[0]] + "&" + parm_keys[1] + "=" + parms[parm_keys[1]] + "&" + parm_keys[2] + "=" + parms[parm_keys[2]] + trigger_1
            print YELLOW + "\n[!] " + END + WHITE + "Testing: " + END + vuln_test
            self.verify(vuln_test)

                     
    def printvuln(self):
        # Remove Duplicate Vuln URLs
        vulns = list(set(vuln_urls))     
        os.system(command)
        if len(vulns) != 0:
            # Printing out vulnerable URLs.
            print GREEN + "\n\t\t     [!] " + END + WHITE + "Vulnerable URLs.\n" + END
            vulnwrite = open("vulnerables.txt", 'w')
            for item in vulns:
                print item
                vulnwrite.write(item + "\n")
            vulnwrite.close()
            print GREEN + "\n[!] " + END + WHITE + "Vulnerables saved into vulnerables.txt." + END
        else:
            print RED + "\n[!] " + END + WHITE + "No Vulnerable URLs found.\n" + END
            
        print YELLOW + "[+] " + END + WHITE + "Process complete. Exiting.....\n\n" + END
        time.sleep(1)

if __name__ == "__main__":
    if 'linux' in sys.platform:
        # I used try, except to prevent interpreter from printing out
        # many error message when KeyboardInterrupt raised.
        try:
            banner()
            netorlocal()
            sqlscan()
        except KeyboardInterrupt:
            os.system(command)
            print RED + "[!] " + END + WHITE + "User interrupted the process." + END
            print RED + "[!] " + END + WHITE + "Process is about to terminated.\n" + END
            lastask = raw_input(WHITE + "Do you want to save current scanned results [y/n] " + END)
            if lastask == 'y':
                print WHITE + "Saving the scanned result into vulnerables.txt....." + END
                # Opening the file and Saving the process.
                vulns = list(set(vuln_urls))
                vulnwrite = open("vulnerables.txt", 'w')
                for item in vulns:
                    vulnwrite.write(item + "\n")
                vulnwrite.close() # Closing the file
                print WHITE + "Done" + END
                print WHITE + "Exiting.........\n" + END
                time.sleep(1)
                sys.exit()
            else:
                print WHITE + "Scanned results will not be saved" + END
                print WHITE + "Exiting...........\n"
                time.sleep(1)
                sys.exit()
    else:
        print "\nSorry, This script works only on Linux.\n"
