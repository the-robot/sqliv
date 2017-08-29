#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#

"""
Author : Black Viking
Version: 0.0.1

https://gist.github.com/blackvkng/7487098fba261ac05f62c4676d33f350
"""

__name__ = 'python-bing'

import re
import urllib
import urllib2

class Bing:
    def __init__(self):
        self.bingsearch = "http://www.bing.com/search?%s"
        self.regex = re.compile('<h2><a href="(.*?)"')

    def default_headers(self, name = __name__):
        '''
        :type name : str
        :param name: Name to add user-agent 

        :rtype: dict
        '''

        return {
            'Accept'         : 'text/html',
            'Connection'     : 'close',
            'User-Agent'     : '%s/%s' % (name, __version__),
            'Accept-Encoding': 'identity'
            }

    def get_page(self, URL):
        '''
        :type URL : str
        :param URL: URL to get HTML source 

        :rtpye: str
        '''

        request = urllib2.Request(URL, headers=self.default_headers())
        resp    = urllib2.urlopen(request)

        return resp.read()

    def parse_links(self, html):
        '''
        :type html : str
        :param html: HTML source to find links

        :rtype: list
        '''

        return re.findall(self.regex, html)

    def search(self, query, stop=100):
        '''
        :type query : str
        :param query: Query for search
        
        :type stop  : int
        :param stop : Last result to retrieve.

        :rtype: list
        '''
 
        links = []
        start = 1

        for page in range(int(round(int(stop), -1)) / 10):
            URL = (self.bingsearch % (urllib.urlencode({'q': query}))) + '&first=' + str(start)

            html   = self.get_page(URL)
            result = self.parse_links(html)

            [links.append(_) for _ in result if _ not in links]

            start = start + 10

        return links
