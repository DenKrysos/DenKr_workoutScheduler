#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-07-23

@author: Dennis Krummacker
'''



def distribute_capacity(capacity, num_entries, fraction_size=None):
    """
    It is a Generator Function (that operates recursively).
    It generates every possible Permutation for Distributing a given 'Capacity' in Chunks of 'fraction_size' over a list of length 'num_entries'.
    With each iteration over the Generator you will get the next Permutation.
    So this is gentle on memory consumption as it does not generate all permutations at once, but only ever returns the next.
    - If no 'fraction_size' is passed, this is internally set to evenly split the 'capacity' in 'num_entries' pieces.
      - In many use-cases, this might make the most sense, because with every fraction-size that has no multiple to equal capacity, always an unused headroom is left
    - But nonetheless, any 'fraction_size' can be freely passed explicitly
    Usage-Example:
        capacity=1
        num_entries=4
        permutations_generator = distribute_capacity(capacity, num_entries, fraction_size)
        for permutation in permutations_generator:
            print(permutation)
        print("\nEnd")
    """
    if fraction_size is None:
        fraction_size=capacity/num_entries
    #Have to normalize step_size and capacity for the loop.
    loop_lim=int(capacity/fraction_size)
    if 0>=num_entries:
        yield []
    else:
        for i in range(loop_lim,-1,-1):
            sublist=distribute_capacity(capacity-i*fraction_size,num_entries-1,fraction_size)
            for permutation in sublist:
                yield [i*fraction_size]+permutation
