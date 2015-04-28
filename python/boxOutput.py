#!/usr/bin/python
#Author - Jigar
#About -
#Prints a sentence in a centered "box" of correct width


#To read input from the user
sentence = raw_input("Sentence: ")

#Defining a variable
screen_width = 80
text_width = len(sentence)
box_width = text_width + 6
left_margin = (screen_width - box_width) // 2

print
print ' ' * left_margin + '+' + '-' * (box_width-2) + '+'
print ' ' * left_margin + '| ' + ' ' * text_width   + '   |'
print ' ' * left_margin + '| ' + sentence           + '   |'
print ' ' * left_margin + '| ' + ' ' * text_width   + '   |'
print ' ' * left_margin + '+' + '-' * (box_width-2) + '+'
print	
