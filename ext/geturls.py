import pysearch

class GetUrls(object):
    """ This class ask your to choose two option
        First option, scan the websites given from text file
        Second option, scan random vulnerable website by giving Google dork
    """
    @staticmethod
    def fileReader(filename):
        """ read url from given file and return as list """
        try:
            openfile = open(filename, 'r')
            urls = openfile.read()
            openfile.close()
            return urls
        except IOError:
            print "File does not exist."
            exit()

    @staticmethod
    def dorkScanner():
        """ look for websites from Google by using dork """
        pysearch.PySearch()
        openfile = open("sites.txt", 'r')
        urls = openfile.read()
        openfile.close()
        return urls