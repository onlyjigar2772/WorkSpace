#!/usr/bin/sh
#Author - Jigar
#About - To validate string we use == operator.
valid_PASSWORD="secret"
echo "Please enter the password: "
read PASSWORD

if [ "$PASSWORD" == "$valid_PASSWORD" ]; then
	echo "You have access!"
else
	echo "You dont have access!"
fi
	
