#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-25

@author: Dennis Krummacker
'''

import os


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV

##Other Files for Project
from settings.path_and_file import ico_path, ico_fName
from settings.VersionInfo import VERSION_DESCRIPTION



class exePaths:
    def __init__(self):
        self.pathRel='..'
        self.pathTop=os.path.normpath(os.path.join(globV.progPath,self.pathRel))
        self.pathBuildDir=os.path.join(self.pathTop,'build')
        self.pathOutDir=os.path.join(self.pathTop,'out')
        self.srcDir='''src'''
        self.pathCodeDir=os.path.join(self.pathTop,self.srcDir)
        self.iconDir=os.path.join(self.pathCodeDir,ico_path,ico_fName)
        self.exeName='''DenKr_workoutScheduler'''
        self.exeNameRecent=f'''{self.exeName}_{VERSION_DESCRIPTION}'''