#!/usr/bin/python
# __author__ = 'Jigar'


# Example for return values

def allowed_dating_age(my_age):
    girls_age = my_age/2 + 7
    return girls_age

jigars_limit = allowed_dating_age(27)
creepy_limit = allowed_dating_age(35)
print("Jigar can date girls", jigars_limit, "or older")
print("Creepy can date girls", creepy_limit, "or older")
