#!/usr/bin/python

encrytped_text = "Uijt!jt!b!uftu/!BCD!bcd"

plain_text = ""

for c in encrytped_text:
    x = ord(c)
    x = x - 1
    c2 = chr(x)
    plain_text += c2

print(plain_text)

