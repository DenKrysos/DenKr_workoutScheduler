#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2020-11-18
Last Update: 2023-04-14

@author: Dennis Krummacker
'''


# Assuming we are working on insertionOrdered-Dictionaries (Python 3.6+)
def dict_get_nth_key(dictionary,nIdx=0):
    if nIdx<0:
        nIdx+=len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i==nIdx:
            return key
    raise IndexError("dictionary index out of range") 

def dict_get_first_key(dictionary):
    #first_key = list(dict)[0]
    #first_val = list(dict.values())[0]
    for key in dictionary:
        return key
    raise IndexError




def convert_tuple_to_list(trgt):
    if isinstance(trgt, dict):
        for k, v in trgt.items():
            trgt[k]=convert_tuple_to_list(v)
    if isinstance(trgt, list):
        return [convert_tuple_to_list(i) for i in trgt]
    if isinstance(trgt, tuple):
        return [convert_tuple_to_list(i) for i in trgt]
    else:
        return trgt