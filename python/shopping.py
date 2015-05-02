#!/usr/bin/python
# __author__ = 'Jigar'

# Set are a collection of items but cannot have any duplicates

groceries = {'cereal', 'milk', 'biscuit', 'ductile', 'lotion', 'biscuit'}
print(groceries)

if 'milk' in groceries:
    print("You already have milk boss!")
else:
    print("Oh yeah you need milk")