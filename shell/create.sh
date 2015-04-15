#!/usr/bin/bash

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
