#!/usr/bin/python
import os
import sys

#ls | wc -l --> Gives me number of files in a dir
print "Number of files: ", len([f for f in os.listdir('.')])
#ls | grep -i ".py" | wc -l
print "Number of files with .py extension: ", len([f for f in  os.listdir('.') if f.endswith(".py")])
print "Number of files with .pl extension: ", len([f for f in  os.listdir('.') if f.endswith(".pl")])
print "Number of files with .sh extension: ", len([f for f in  os.listdir('.') if f.endswith(".sh")])
print "Number of files with .txt extension: ", len([f for f in  os.listdir('.') if f.endswith(".txt")])
