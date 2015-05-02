#!/usr/bin/python
# __author__ = 'Jigar'

# Examples of dictionary

classmates = {'Jigar': ' cool and handsome', 'Kim': ' knows about ipush', 'Wipro': ' my firm'}

print(classmates)
print(classmates['Kim'])

# Loop through

for k, v in classmates.items():
    print(k + v)
