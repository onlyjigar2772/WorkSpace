#!/usr/bin/ruby

# I'm a comment
a = 1 # We do not need semi colon at the EoL

b = 2; c = 3 

name = "ABD \
RCB" # a line contunued by trailing \

puts "#{name}"

=begin
This is a multi line comment
and everything printed 
until end is ignored
=end

puts "goodbye"
#Lines followed by "__END__" on its own line with 
no white space, are ignored
__END__
1
1
2
3
puts "Bye again"