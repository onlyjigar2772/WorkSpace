#!/usr/bin/python
# __author__ = 'Jigar'

# Example to show the variable scopr

a = 999
# If the variable is created outside and above function, it can access a


def corn():
    print(a)


def fudge():
    print(a)


corn()
fudge()