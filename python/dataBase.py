#!/usr/bin/python

# A simple data base

people = {

    'Alice': {
	    'phone': '2341',
		'addr': 'Foo drive 23'
	},
	
	'Beth': {
	    'phone': '9102',
		'addr': 'Bar street 42'
	},
	
	'Jigar': {
	    'phone': '9945',
		'addr': 'Rag res'
	}
	
}

#Describe label.

labels = {
    'phone': 'phone number',
	'addr': 'address'
}

name = raw_input('Name: ')

request = raw_input('Phone number (p) or address (a)?')

#Use the correct key:

if request == 'p': key = 'phone'
if request == 'a': key = 'addr'

if name in people: print "%s's %s is %s." % \
    (name, labels[key], people[name][key])
