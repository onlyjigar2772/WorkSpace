#!/usr/bin/python
# __author__ = 'Jigar'


# How to read and write files.

fw = open('sample.txt', 'w')
fw.write('Writing some stuff in my text files\n')
fw.write('I want to become a good programmer\n')

fw.close()


# How to read a file

fr = open('sample.txt', 'r')
text = fr.read()
print(text)
fr.close()

