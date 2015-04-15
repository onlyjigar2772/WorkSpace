#!/usr/bin/perl

open(OUTFILE, ">test.dat") or die 'Cannot open file test.dat';
for($i=0; $i < 10; $i++)
{
	print OUTFILE " line $i\n"
}
close(OUTFILE);

print "Finished writing to \"test.dat\"";
