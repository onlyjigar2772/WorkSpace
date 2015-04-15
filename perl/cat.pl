#!/usr/bin/perl

#program to print a file

open(MYFILE,$ARGV[0]) or die "cannot open file $ARGV[0]\n";

while($line = <MYFILE>) 
{
	print "$line";
}
