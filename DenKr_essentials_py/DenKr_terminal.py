#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2020-11-18
Last Update: 2023-04-16

@author: Dennis Krummacker
'''

import sys



#TODO    
def printf(string):
    sys.stdout.write(string)
    sys.stdout.flush()


class DKTerminal(object):
    def __init__(self):
        self.sout=sys.stdout
        self.sin=sys.stdin
        self.serr=sys.stderr
    #------------------------------------------------------------------------------------------
    def printStd(self, *objects, sep=' ', end='\n', flush=False):
        print(*objects,sep=sep,end=end,file=self.sout,flush=flush)
    def printErr(self, *objects, sep=' ', end='\n', flush=False):
        print(*objects,sep=sep,end=end,file=self.serr,flush=flush)
    #------------------------------------------------------------------------------------------
    def set_out(self,trgtStream):
        self.sout=trgtStream
    def switch_out(self,trgtStream):
        self.soutBkp=self.sout
        self.sout=trgtStream
    def restore_out(self):
        self.sout=self.soutBkp
        del self.soutBkp