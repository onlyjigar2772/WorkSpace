#!/usr/bin/perl

my $startTime = time();

print "What is your name?";
$name = <STDIN>;
chomp($name);
print "Hello $name!\n";
printf "\nElapsed Time: %d seconds\n",time()-$startTime;
