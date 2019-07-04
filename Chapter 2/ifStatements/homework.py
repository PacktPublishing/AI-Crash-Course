# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 17:24:03 2019

@author: janwa
"""

a = 12                                          # we will check the divisibility of this number by 3

if a % 3 == 0:                                  # we check if a is divisible by 3
    print(str(a) + ' is divisible by 3')        # if it is we display that this number is divisible 
else:                                           # we enter this condtition, if the number is not divisible by 3
    print(str(a) + ' is not divisible by 3')    # then we display that indeed this number is not divisible by 3

# NOTE: str() function let's us display a variable followed by a text, it changes this integer number "a" to a text