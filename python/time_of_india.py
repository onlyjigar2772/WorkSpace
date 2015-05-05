#!/usr/bin/python
# __author__ = 'Jigar'


# Attempt to get all the links from times of india web site


import urllib2
from bs4 import BeautifulSoup

def trade_spider():
    url = 'http://timesofindia.indiatimes.com/'
    conn = urllib2.urlopen(url)
    source_code = conn.read()
    print(source_code)

    soup = BeautifulSoup(source_code)
    links = soup.find_all('a')

    fx = open('toi.txt', 'w')
    for tag in links:
        link = tag.get('href', None)
        if link != None:
            fx.write(link + "\n")
    fx.close()




trade_spider()