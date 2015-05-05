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


print "Now providing detailed information\n"
pyCount = 0
for file in os.listdir('.'):
    if not file.startswith('.'):
        pyCountFile = 0
        FH = open(file, 'r')
        for line in FH:
            if (line.startswith('#') or line =='\n' or line =='^M$'):
               continue 
            pyCountFile += 1
        print "The LoC for %s is %d"%(file, pyCountFile)
#print "Total Lines of code is", (pyCount +=pyCountFile)




'''
1)
http://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir-python

2)
Doing pylint $@ | grep 'Raw metrics' -A 14 will show only a table of the different line counts (where $@ is the names of the Python files you're counting).
http://stackoverflow.com/questions/9076672/how-to-count-lines-of-code-in-python-the-right-way
'''
