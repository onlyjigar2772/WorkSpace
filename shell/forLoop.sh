#!/usr/bin/bash
#Author - Jigar
#About - This script shows syntax for for loop
#$@ represents all the arguments:
#variable is defined like this below
for var in "$@"
do 
	echo "$var"
done
