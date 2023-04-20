#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-10

@author: Dennis Krummacker
'''


## System Packages
from builtins import object


## Some Fundamentals
import DenKr_essentials_py.importMe_fundamental  # @UnusedImport


##Fundamental Project Settings
from settings.path_and_file import (
    history_file_subpath
)


##DenKr Packages
from auxiliary.filesystem import file_json_write, file_json_read, file_backup_asMove, file_json_read_singleArray


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV


class CommonMuscleExercise(object):
    servingThreshold=0.45#Only when the intensity for which an exercise serves a muscle is at least (>=) this, the exercise can be explicitly picked to serve the muscle. (See also comment on "self.muscleIntensity")
    minimumServing=0.7#A muscle has to be trained with at least this intensity (increase as long as <=minimumServing). If picked exercises serve a muscle that is scheduled for a workout less than this, additional exercises (with intensity <1) are included.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def history_read_file_single(self,fName_prefix,fName_ext):
        '''The "_single" versions are not in use. Instead one common file is stored which contains all muscles at once'''
        fName=fName_prefix+self.name+fName_ext
        self.history=file_json_read_singleArray(fName)
    def history_write_file_single(self,fName_prefix,fName_ext):
        '''The "_single" versions are not in use. Instead one common file is stored which contains all muscles at once'''
        fName=fName_prefix+self.name+fName_ext
        file_json_write(fName, self.history)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def history_read_file(cls,trgtArray,fName_prefix,fName,fName_ext):
        fName=fName_prefix+fName+fName_ext
        readData=file_json_read(history_file_subpath,fName)
        for i in range(len(trgtArray)):
            if trgtArray[i].name in readData:
                trgtArray[i].history=readData[trgtArray[i].name]
            else:
                trgtArray[i].history=[]
    @classmethod
    def history_write_file(cls,trgtArray,fName_prefix,fName,fName_ext):
        fName=fName_prefix+fName+fName_ext
        jsonData={}
        for i in range(len(trgtArray)):
            jsonData[trgtArray[i].name]=trgtArray[i].history
        file_json_write(history_file_subpath,fName, jsonData)
    @classmethod
    def history_trim_file(cls,trgtArray,fName_prefix,fName,fName_ext):
        for x in trgtArray:
            x.history=x.history_shortened[:]
        file_backup_asMove(history_file_subpath,fName_prefix+fName,fName_ext)
        cls.history_write_file(trgtArray,fName_prefix,fName,fName_ext)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def history_prepare_shortened(self,shortenedHistoryLen):
        if len(self.history)<=shortenedHistoryLen:
            self.history_shortened=self.history[0:len(self.history)]
        else:
            self.history_shortened=self.history[len(self.history)-shortenedHistoryLen:len(self.history)]
    @classmethod
    def history_prepare_shortened_exerciseOriented(cls,target):
        #prepare a shortened history over 2 weeks
        found_wo=0
        wo_toFind=target.wo_pW*2#4
        history_len=len(target.history)
        i=history_len-1
        while i>=0:
            if target.history[i]==1:
                found_wo+=1
            elif target.history[i]==0:
                pass
            else:
                globV.HCI.printErr("Malformed History for Muscle %s. Exiting..." % target.name)
                exit()
            if found_wo>=wo_toFind:
                break
            i-=1
        if i<0:
            i=0
        target.history_shortened=target.history[i:history_len]
    #------------------------------------------------------------------------------------------
    def history_push_schedule(self):
        self.history=self.history+self.schedule
        self.schedule=[]
    @classmethod
    def history_push_schedule_all(cls,trgtList):
        [i.history_push_schedule() for i in trgtList]
#-----------------------------------------------------
    