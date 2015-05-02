#!/usr/bin/python
# __author__ = 'Jigar'

# Example to show how to unpack argument.


def health_calculator(age, apples_ate, cigs_smoked):
    answer = (100 - age) + (apples_ate * 3.5) - (cigs_smoked * 2)
    print(answer)

jigar_data = [27, 20, 0]


health_calculator(jigar_data[0], jigar_data[1], jigar_data[2])
health_calculator(*jigar_data)
# The above example is unpacking a list