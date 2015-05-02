#!/usr/bin/python
# __author__ = 'Jigar'

# Example for default values for arguments.


def get_gender(sex='Unknown'):
    if sex is 'm':
        sex = "Male"
    elif sex is 'f':
        sex = "Female"
    print(sex)

get_gender('m')
get_gender('f')
get_gender()

