#!/usr/bin/ruby

def welcome(name)
    puts "Howdy #{name}"    #inside double quotes, #{} will evaluate the variable
end

welcome "Visitor"


def multiply(a,b)
    product = a * b
    return product
end

puts multiply(2,3)

#You can leave out return statement and ruby will helpfully 
#return the last expression
def mult(a,b)
    product = a*b
end
puts mult(2,5)

#Optional argument values
def test(a=1,b=2,c=a+b)
    puts "#{a},#{b},#{c}"
end

test
test 5
test 5, 6
test 5, 6, 7