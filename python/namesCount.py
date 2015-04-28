#!/usr/bin/python

import sys

if __name__ == "__main__":
    names = {}
    # sys.stdin is a file object.
    for name in sys.stdin.readlines():
        name = name.strip()
        if name in names:
            names[name] += 1
        else:
            names[name] = 1

# printing the new dic
for name, count in names.iteritems():
    sys.stdout.write("%d\t%s\n" % (count, name))

