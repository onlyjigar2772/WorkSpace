#!/usr/bin/bash

#To equate numbers use -eq, -ne, -gt, -ge, -lt, -le, !expr

a=4
b=10
c=10

if [ $a -eq $b ]
then
	echo "\$a and \$b are equal"
fi

if [ $b -eq $c ]
then 
	echo "They are equal"
fi
