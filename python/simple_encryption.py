#!/usr/bin/python

plain_text = "This is a test. ABD"
encrypted_text = ""

for c in plain_text:
    x = ord(c)
    x = x + 1
    c2 = chr(x)
    encrypted_text+=c2
print (encrypted_text)
