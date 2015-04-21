#!/usr/bin/bash
#Author - Jigar
#About - The script should if..then..fi, if..then..else..fi and if..then..elif..then..else..fi

#To equate numbers use -eq, -ne, -gt, -ge, -lt, -le, !expr

a=4
b=10
c=10

#"This is a exampls of if then"
if [ $b -eq $c ]
then 
	echo "They are equal"
	echo "This is a exampls of if then"
fi

#"This is an example of if then else"
if [ $a -eq $b ]
then
	echo "\$a and \$b are equal"
else
	echo "They are not equal"
	echo "This is an example of if then else"
fi

#Multi if, elif statement

if [ "$1" = "cool" ]
then
	echo "Cool beans"
elif [ "$1" = "neat" ]
then
	echo "Neto cool"
else
	echo "No cool"
fi
