#!/usr/bin/python
# __author__ = 'Jigar'


# Using urllib2

import urllib2


response = urllib2.urlopen('http://python.org/')

html = response.read()

# Example 2


req = urllib2.Request('http://www.voidspace.org.uk')
response = urllib2.urlopen(req)
the_page = response.read()

print the_page


