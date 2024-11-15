#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2024-11-15

@author: Dennis Krummacker
'''


'''
if num % 2 == 0:
    # Even 
else:
    # Odd

OR

if number & 2:# Bitwise AND Operator works also. Would be way faster in most languages. But since Python is a Script-language, wrapping all kinds of stuff around the logic...
    # Odd
    return
else:
    # Even 
    return 
'''
def isEven(number):
    if number % 2:
        # Odd
        return False
    else:
        # Even 
        return True

def isOdd(number):
    if number % 2:
        # Odd
        return True
    else:
        # Even 
        return False
