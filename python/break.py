#!/usr/bin/python
# __author__ = 'Jigar'

# Example for break and continue statement

magicNumber = 26

for n in range(101):
    if n is magicNumber:
        print(n, "is the magicNumber!")
        break
    else:
        print(n)

