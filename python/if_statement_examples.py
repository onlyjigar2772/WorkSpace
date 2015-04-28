#!/usr/bin/python

# Variables used in the example if statements

a = 4
b = 5
c = 6

# Basic comparisons

if a < b:
    print("a is less than b")

if a > b:
    print("a is greater than b")

if a <= b:
    print("a is less than or equal to b")

if a >= b:
    print("a is greater than or equal to b")

# Use == if you are asking if they are equal
# Use = if you are assigning.
if a == b:
    print("a is equal to b")

# Not equal
if a != b:
    print("a and b are not equal")

# And
if a < b and a < c:
    print("a is less than b and c")

# Non-exclusive or
if a < b or a < c:
    print("a is less than either a or b or both")

# Bollean data type. This is legal!
a = True
if a:
    print("a is true")

if not a:
    print("a is false")

a = True
b = False

if a and b:
    print("a and b both are true")

a = 3
b = 3
c = a == b
print(c)

if 1:
    print("1")

if "A":
    print("A")

if 0:
    print("Zero")

a = "c"

if a == "B" or a == "b":
    print("a is equal to b")

# Example 1: If statement
temperature = int(input("What is the temperate in far? "))
if temperature > 90:
    print("It is hot outside")
print("Done")

# Example 2: Else statement
temperature = int(input("What is the temperatein far? "))
if temperature > 90:
    print("It is hot outside")
else:
    print("It is not hot outside")
print("Done")

# Example 3: Else if statement
temperature = int(input("What is the temperate in far? "))
if temperature > 90:
    print("It is hot outside")
elif temperature < 30:
    print("It is too cold outside")
else:
    print("It is not hot outside")
print("Done")

# Compare string
userName = raw_input("What is your name? ")

if userName == "Jigar":
    print("You have a nice name")
else:
    print("Your name is ok")



