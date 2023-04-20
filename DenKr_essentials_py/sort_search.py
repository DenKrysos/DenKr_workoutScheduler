#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 2023-04-11

@author: Dennis Krummacker
'''

import bisect


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



def search_sorted_list(sorted_list, searchVal, key):
    """Return -1 when searchVal is not in list, otherwise index of position. Pass a lambda as key as common. Assumes a sorted-list"""
    index=bisect.bisect_left(sorted_list, searchVal, key=key)
    if index!=len(sorted_list) and key(sorted_list[index])==searchVal:
        return index
    else:
        return -1