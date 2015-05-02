#!/usr/bin/python
# __author__ = 'Jigar'

# Example to showcase keyword Arguments.


def dumb_sentence(name='Jigar', action='ate', item='mangoes'):
    print(name, action, item)

dumb_sentence()
dumb_sentence("Shah", "farts", "gently")
dumb_sentence(item="Awesome")
dumb_sentence(item="Awesome", action="is")


