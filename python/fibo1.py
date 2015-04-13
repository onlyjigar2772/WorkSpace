#!/usr/bin/python

fibs = [0,1]
'''
for i in range(8):
    fibs.append(fibs[-2] + fibs[-1])
'''

num = input('How many Fibonacci numbers do you want? ')
for i in range(num-2):
    fibs.append(fibs[-2] + fibs[-1])
print fibs