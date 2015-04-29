#!/usr/bin/python
# __author__ = 'Jigar'

# Example for continue statement
myTeam = [2, 4, 9, 12]

print("Here are the numbers that are still available")

for n in range(1,20):
    if n in myTeam:
        continue
    print(n)