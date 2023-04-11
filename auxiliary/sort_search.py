#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 2023-04-11

@author: Dennis Krummacker
'''


def binary_search(number, lst):
    left=0
    right=len(lst)-1
    while left<=right:
        mid=(left+right)//2
        if lst[mid]==number:
            return True
        elif lst[mid]<number:
            left=mid+1
        else:
            right=mid-1
    return False