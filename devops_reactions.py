#!/usr/bin/env python
import sys
sys.path.insert(0, 'lib')

import urllib2
import telegram
from BeautifulSoup import BeautifulSoup


class DevOpsReactions(object):
    URL = 'http://devopsreactions.tumblr.com/%s'
    STATIC_DIR = 'static'

    @classmethod
    def _getRSS(cls):
        url = cls.URL % 'rss'
        data = urllib2.urlopen(url).read()
        soup = BeautifulSoup(data)

        return [i.find('guid').text for i in soup.findAll('item')]

    @classmethod
    def _getPost(cls, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

        try:
            title = soup.find('div', attrs={'class': 'post_title'}).text.encode('utf-8')
            image_url = soup.find('div', attrs={'class': 'item text'}).p.img['src']
        except TypeError:
            image_url = soup.find('div', attrs={'class': 'item text'}).img['src']

        return {'title': title, 'image_url': image_url}

    @classmethod
    def latest(cls):
        urls = cls._getRSS()
        html = urllib2.urlopen(urls[0]).read()
        post = cls._getPost(html)

        return post

    @classmethod
    def random(cls):
        url = DevOpsReactions.URL % 'random'
        html = urllib2.urlopen(url).read()
        post = cls._getPost(html)

        return post
