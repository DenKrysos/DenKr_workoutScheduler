#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-09

@author: Dennis Krummacker
'''


## Some Fundamentals
import package.importMe_fundamental  # @UnusedImport


## System Packages
# import math
from builtins import object




##Workout-Scheduler Packages
from commonFeatures.common_muscle_exercise import CommonMuscleExercise
from workoutScheduler.muscle import muscle


##Fundamental Project Settings
from settings.path_and_file import (
    history_file_fExt,
    history_file_prefix_exercise,
    history_file_fname_exercise
)

##Individual Configuration
from _1cfg.setup import exercise_setup
from _1cfg.configuration import exercisesToInclude



#-----------------------------------------------------
#Leave the default function just alone. It essentially only serves as a template.
# -> If you want to change muscle's values, Look into ./_1cfg/setup.py
exercise_setup_default=[
]
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
class exercise(object):
    instance_counter=0
    #primaryExeLowerBound=0.7#To be picked as primary exercise for a muscle, the exercise has to train it with at least this intensity (must be >=)
    servingThreshold=0.45#Only when the intensity for which an exercise serves a muscle is at least (>=) this, the exercise can be explicitly picked to serve the muscle. (See also comment on "self.muscleIntensity")
    minimumServing=0.7#A muscle has to be trained with more than this intensity (increase as long as <=minimumServing). If picked exercises serve a muscle that is scheduled for a workout less than this, additional exercises (with intensity <1) are included.
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
        exercise.instance_counter+=1
        """Initialize some Stuff"""
        self.clear()
    #------------------------------------------------------------------------------------------
    def __del__(self):
        exercise.instance_counter-=1
    #------------------------------------------------------------------------------------------
    def clear(self):
        self.idx=0
        self.name=""
        self.equipment=[]#which type of equipment is required for the exercise. See ./settings/values.py/equipmentIdentifier
        self.muscleIntensity=[]#Per Muscle that is attacked by the exercise, a Tuple of Idc and the intensity it trains the muscle (Idx as according to ./settings/values.py/muscleIdentifier). An exercise may attack multiple muscles, but with different intensitiy (e.g. 1 for back and simultaneously 0.3 for bizeps). Here stored is a tuple for each muscle, carrying the idx and intensity for the muscle. When the intensity is low for a muscle (below "servingThreshold" set in Class): Then the exercise is not taken for explicitly training that muscle, but when it is picked for another muscle, it still lowers the urgency for the subsidiary muscles in upcoming computations
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
        self.equipment=equipment
        self.muscleIntensity=muscle
        self.precedence=precedence#Temporarily set. Later deleted in _calc_exe_malus_bonus()
        self.enabled=enabled
        if enabled:
            self.enabled=False
            for i in range(len(self.equipment)):
                if exercisesToInclude[self.equipment[i]]:
                    self.enabled=True
                    break
    #------------------------------------------------------------------------------------------
    def _sort_properties(self):
        self.equipment.sort(key=lambda x: x)
        self.muscleIntensity.sort(key=lambda x: x[0])
    @classmethod
    def _sort_properties_list(cls,trgtArray):
        [i._sort_properties() for i in trgtArray]
    def _calc_exe_malus_bonus(self):
        #Inside .malus, temporarily the precedence is stored after the first setting-up steps
        self.malus=self.precedence/exercise.muscleStats[self.muscleIntensity[0][0]]['count']
        del self.precedence
        self.bonus=1/exercise.muscleStats[self.muscleIntensity[0][0]]['count']
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
            cls.muscleStats[muscle[highestIdx][0]]['count']+=1
        except KeyError:
            cls.muscleStats.setdefault(muscle[highestIdx][0], {})['count']=1
    @classmethod
    def _add_exercise(cls,trgtArr,excludedArr,idx,name,precedence,equipment,muscle,enabled):
        toAdd=exercise()
        toAdd.set_attributes(idx,name,precedence,equipment,muscle,enabled)
        if toAdd.enabled:
            trgtArr.append(toAdd)
            cls._calc_class_stats__entry(muscle)
        else:
            excludedArr.append(toAdd)
    @classmethod
    def set_exercises(cls,trgtArr,excludedArr):
        for index, (ident, enabled, precedence, equip, muscle) in enumerate(exercise_setup):
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
    def history_prepare_shortened(self,workouts_perWeek):
        #derive the credit over 4 weeks
        CommonMuscleExercise.history_prepare_shortened(self, int(workouts_perWeek*4))
    @classmethod
    def history_prepare_shortened_all(cls,trgtArray,workouts_perWeek):
        [i.history_prepare_shortened(workouts_perWeek) for i in trgtArray]
    def history_push_schedule(self):
        CommonMuscleExercise.history_push_schedule(self)
    @classmethod
    def history_push_schedule_all(cls,trgtList):
        [i.history_push_schedule() for i in trgtList]
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
                        print("Malformed History while Credit calculation. Exiting...")
                        exit()
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
            self.urgency=(credit_center-self.credit)/self.bonus
        else:
            self.urgency=0
    @classmethod
    def derive_urgency_array(self,trgtArray,credit_center,wo_perWeek_total):
        [i.derive_urgency(credit_center,wo_perWeek_total) for i in trgtArray]
#-----------------------------------------------------