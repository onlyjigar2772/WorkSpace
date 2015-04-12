#!/usr/bin/python

#Check user name and PIN code

database = [
    ['name1', '1234'],
	['name2', '4242'],
	['name3', '7543'],
	['name4', '3333']
]

username = raw_input('User Name: ')
pin = raw_input('PIN Code: ')

if [username, pin] in database: print 'Access granted'


	