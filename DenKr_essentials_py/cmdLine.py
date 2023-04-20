#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-14

@author: Dennis Krummacker
'''

import sys
#from sys import argv


#Return:
#  0 - No Arguments. Continue normal operation
#  1 - Cmd-Line Mux did all the work. Terminate
#  2 - Insufficient Number of Arguments
#  3 - Invalid Cmd-Line Arguments
#  4 - Reserved
class cmdLine_Mux(object):
    """The function \"def cmdLine_Mux(self)\" is to be defined by a child-class"""
    instance_counter=0
    #------------------------------------------------------------------------------------------
    def __init__(self):
        cmdLine_Mux.instance_counter+=1
        self._argv=sys.argv
        self._argc=len(self._argv)
        self._skip_ProgramCallPath()
        # "Traverse-Variables" for modifying while Traversal Argument List
        self.targc=self.argc
        self.curArg=0
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __del__(self):
        cmdLine_Mux.instance_counter-=1
    #------------------------------------------------------------------------------------------
    def _print_given_arguments(self):
        print('Number of arguments:',len(self._argv),'arguments.')
        print('Argument List:',str(self._argv))
    def _skip_ProgramCallPath(self):
        self.argv=sys.argv[1:]
        self.argc=len(self.argv)-1
    #------------------------------------------------------------------------------------------
    def cmdLine_Mux__oneLevelDeeper(self,LevelName):
        if 0<self.targc:
            self.targc-=1
            self.curArg+=1
            return 0
        else:
            print(f"-> Insufficient Cmd-Line Arguments after \"{LevelName}\".")
            return 2
    def cmdLine_Mux__errHandling(self):
        """A defined \"cmdLine_mux(self)\" shall return '3' on detecting an invalid Argument."""
        err=self.cmdLine_Mux()
        if 0==err:
            pass
        elif 1==err:
            print("\nDone.")
            print(sys.exit())
        elif 2==err or 3==err:
            print("\nExiting...")
            print(sys.exit())
        else:
            print(sys.exit())