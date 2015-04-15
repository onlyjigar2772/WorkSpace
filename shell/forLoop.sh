#!/usr/bin/bash

#$@ represents all the arguments:
#variable is defined like this below
for var in "$@"
do 
	echo "$var"
done
