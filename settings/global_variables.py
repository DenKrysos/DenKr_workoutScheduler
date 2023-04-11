#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18

@author: Dennis Krummacker
'''


import os

progPath=None


'''
Usage:
- import the whole module (not single elements). Afterwards access it everything as global_variables.x
from settings import global_variables
- Call this function giving it the main file's __file__ as argument, preferably just inside the main-file:
global_variables.set_ProgramPath(__file__)
'''
def set_ProgramPath(mainFile__file__):
    global progPath
    #print('sys.argv[0] =', sys.argv[0])
    #progPath = os.path.dirname(sys.argv[0])
    #print('path =', progPath)
    #print('full path =', os.path.abspath(progPath))
    #progPath = os.path.realpath(__file__)
    #print('realpath = ', progPath)
    #progPath = os.path.dirname(progPath)
    #print('realpath = ', progPath)
    progPath=os.path.realpath(mainFile__file__)
    progPath=os.path.dirname(progPath)
    #print('Path of Script: ', progPath)