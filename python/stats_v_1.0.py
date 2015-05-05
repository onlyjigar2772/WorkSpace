#!/usr/bin/python
import os
import sys

#ls | wc -l --> Gives me number of files in a dir
print "Number of files: ", len([f for f in os.listdir('.')])
#ls | grep -i ".py" | wc -l
print "Number of files with .txt extension: ", len([f for f in  os.listdir('.') if f.endswith(".txt")])
print "Number of files with .log extension: ", len([f for f in  os.listdir('.') if f.endswith(".log")])


print "Now providing detailed information"
for file in os.listdir('.'):
    if not file.startswith('.'):
        loc = 0
        pout = os.popen("pylint %s | grep 'Raw metrics' -A 14"% file, 'r')
        for line in pout:
            word = []
            if "code" in line:
                words = line.split("|")
                loc = int(words[2])
        print "The LoC for %s is %d"%(file, loc)
#print "Total Lines of code is", (pyCount +=pyCountFile)




'''
1)
http://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir-python

2)
Doing pylint $@ | grep 'Raw metrics' -A 14 will show only a table of the different line counts (where $@ is the names of the Python files you're counting).
http://stackoverflow.com/questions/9076672/how-to-count-lines-of-code-in-python-the-right-way

3)
http://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string
if word in mystring: 
   print 'success'

4) 
http://www.pythonforbeginners.com/basics/string-manipulation-in-python
http://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
tim.split(':')

5)
No config file found, using default configuration
http://stackoverflow.com/questions/5253559/trying-to-run-pylint-with-jenkins-getting-error-no-config-file-found-using-de

I had the same issue today and this worked perfectly. Just do a "touch ~/.pylintrc" and the error message goes away. Thanks!

'''
