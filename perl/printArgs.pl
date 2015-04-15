#!/usr/bin/perl

#To print all arguments passed

$numOfArgs = @ARGV;

print "The number of arguments passed was $numOfArgs \n";

for ($i=0; $i < $numOfArgs; $i++)
{
	print "argv[$i] = $ARGV[$i]\n"
}


