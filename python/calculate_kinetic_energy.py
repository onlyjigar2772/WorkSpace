#!/usr/bin/python

#Calculate kinetic Energy

print("This program calculates the kinetic energy of a moving object.")
m_string = input("Enter the object's mass in kilograms: ")
m = float(m_string)
v_sting = input("Enter the object's speed in meters per second: ")
v = float(v_sting)

e = 0.5 * m * v * v

print("The object has " + str(e) + " joules of energy.")
