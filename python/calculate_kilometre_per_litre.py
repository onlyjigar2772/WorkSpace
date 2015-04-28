#!/usr/bin/python
#Author - Jigar
#About -
#Calculate Kilometre per litre

print ("This program calculates kmpl.")

#Get kilometre driven from the user
kilometre_driven = input("Enter kilometre driven: ")

#convert text entered to a 
#floating point number
kilometre_driven = float(kilometre_driven)

#Get litre used from the user
litre_used = input("Enter litre used: ")

#convert text entered to a 
#floating point number
litre_used = float(litre_used)

#Calculate and print the answer

kmpl = kilometre_driven / litre_used
print("Kilometre per litre: ", kmpl)
