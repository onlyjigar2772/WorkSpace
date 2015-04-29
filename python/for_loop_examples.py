#!/usr/bin/python

# Print 'Hi' 10 times

for i in range(10):
    print("Hi")

for i in range(5):
    print("Hello")
    print("There")

for i in range(10):
    print(i+1)

for i in range(10, 0, -1):
    print(i)

for i in range(3):
    print("a")
    for j in range(3):
        print("b")

# What is the value of a
a = 0
for i in range(10):
    a += 1
print(a)

# What is the value of a?
a = 0
for i in range(10):
    a += 1
for j in range(10):
    a += 1
print(a)

# What is the value of a?
a = 0
for i in range(10):
    a += 1
    for j in range(10):
        a += 1
print(a)

