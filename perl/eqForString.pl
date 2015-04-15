#!/usr/bin/perl

print "What is your name? ";
$name = <STDIN>;
chomp($name);    #Get rid of the carriage return

if ($name eq "Jigar")
	{
	print "Howdy $name!\n";
	}
else
	{
	print "Hello $name!\n";
	}
