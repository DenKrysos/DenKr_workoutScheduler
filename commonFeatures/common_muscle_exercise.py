#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-10

@author: Dennis Krummacker
'''

##DenKr Packages
from auxiliary.filesystem import file_json_write, file_json_read


class CommonMuscleExercise:
    @classmethod
    def history_read_file(cls,trgtArray,fName_prefix,fName,fName_ext):
        fName=fName_prefix+fName+fName_ext
        readData=file_json_read(fName)
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
        file_json_write(fName, jsonData)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def history_prepare_shortened(cls,target,toLoad):
        if len(target.history)<=toLoad:
            target.history_shortened=target.history[0:len(target.history)]
        else:
            target.history_shortened=target.history[len(target.history)-toLoad:len(target.history)]
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
                print("Malformed History for Muscle %s. Exiting..." % target.name)
                exit()
            if found_wo>=wo_toFind:
                break
            i-=1
        if i<0:
            i=0
        target.history_shortened=target.history[i:history_len]
    @classmethod
    def history_push_schedule(cls,target):
        target.history=target.history+target.schedule
        target.schedule=[]
#-----------------------------------------------------
    