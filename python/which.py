#!/usr/bin/python

from __future__ import print_function

import sys
import os
import os.path
import stat

def usage():
    sys.stderr.write("Usage: python which.py name\n")
    sys.stderr.write("or which.py name\n")

def which(name):
    found = 0
    for path in os.getenv("PATH").split(os.path.pathsep):
	    full_path = path + os.sep + name
	    if os.path.exists(full_path):
		    found = 1
		    print(full_path)
    sys.exit(1 - found)
	
def main():
    if len(sys.argv) != 2:
	    usage()
	    sys.exit(1)
    which(sys.argv[1])
	
if "__main__" == __name__:
	    main()