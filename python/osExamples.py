#!/usr/bin/python

import os
import subprocess

os.system("date")


f = os.popen('date')
now = f.read()

print "Today is", now


print "The os.system has many problems\
 and subprocess \nis a much better wat to execting Unix commands"

p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
print "Today is", output 

p = subprocess.Popen("ls", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
print "Files are", output 


p = subprocess.Popen(["ping", "-c", "10", "www.google.com"], stdout=subprocess.PIPE)

(output, err) = p.communicate()
print output 
