#!/usr/bin/bash
#Author - Jigar
#About - This script is used to check if the number of input args is not 0.
#It then creates a new file using touch command and gives the file exe per
#Also should how we can iterate through all input line arg

#Usage

if [ $# -eq 0 ]
then
	echo "No file name specified"
	exit
fi

for var in "$@"
do
	echo "Creating file $var and setting execute permission"
	touch $var
	chmod u+x $var
done
