#!/usr/bin/python
# __author__ = 'Jigar'

# Example to show how to have flexible input arguments for function
# It is a norm among programmers to name flexible input
# as args. We can name it to actually anything


def add_numbers(*args):
    total = 0
    for a in args:
        total += a
    print(total)

add_numbers(3)
add_numbers(3, 32)
add_numbers(3, 232, 342, 23451451)
