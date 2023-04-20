#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2020-11-18

@author: Dennis Krummacker
'''

## System Packages
import sys  # @UnusedImport



if sys.version_info < (3,):#Compatibility, because xrange has changed to range from Python 2.x to 3
    range= xrange  # @UndefinedVariable @ReservedAssignment


try:
    input=raw_input  # @UndefinedVariable @ReservedAssignment
except NameError:
    pass
##Or Alternative:
# try:
#     import __builtin__
#     input = getattr(__builtin__, 'raw_input')
# except (ImportError, AttributeError):
#     pass