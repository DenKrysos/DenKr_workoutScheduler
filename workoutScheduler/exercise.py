#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-09

@author: Dennis Krummacker
'''

import sys
import copy


## Some Fundamentals
import DenKr_essentials_py.importMe_fundamental  # @UnusedImport


## System Packages
# import math
# from builtins import object



##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV


##Workout-Scheduler Packages
from commonFeatures.common_muscle_exercise import CommonMuscleExercise
from workoutScheduler.muscle import muscle
from settings.values import SetupExeIdx


##Fundamental Project Settings
from settings.path_and_file import (
    history_file_fExt,
    history_file_prefix_exercise,
    history_file_fname_exercise
)

##Individual Configuration
import settings.config_handler as cfghandle
# Instead: Also using a read handle within cfghandle
#from _1cfg.setup import exercise_setup



#-----------------------------------------------------
#Leave the default function just alone. It essentially only serves as a template.
# -> If you want to change muscle's values, Look into ./_1cfg/setup.py
exercise_setup_default=[
]
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
class exercise(CommonMuscleExercise):
    instance_counter=0
    #primaryExeLowerBound=0.7#To be picked as primary exercise for a muscle, the exercise has to train it with at least this intensity (must be >=)
    muscleStats={}#Dev-NOTES:
        # This is a Nested Dictionary to calculate and store statistics per Muscle-Group. This in order to have a bonus and malus for computing the schedule of exercises. After instantiation, content looks like:
        # The 'count' is only increased for exercises that have an intensitiy above servingThreshold
        #   Or, in fact, it is implemented the way, that each exercise is only counted for one muscle, that is the first with the highest intensity.
        # The muscles are indexed via their numeric index, e.g. 1 for 'Chest'
        # muscleStats={
        #   1 :{
        #      'count': 6,# The number of exercises primary to that muscle are set-up
        #   },
        #   2 :{
        #      'count': 7,# The number of exercises primary to that muscle are set-up
        #   }
        # }
    #------------------------------------------------------------------------------------------
    def __init__(self):
        """Explain it!"""
        self.__class__.instance_counter+=1
        """Initialize some Stuff"""
        self.clear()
    #------------------------------------------------------------------------------------------
    def __del__(self):
        self.__class__.instance_counter-=1
    #------------------------------------------------------------------------------------------
    def clear(self):
        self.idx=0
        self.name=""
        self.equipment=[]#which type of equipment is required for the exercise. See ./settings/values.py/equipID
        self.muscleIntensity=[]#Per Muscle that is attacked by the exercise, a Tuple of Idc and the intensity it trains the muscle (Idx as according to ./settings/values.py/muscleID). An exercise may attack multiple muscles, but with different intensitiy (e.g. 1 for back and simultaneously 0.3 for bizeps). Here stored is a tuple for each muscle, carrying the idx and intensity for the muscle. When the intensity is low for a muscle (below "servingThreshold" set in Class): Then the exercise is not taken for explicitly training that muscle, but when it is picked for another muscle, it still lowers the urgency for the subsidiary muscles in upcoming computations
        self.malus=0.0
        self.bonus=0.0
        self.credit=0.0
        self.urgency=0.0
        self.history=[]
        self.history_shortened=[]
        self.schedule=[]
    #------------------------------------------------------------------------------------------
    def set_attributes(self,idx,name,precedence,equipment,muscle,enabled):
        self.idx=idx
        self.name=name
        self.equipment=copy.deepcopy(equipment)
        self.muscleIntensity=copy.deepcopy(muscle)
        self.precedence=precedence#Temporarily set. Later deleted in _calc_exe_malus_bonus()
        self.enabled=enabled
        if enabled:
            self.enabled=False
            for i in range(len(self.equipment)):
                if cfghandle.cfgh_rt[cfghandle.keyExeEquip][self.equipment[i]]:
                    self.enabled=True
                    break
    #------------------------------------------------------------------------------------------
    def _sort_properties(self):
        self.equipment.sort(key=lambda x: x.value[0])
        #self.muscleIntensity.sort(key=lambda x: x[0].value[0])
        self.muscleIntensity.sort(key=lambda x: x[1], reverse=True)
    @classmethod
    def _sort_properties_list(cls,trgtArray):
        [i._sort_properties() for i in trgtArray]
    def _calc_exe_malus_bonus(self):
        #Inside .malus, temporarily the precedence is stored after the first setting-up steps
        self.bonus=1
        self.malus=self.precedence/exercise.muscleStats[self.muscleIntensity[0][0].value[0]]['count']
        del self.precedence
    @classmethod
    def _calc_class_stats__entry(cls,muscle):
        #Actually an exercise defines multiple muscles in an array. But for the stats, only the muscle is counted, with the highest intensity
        highestIntens=0.0
        highestIdx=0
        for i in range(len(muscle)):
            if muscle[i][1]>highestIntens:
                highestIntens=muscle[i][1]
                highestIdx=i
        try:
            cls.muscleStats[muscle[highestIdx][0].value[0]]['count']+=1
        except KeyError:
            cls.muscleStats.setdefault(muscle[highestIdx][0].value[0], {})['count']=1
    @classmethod
    def _add_exercise(cls,trgtArr,excludedArr,idx,name,precedence,equipment,muscle,enabled):
        toAdd=exercise()
        toAdd.set_attributes(idx,name,precedence,equipment,muscle,enabled)
        if toAdd.enabled:
            trgtArr.append(toAdd)
            cls._calc_class_stats__entry(toAdd.muscleIntensity)
        else:
            excludedArr.append(toAdd)
    # Better don't do such a thing. That messes up the Config-File Handling (especially writing)
    # @classmethod
    # def _set_exercises__strip_enum(cls):
    #     for i in range(len(cfghandle.cfgSetup_rt[cfghandle.keySetupExe])):
    #         # equip=exercise_setup[i][3]
    #         # for j in range(len(equip)):
    #         #     equip[j]=equip[j].value[0]
    #         muscle=cfghandle.cfgSetup_rt[cfghandle.keySetupExe][i][4]
    #         for j in range(len(muscle)):
    #             #muscle[j]=(muscle[j][0].value[0],muscle[j][1])
    #             if isinstance(muscle[j][0], muscleID):
    #                 muscle[j][0]=muscle[j][0].value[0]
    #             elif not isinstance(muscle[j][0],int):
    #                 globV.HCI.printErr("Malformed Exercise Setup. Exiting...")
    #                 sys.exit(4)
    @classmethod
    def set_exercises(cls,trgtArr,excludedArr):
        #cls._set_exercises__strip_enum()
        #for index, (ident, enabled, precedence, equip, muscle) in enumerate(cfghandle.cfgSetup_rt[cfghandle.keySetupExe]):
        for index in range(len(cfghandle.cfgSetup_rt[cfghandle.keySetupExe])):
            ident=cfghandle.cfgSetup_rt[cfghandle.keySetupExe][index][SetupExeIdx.NAME]
            enabled=cfghandle.cfgSetup_rt[cfghandle.keySetupExe][index][SetupExeIdx.ENABLED]
            precedence=cfghandle.cfgSetup_rt[cfghandle.keySetupExe][index][SetupExeIdx.PRECEDENCE]
            equip=cfghandle.cfgSetup_rt[cfghandle.keySetupExe][index][SetupExeIdx.EQUIPMENT]
            muscle=cfghandle.cfgSetup_rt[cfghandle.keySetupExe][index][SetupExeIdx.INTENSITY]
            cls._add_exercise(trgtArr,excludedArr,index,ident,precedence,equip,muscle,enabled)
        for i in range(0,len(trgtArr)):
            trgtArr[i]._calc_exe_malus_bonus()
        cls._sort_properties_list(trgtArr)
        cls._sort_properties_list(excludedArr)
    #------------------------------------------------------------------------------------------
    #The History for a exercise stores the idx of the muscle, to which it was assigned
    @classmethod
    def history_read_file(cls,trgtArray,excludedArray):
        CommonMuscleExercise.history_read_file(trgtArray+excludedArray, history_file_prefix_exercise, history_file_fname_exercise, history_file_fExt)
    @classmethod
    def history_write_file(cls,exerciseArray,excludedArray):
        CommonMuscleExercise.history_write_file(exerciseArray+excludedArray, history_file_prefix_exercise, history_file_fname_exercise, history_file_fExt)
    @classmethod
    def history_trim_file(cls,exerciseArray,excludedArray):
        CommonMuscleExercise.history_trim_file(exerciseArray+excludedArray, history_file_prefix_exercise, history_file_fname_exercise, history_file_fExt)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def history_prepare_shortened_all(cls,trgtArray,workouts_perWeek):
        #derive the credit over 4 weeks
        [i.history_prepare_shortened(int(workouts_perWeek*4)) for i in trgtArray]
    #------------------------------------------------------------------------------------------
    def derive_credit_fromHistory(self,credit_center):
        if self.enabled:
            self.credit=credit_center
            joined_history=self.history_shortened+self.schedule
            hist_len=len(joined_history)
            if hist_len>0:
                i=hist_len-1
                while i>=0:
                    if 0==joined_history[i]:
                        self.credit-=self.malus
                    elif 0<joined_history[i]:
                        self.credit+=self.bonus
                    else:
                        globV.HCI.printErr("Malformed History while Credit calculation. Exiting...")
                        sys.exit()
                    i-=1
        else:
            self.credit=0
        #del self.enabled
    @classmethod
    def derive_credit_fromHistory_all(cls,trgtArray,credit_center):
        [i.derive_credit_fromHistory(credit_center) for i in trgtArray]
    #------------------------------------------------------------------------------------------
    def derive_urgency(self,credit_center,wo_perWeek_total):
        if self.enabled:
            # self.urgency=(credit_center-self.credit)/self.bonus
            self.urgency=(credit_center-self.credit)
        else:
            self.urgency=-100#Just to have something low
        # for muscle in self.muscleIntensity:
        #     if muscle[0].value[0]==muscleID.chest.value[0]:
        #         print(f"{self.name} - {self.credit:.3f}  {self.urgency:.3f}")
    @classmethod
    def derive_urgency_array(self,trgtArray,credit_center,wo_perWeek_total):
        [i.derive_urgency(credit_center,wo_perWeek_total) for i in trgtArray]
        # print("\n")
#-----------------------------------------------------