#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-09

@author: Dennis Krummacker
'''


## Some Fundamentals
import DenKr_essentials_py.importMe_fundamental  # @UnusedImport


## System Packages
# import math
# from builtins import object


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV



##Workout-Scheduler Packages
from commonFeatures.common_muscle_exercise import CommonMuscleExercise


##Fundamental Project Settings
from settings.path_and_file import (
    history_file_fExt,
    history_file_prefix_muscle,
    history_file_fname_muscle
)
##Regarding Arrangement/Ensemble
# from settings.values import muscleID

##Individual Configuration
import settings.config_handler as cfghandle
# Instead: Also using a read handle within cfghandle
#from _1cfg.setup import muscle_setup



#-----------------------------------------------------
    #("quads",1,1.75,10)#("quads",1,2,10)
    #("glutes",1,1.75,10)#("glutes",1,2,10)
    # - - - - - -
#Leave the default function just alone. It essentially only serves as a template.
# -> If you want to change muscle's values, Look into ./_1cfg/setup.py
# muscle_setup_default=[
#     (muscleID.chest,1,2,10),
#     (muscleID.back,1,2,10),
#     (muscleID.delt_front,2,0.75,5),
#     (muscleID.delt_rear,2,1,5),
#     (muscleID.rotator_cuff,2,1.25,6),
#     (muscleID.delt_side,2,1,5),
#     (muscleID.quads_n_glutes,1,1.5,10),#1.75-2 per Week
#     (muscleID.biceps,2,1,5),
#     (muscleID.triceps,2,1,5),
#     (muscleID.hamstrings,2,0.9,5),#1
#     (muscleID.abs,1,1.5,8),
#     (muscleID.calves,2,0.8,6),#("calves",1,1.5,7)
#     (muscleID.trapez,2,1,5),
#     (muscleID.lower_back,2,1,5)#0.75
# ]
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
class muscle(CommonMuscleExercise):
    instance_counter=0
    #------------------------------------------------------------------------------------------
    def __init__(self):
        """Explain it!"""
        self.__class__.instance_counter += 1
        """Initialize some Stuff"""
        self.clear()
    #------------------------------------------------------------------------------------------
    def __del__(self):
        self.__class__.instance_counter -= 1
    #------------------------------------------------------------------------------------------
    def clear(self):
        self.idx=0
        self.name=""
        self.muscle_class=0#0: undefined, 1: big muscle, 2: small muscle
        self.wo_pW = 0#Workouts per Week for this muscle
        self.set_pW = 0#Sets per Week
        self.malus=0.0#A "perWorkout" for this muscle. Also used as "Malus" for not training it
        self.bonus=0.0
        self.credit=0.0#used to determine the urgency of training this muscle
        self.urgency=0.0#A more thorough, elaborate and sophisticated value to determine to actual urgency. The credit goes into its calculation
        self.history=[]
        self.history_shortened=[]
        #self.urgency=-1
        self.schedule=[]
    #------------------------------------------------------------------------------------------
    def set_attributes(self,wo_perWeek_total,idx,name,muscle_class,wo_perWeek,set_perWeek):
        self.idx=idx
        self.name=name
        self.muscle_class=muscle_class
        self.wo_pW=wo_perWeek
        self.set_pW=set_perWeek
        # self.malus=wo_perWeek/wo_perWeek_total
        # self.bonus=1/wo_perWeek
        self.malus=wo_perWeek/(wo_perWeek_total-wo_perWeek)
        self.bonus=1
    #------------------------------------------------------------------------------------------
    @classmethod
    def _add_muscle(cls,trgtArr,wo_perWeek_total,idx,name,muscletype,wo_perWeek,sets_perWeek):
        trgtArr.append(muscle())
        trgtArr[len(trgtArr)-1].set_attributes(wo_perWeek_total,idx,name,muscletype,wo_perWeek,sets_perWeek)
    @classmethod
    def set_muscles(cls,trgtArr,wo_perWeek_total):
        for ident, bigOrSmall, workouts, sets in cfghandle.cfgSetup_handle[cfghandle.keySetupMuscle]:
            cls._add_muscle(trgtArr,wo_perWeek_total,ident.value[0],ident.value[1],bigOrSmall,workouts,sets)
    #------------------------------------------------------------------------------------------
    #The History for a muscle stores to which Intensity it was trained (which is depending on the scheduled exercise)
    @classmethod
    def history_read_file(cls,trgtArray):
        CommonMuscleExercise.history_read_file(trgtArray, history_file_prefix_muscle, history_file_fname_muscle, history_file_fExt)
    @classmethod
    def history_write_file(cls,muscleArray):
        CommonMuscleExercise.history_write_file(muscleArray, history_file_prefix_muscle, history_file_fname_muscle, history_file_fExt)
    @classmethod
    def history_trim_file(cls,muscleArray):
        CommonMuscleExercise.history_trim_file(muscleArray, history_file_prefix_muscle, history_file_fname_muscle, history_file_fExt)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def history_prepare_shortened_all(cls,trgtArray,workouts_perWeek):
        #derive the credit over 2 weeks
        [i.history_prepare_shortened(int(workouts_perWeek*2)) for i in trgtArray]
    #------------------------------------------------------------------------------------------
    def derive_credit_fromHistory(self,credit_center):
        self.credit=credit_center
        joined_history=self.history_shortened+self.schedule
        hist_len=len(joined_history)
        if hist_len>0:
            i=hist_len-1
            while i>=0:
                if self.minimumServing>joined_history[i]:
                    self.credit-=self.malus
                    self.credit+=joined_history[i]*0.5*self.bonus
                else:
                    self.credit+=joined_history[i]*self.bonus
                # else:
                #     globV.HCI.printErr("Malformed History while Credit calculation. Exiting...")
                #     exit()
                i-=1
    @classmethod
    def derive_credit_fromHistory_all(cls,trgtArray,credit_center):
        [i.derive_credit_fromHistory(credit_center) for i in trgtArray]
    #------------------------------------------------------------------------------------------
    def derive_urgency(self,credit_center,wo_perWeek_total):
        #To make it a little more sophisticated: Derive a value which influences the urgency based on a ratio of workout-free days in relation to workouts-to-do (-> Long free period for a muscle -> high urgency. -> Many workouts with short pause-periods -> lowers urgency. -> Pretty much in schedule and even distribution -> low to none influence)
        #  - To account for that, I analyse the last resting period
        rest_period=0
        joined_history=self.history_shortened+self.schedule
        hist_len=len(joined_history)
        if hist_len>0:
            i=hist_len-1
            while i>=0:
                if self.minimumServing>joined_history[i]:
                    rest_period+=(1-joined_history[i])
                else:
                    break;
                # else:
                #     globV.HCI.printErr("Malformed History while Credit calculation. Exiting...")
                #     exit()
                i-=1
        rest_supposed=(wo_perWeek_total-self.wo_pW)/self.wo_pW
        rest_ratio=rest_period/rest_supposed
        #
        #ToDo: As factor for the rest_ratio, another value might be better suited
        #self.urgency=(credit_center-self.credit)/self.bonus+0.5*rest_ratio
        self.urgency=(credit_center-self.credit)+0.5*rest_ratio
        #print(f"{self.name} - {self.credit:.3f}  {0.5*rest_ratio}  {self.urgency:.3f}")
    @classmethod
    def derive_urgency_array(self,trgtArray,credit_center,wo_perWeek_total):
        [i.derive_urgency(credit_center,wo_perWeek_total) for i in trgtArray]
        #print("---------------")
#-----------------------------------------------------
