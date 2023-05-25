#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2020-11-18
Last Update: 2023-04-13

@author: Dennis Krummacker
'''

import sys


## Some Fundamentals
import DenKr_essentials_py.importMe_fundamental  # @UnusedImport


## System Packages
from builtins import object
import random
from itertools import groupby
#import bisect




##DenKr Packages
from DenKr_essentials_py.ansiescape import *  # @UnusedImport @UnusedWildImport
from auxiliary import math  # @UnusedImport @UnusedWildImport
from auxiliary.filesystem import directory_history_tidy
import datetime


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV

##Other Files for Project
##Workout-Scheduler Packages
from workoutScheduler.muscle import muscle
from workoutScheduler.exercise import exercise
##Regarding Arrangement/Ensemble
from settings.values import muscleID
##Individual Configuration
import settings.config_handler as cfghandle





#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO
#
#- For "Volume-Scaling": A better Threshold to determine when scaling should be performed
#
#- Add an extra Slot for Warm-Up?. Exercises like BW-Side-Lateral-Raise would fall into that. That slot can also be left empty by the computation, which gives the user so-to-speak freeroom to then have a warmup after own gusto.
#   But with the occassional suggestion of explicit warmup exercises, it can be made sure that these exercises are done regularly, every now and then.



        
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
class workout(object):
    instance_counter=0# should always stay '1' during runtime
    #------------------------------------------------------------------------------------------
    def __init__(self):
        """Explain it!"""
        workout.instance_counter += 1
        """Initialize some Stuff"""
        self.muscle_groups=[]
        self.exercises=[]
        self.exercises_excluded=[]
        self.workouts_perWeek=0
        self.supersets=()
        self.bigMuscle_precedence_tolerance=0.0
        self.num_workout_toCompute=0
        self.group_by_superset=0
        self.muscles_per_workout=0
        self.credit_center=0
        # - - - - - - - - - -
        self.muscle_workingSet=[]
        self.exercise_workingSet=[]
    #------------------------------------------------------------------------------------------
    def __del__(self):
        workout.instance_counter -= 1
    #------------------------------------------------------------------------------------------
    def _set_basics_default(self):
        self.workouts_perWeek=3.5
        #self.bigMuscle_precedence_tolerance=7/self.workouts_perWeek-1
        self.num_workout_toCompute=int(self.workouts_perWeek*2)#6
        self.group_by_superset=1
    def set_basics(self):
        self.workouts_perWeek=cfghandle.cfgh_rt[cfghandle.keyWOpW]
        #self.bigMuscle_precedence_tolerance=7/self.workouts_perWeek-1
        self.num_workout_toCompute=cfghandle.cfgh_rt[cfghandle.keyNumComp]
        self.group_by_superset=1
    def set_phase2(self):
        #self.bigMuscle_precedence_tolerance=self.muscle_groups[0].malus*0.45
        self.bigMuscle_precedence_tolerance=0#Hem, I say, we calc this dynamically for every run on the position, where it is used
        #
        def calc_muscles_per_workout():
            muscles_perWeek_total=0.0
            i=0
            while i<len(self.muscle_groups):
                if self.muscle_groups[i].name!="glutes":#Because we assume that quads and glutes are most of the time trained in conjunction
                    muscles_perWeek_total+=self.muscle_groups[i].wo_pW
                i+=1
            #print(f"musperWeek {muscles_perWeek_total} | {muscles_perWeek_total/self.workouts_perWeek}")
            muscPerWorkout=muscles_perWeek_total/self.workouts_perWeek
            self.muscles_per_workout=int(muscles_perWeek_total//self.workouts_perWeek)
            #Smoothen lacking float precision
            delta=self.muscles_per_workout+1-muscPerWorkout
            if 0<delta and 0.00001>abs(delta):
                self.muscles_per_workout+=1
            return muscles_perWeek_total
        muscles_perWeek_total=calc_muscles_per_workout()
        #
        def muscle_volume_normalization():
            musPerWorkoutFloat=muscles_perWeek_total/self.workouts_perWeek
            normRatio=self.muscles_per_workout/musPerWorkoutFloat
            for muscle in self.muscle_groups:
                muscle.wo_pW*=normRatio
        #
        if not cfghandle.cfgh_rt[cfghandle.keyVolScal]:
            muscle_volume_normalization()
            muscles_perWeek_total=calc_muscles_per_workout()
        #
        if self.muscles_per_workout!=4:
            globV.HCI.printStd(f"Attention! A \"muscles_per_workout\" of other than 4 was calculated ({muscles_perWeek_total/self.workouts_perWeek}). You might want to have a look into that (maybe overwrite the value directly, after \"set_phase2()\"). For most cases, 4 muscles per workout is an appropriate amount/value. This tool afterwards allows a reasonable deviation from that anyway to adjust individual workouts to the urgency of muscle groups.")
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def set_exercises(self):
        exercise.set_exercises(self.exercises,self.exercises_excluded)
    def set_muscles(self):
        muscle.set_muscles(self.muscle_groups, self.workouts_perWeek)
        self.supersets=(
            (muscleID.chest.value[0],muscleID.back.value[0]),
            (muscleID.biceps.value[0],muscleID.triceps.value[0])
        )
    def set(self):
        self.set_basics()
        self.set_muscles()
        self.set_exercises()
        self.validate_config()
        self.set_phase2()
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def validate_config(self):
        #ToDo: This is very much to be extende
        for muscle in self.muscle_groups:
            if muscle.wo_pW>self.workouts_perWeek:
                globV.HCI.printErr("Invalid Configuration!")
                globV.HCI.printErr(f"  You configured the muscle \"{muscle.name}\" to have more Workouts-per-Week than you set as total Workouts-per-Week.")
                globV.HCI.printErr("  That doesn't make sense, right?")
                globV.HCI.printErr("  You should adjust this.")
    #------------------------------------------------------------------------------------------
    def debug_print_muscles(self,lst,indiv_muscle_c):
        globV.HCI.printStd("Debug - Muscles: (Counter: %d)"%(indiv_muscle_c))
        i=0
        while i<len(lst):
            globV.HCI.printStd(lst[i].name)
            i+=1
        globV.HCI.printStd("")
    def debug_print_credits_sorted(self):
        printSet=[]
        musNum=len(self.muscle_groups)
        i=0
        while i<musNum:
            printSet.append(self.muscle_groups[i])
            i+=1
        cr_ave=0
        #order after credit
        printSet.sort(key=lambda x: x.credit, reverse=False)
        for i in range(0,len(printSet),1):
            cr_ave+=printSet[i].credit
        cr_ave/=len(printSet)
        globV.HCI.printStd("Credits (Ave %2.2f): [ "%(cr_ave),end='')
        for i in range(0,len(printSet)-1,1):
            globV.HCI.printStd("%s:%2.2f, "%(printSet[i].name,printSet[i].credit),end='')
        globV.HCI.printStd("%s:%2.2f"%(printSet[len(printSet)-1].name,printSet[len(printSet)-1].credit),end='')
        globV.HCI.printStd(" ]")
    def debug_print_credits(self):
        cr_ave=0
        for i in range(0,len(self.muscle_groups),1):
            cr_ave+=self.muscle_groups[i].credit
        cr_ave/=len(self.muscle_groups)
        globV.HCI.printStd("Credits (Ave %2.2f): [ "%(cr_ave),end='')
        for i in range(0,len(self.muscle_groups)-1,1):
            globV.HCI.printStd("%s:%2.2f, "%(self.muscle_groups[i].name,self.muscle_groups[i].credit),end='')
        globV.HCI.printStd("%s:%2.2f"%(self.muscle_groups[len(self.muscle_groups)-1].name,self.muscle_groups[len(self.muscle_groups)-1].credit),end='')
        globV.HCI.printStd(" ]")
    def debug_print_credits_workingSet_generic(self,trgtArray):
        cr_ave=0
        for i in range(0,len(trgtArray),1):
            cr_ave+=trgtArray[i].credit
        cr_ave/=len(trgtArray)
        globV.HCI.printStd("WorkingSet[Cred] (Ave %2.2f): [ "%(cr_ave),end='')
        for i in range(0,len(trgtArray)-1,1):
            globV.HCI.printStd("%s:%2.2f, "%(trgtArray[i].name,trgtArray[i].credit),end='')
        globV.HCI.printStd("%s:%2.2f"%(trgtArray[len(trgtArray)-1].name,trgtArray[len(trgtArray)-1].credit),end='')
        globV.HCI.printStd(" ]")
    def debug_print_credits_workingSet_muscle(self):
        self.debug_print_credits_workingSet_generic(self.muscle_workingSet)
    def debug_print_credits_workingSet_exercise(self):
        self.debug_print_credits_workingSet_generic(self.exercise_workingSet)
    def debug_print_urgency_workingSet_generic(self,trgtArray):
        urg_ave=0
        for i in range(0,len(trgtArray),1):
            urg_ave+=trgtArray[i].urgency
        urg_ave/=len(trgtArray)
        globV.HCI.printStd("WorkingSet[Urg] (Ave %2.2f): [ "%(urg_ave),end='')
        for i in range(0,len(trgtArray)-1,1):
            globV.HCI.printStd("%s:%2.2f, "%(trgtArray[i].name,trgtArray[i].urgency),end='')
        globV.HCI.printStd("%s:%2.2f"%(trgtArray[len(trgtArray)-1].name,trgtArray[len(trgtArray)-1].urgency),end='')
        globV.HCI.printStd(" ]")
    def debug_print_urgency_workingSet_muscle(self):
        self.debug_print_urgency_workingSet_generic(self.muscle_workingSet)
    def debug_print_urgency_workingSet_exercise(self):
        self.debug_print_urgency_workingSet_generic(self.exercise_workingSet)
    def debug_print_muscleList(self,mlst):
        lstlen=len(mlst)
        i=0
        while i<lstlen:
            globV.HCI.printStd(mlst[i].name)
            i+=1
        globV.HCI.printStd("")
    #------------------------------------------------------------------------------------------
    def history_read(self):
        directory_history_tidy()
        #[i.history_read_file() for i in self.muscle_groups]
        muscle.history_read_file(self.muscle_groups)
#        #check for consistency
#         name_first=self.muscle_groups[0].idx
#         len_first=len(self.muscle_groups[0].history)
#         for i in range(1,len(self.muscle_groups),1):
#             len_cur=len(self.muscle_groups[i].history)
#             if len_first!=len_cur:
#                 globV.HCI.printStd("Malformed History: Unmatching lenghts. History of muscle \"%s\" is of different length (%d) than of muscle \"%s\" (%d)"%(name_first,len_first,self.muscle_groups[i].idx,len_cur))
        muscle.history_prepare_shortened_all(self.muscle_groups,self.workouts_perWeek)
        exercise.history_read_file(self.exercises,self.exercises_excluded)
        exercise.history_prepare_shortened_all(self.exercises,self.workouts_perWeek)
        exercise.history_prepare_shortened_all(self.exercises_excluded,self.workouts_perWeek)
        self.history_autoTrim()
    def history_write(self):
        #[i.history_write_file() for i in self.muscle_groups]
        muscle.history_write_file(self.muscle_groups)
        exercise.history_write_file(self.exercises,self.exercises_excluded)
    def history_write_userQuery(self):
        inputtry=0
        while 1:
            globV.HCI.printStd("»Shall the history-files be updated with the recent computation?« (y/n)")
            inp=input()
            if inp=="y" or inp=="yes" or inp=="ja" or inp=="j" or inp=="1":
                globV.HCI.printStd("-> »Updating History«")
                #inputtry=3
                return True
            elif inp=="n" or inp=="no" or inp=="nein" or inp=="n" or inp=="0":
                globV.HCI.printStd("-> »NO Update to History«")
                #inputtry=3
                return False
            else:
                globV.HCI.printStd("-> »Invalid Input.",end='')
                inputtry+=1
                if inputtry>=3:
                    globV.HCI.printStd("«\n»Yeah, I propose we just cancel this...«\n")
                    return False
                else:
                    globV.HCI.printStd(" Try again.«\n")
    def push_schedule_toHistory(self):
        muscle.history_push_schedule_all(self.muscle_groups)
        #muscle.history_prepare_shortened_all(self.muscle_groups,self.workouts_perWeek)
        exercise.history_push_schedule_all(self.exercises)
        exercise.history_push_schedule_all(self.exercises_excluded)
        #exercise.history_prepare_shortened_all(self.exercises,self.workouts_perWeek)
    #------------------------------------------------------------------------------------------
    def history_autoTrim(self):
        autoTrimThreshold=self.workouts_perWeek*27
        if len(self.muscle_groups[0].history)>autoTrimThreshold or len(self.exercises[0].history)>autoTrimThreshold:
            self.history_trim()
    def history_trim(self):
        #Trims the history-Files down to a number of entries corresponding to the least required amount (That is, the number of entries a calculation looks back to derive the urgency)
        muscle.history_trim_file(self.muscle_groups)
        exercise.history_trim_file(self.exercises,self.exercises_excluded)
    def history_trim_query(self):
        inputtry=0
        while 1:
            globV.HCI.printStd("»History Files Trimming called. Shall I proceed?«")
            globV.HCI.printStd("    (Continue: y / yes / ja / j / 1)")
            globV.HCI.printStd("    (Abort: n / no / nein / 0)")
            inp=input()
            if inp=="y" or inp=="yes" or inp=="ja" or inp=="j" or inp=="1":
                globV.HCI.printStd("-> »Trimming History«")
                self.set()
                self.history_read()
                self.history_trim()
                return True
            elif inp=="n" or inp=="no" or inp=="nein" or inp=="0":
                globV.HCI.printStd("-> »NOT Trimming History«")
                return False
            else:
                globV.HCI.printStd("-> »Invalid Input.",end='')
                inputtry+=1
                if inputtry>=3:
                    globV.HCI.printStd("«\n»Yeah, Ehem, I propose we just cancel this...«\n")
                    return False
                else:
                    globV.HCI.printStd(" Try again.«\n")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __history_show_WorkoutSchedule_element_generic_reverse(self,exeList,index,chosenList):
        #index+=1#Because when using it subtractive to access the entries in reverse order, one would actually have to use 'len(List)-1'. With this increment here, this is done for
        #  ^^ But that's already assured by how the function is driven by its wrapper
        scheduled_exe=[]
        scheduled_mus=[]
        for iexercise in exeList:
            iList=getattr(iexercise,chosenList)
            if len(iList)>=index:
                if 0<iList[len(iList)-index]:
                    scheduled_exe.append(iexercise)
        for imuscle in self.muscle_groups:
            iList=getattr(imuscle,chosenList)
            if len(iList)>=index:
                if 0<iList[len(iList)-index]:
                    scheduled_mus.append(imuscle)
        #
        leftEnt=len(scheduled_exe)
        while 0<leftEnt:
            iexercise=scheduled_exe[0]
            iList=getattr(iexercise,chosenList)
            exeForThisMus=[]
            exeForThisMus.append((0,iexercise))
            for j in range(1, len(scheduled_exe)):
                jexercise=scheduled_exe[j]
                jList=getattr(jexercise,chosenList)
                if iList[len(iList)-index]==jList[len(jList)-index]:
                    exeForThisMus.append((j,jexercise))
            for imuscle in scheduled_mus:
                if iList[len(iList)-index]==imuscle.idx:
                    globV.HCI.printStd("%s - %s"%(imuscle.name,exeForThisMus[0][1].name))
                    if 1<len(exeForThisMus):
                        globV.HCI.printStd(" ",end="")
                        for i in range(1,len(exeForThisMus),1):
                            globV.HCI.printStd("  >& %s"%(exeForThisMus[i][1].name),end="")
                        globV.HCI.printStd("")
            for j in range(len(exeForThisMus)-1,-1,-1):
                scheduled_exe.pop(exeForThisMus[j][0])
                leftEnt-=1
    def _history_show_previousWorkoutSchedule_element(self,exeList,index):
        globV.HCI.printStd("===============")
        globV.HCI.printStd("== Workout t-%d"%(index))
        globV.HCI.printStd("---------------")
        self.__history_show_WorkoutSchedule_element_generic_reverse(exeList,index,"history_shortened")
    def history_show_previousWorkoutSchedule(self):
        #TODO
        exeList=self.exercises+self.exercises_excluded
        lenMax=0
        i=0
        while i<len(exeList):
            lenMax=max(lenMax,len(exeList[i].history_shortened))
            i+=1
        
        numOutput=int(self.workouts_perWeek*2)
        numOutput=min(numOutput,lenMax)

        i=numOutput
        while i>=1:
            self._history_show_previousWorkoutSchedule_element(exeList,i)
            if 1<i:
                globV.HCI.printStd("")
            i-=1
    def history_show_previousWorkoutSchedule_terminal(self):
        globV.HCI.printStd("######################")
        globV.HCI.printStd("# Previous Workouts: #")
        self.history_show_previousWorkoutSchedule()
        globV.HCI.printStd("#########################################")
        globV.HCI.printStd("#########################################")
        globV.HCI.printStd("#########################################\n")
    def _history_show_computedWorkoutSchedule_element(self,index,dotw="DotW",year="2023",month="MM",day="DD"):
        scheduled_exe=[]
        scheduled_mus=[]
        for iexercise in self.exercises:
            if 0<iexercise.schedule[index]:
                scheduled_exe.append(iexercise)
        for imuscle in self.muscle_groups:
            if 0<imuscle.schedule[index]:
                scheduled_mus.append(imuscle)
        globV.HCI.printStd("===============")
        #globV.HCI.printStd("== Workout %d"%(i+1))
        if "DotW"==dotw:
            dotw=dotw+f"{index+1}"
        globV.HCI.printStd(f"== {dotw}, {year}-{month}-{day}")
        globV.HCI.printStd("---------------")
        leftEnt=len(scheduled_exe)
        while 0<leftEnt:
            iexercise=scheduled_exe[0]
            exeForThisMus=[]
            exeForThisMus.append((0,iexercise))
            for j in range(1, len(scheduled_exe)):
                jexercise=scheduled_exe[j]
                if jexercise.schedule[index]==iexercise.schedule[index]:
                    exeForThisMus.append((j,jexercise))
            for imuscle in scheduled_mus:
                if iexercise.schedule[index]==imuscle.idx:
                    globV.HCI.printStd("%s - %s"%(imuscle.name,exeForThisMus[0][1].name))
                    if 1<len(exeForThisMus):
                        globV.HCI.printStd(" ",end="")
                        for i in range(1,len(exeForThisMus),1):
                            globV.HCI.printStd("  >& %s"%(exeForThisMus[i][1].name),end="")
                        globV.HCI.printStd("")
            for j in range(len(exeForThisMus)-1,-1,-1):
                scheduled_exe.pop(exeForThisMus[j][0])
                leftEnt-=1
    def history_show_computedWorkoutSchedule(self,date=None):
        def _set_weekday():
            day=date.weekday()
            if 0==day:
                return "Mo"
            elif 1==day:
                return "Tu"
            elif 2==day:
                return "We"
            elif 3==day:
                return "Th"
            elif 4==day:
                return "Fr"
            elif 5==day:
                return "Sa"
            elif 6==day:
                return "Su"
            else:
                return "DotW"
        daydelta=7.0/self.workouts_perWeek
        if not cfghandle.cfgh_rt[cfghandle.keyOutRev]:
            i=0
            while i<len(self.muscle_groups[0].schedule):
                if 0<i:
                    globV.HCI.printStd("\n")
                if date is None:
                    self._history_show_computedWorkoutSchedule_element(i)
                else:
                    dotw=_set_weekday()
                    self._history_show_computedWorkoutSchedule_element(i,dotw,date.strftime('%Y'),date.strftime('%m'),date.strftime('%d'))
                    date=date+datetime.timedelta(days=int(daydelta))
                i+=1
        elif cfghandle.cfgh_rt[cfghandle.keyOutRev]:
            if not date is None:
                date=date+datetime.timedelta(days=int(daydelta*(len(self.muscle_groups[0].schedule)-1)))
            i=len(self.muscle_groups[0].schedule)-1
            while i>=0:
                if len(self.muscle_groups[0].schedule)-1>i:
                    globV.HCI.printStd("\n")
                if date is None:
                    self._history_show_computedWorkoutSchedule_element(i)
                else:
                    dotw=_set_weekday()
                    self._history_show_computedWorkoutSchedule_element(i,dotw,date.strftime('%Y'),date.strftime('%m'),date.strftime('%d'))
                    date=date-datetime.timedelta(days=int(daydelta))
                i-=1
        else:
            globV.HCI.printStd("Invalid Value given for \"upcomingOutput_Reverse\"")
    def history_show_computedWorkoutSchedule_terminal(self):
        globV.HCI.printStd("######################")
        globV.HCI.printStd("# Computed Schedule: #  (Reverse-Output: %s)"%(cfghandle.cfgh_rt[cfghandle.keyOutRev]))
        self.history_show_computedWorkoutSchedule()
        globV.HCI.printStd("")
        globV.HCI.printStd("#########################################")
        globV.HCI.printStd("#########################################")
        globV.HCI.printStd("\n")
    def print_Fin(self):
        globV.HCI.printStd("\nFin.\nGood Success with your endeavours.\n")
        globV.HCI.printStd("P.S.: Oh yeah, and remember to always do your fucking »Facepull«! ;oD")
        globV.HCI.printStd("      And don't forget your »YTWL«...\n")
    #------------------------------------------------------------------------------------------
    def muscles_analyse_history(self):
        muscle.derive_credit_fromHistory_all(self.muscle_groups,self.credit_center)
        muscle.derive_urgency_array(self.muscle_groups,self.credit_center,self.workouts_perWeek)
        exercise.derive_credit_fromHistory_all(self.exercises,self.credit_center)
        exercise.derive_urgency_array(self.exercises,self.credit_center,self.workouts_perWeek)
    def muscles_analyse_urgency(self):
        #First, init the workingSet, later on we work on that
        self.muscle_workingSet=[]
        musNum=len(self.muscle_groups)
        i=0
        while i<musNum:
            self.muscle_workingSet.append(self.muscle_groups[i])
            i+=1
        #order after credit
        self.muscle_workingSet.sort(key=lambda x: x.urgency, reverse=True)
        #Give these entries with the same urgency a random shuffle among them.
        # Group the sublists based on their first element
        groups=[list(g) for _, g in groupby(self.muscle_workingSet, lambda x: x.urgency)]
        # Shuffle each group randomly
        for group in groups:
            random.shuffle(group)
        # Concatenate the shuffled groups back into a single list
        self.muscle_workingSet=[item for group in groups for item in group]
        #
        #ToDo: A proper Value / Calculation for the precedence_tolerance
        self.bigMuscle_precedence_tolerance=0.29
        #
        self.exercise_workingSet=[]
        exeNum=len(self.exercises)
        i=0
        while i<exeNum:
            self.exercise_workingSet.append(self.exercises[i])
            i+=1
        self.exercise_workingSet.sort(key=lambda x: x.urgency, reverse=True)
        #Shuffle
        groups=[list(g) for _, g in groupby(self.exercise_workingSet, lambda x: x.urgency)]
        # Shuffle each group randomly
        for group in groups:
            random.shuffle(group)
        # Concatenate the shuffled groups back into a single list
        self.exercise_workingSet=[item for group in groups for item in group]
    def muscles_assure_rest_old(self):#deprecated, not used anymore
        # (detailed workout spread across days) to make sure that a muscle has 48-72 h of rest
        #move muscles with no preceeding rest (i.e. was trained last workout) to the end of the list
        i=len(self.muscle_workingSet)-1
        while i>=0:
            joined_history=self.muscle_workingSet[i].history_shortened+self.muscle_workingSet[i].schedule
            hist_len=len(joined_history)
            if hist_len>0:
                if joined_history[hist_len-1]>=exercise.minimumServing:
                    #self.muscle_workingSet.append(self.muscle_workingSet.pop(self.muscle_workingSet.index(5)))
                    #self.muscle_workingSet.append(self.muscle_workingSet.pop(i))
                    self.muscle_workingSet.pop(i)
            i-=1
    def muscles_assure_rest(self):
        # (detailed workout spread across days) to make sure that a muscle has 48-72 h of rest
        #move muscles with no preceeding rest (i.e. was trained last workout) to the end of the list
        i=len(self.muscle_workingSet)-1
        while i>=0:
            if 0.95<self.muscle_workingSet[i].rest_supposed and 0==self.muscle_workingSet[i].rest_period:
                self.muscle_workingSet.pop(i)
            i-=1
    #------------------------------------------------------------------------------------------
    def _is_supersetMuscle(self,muscle):
        #is_supset=0
        for i in range(0,len(self.supersets)):
            for j in range(0,2):
                if muscle.idx==self.supersets[i][j]:
                    return (True,i,j)
        return (False,0,0)
    def workoutArrange_optimization_urgencyAdjust(self,picked_pre,indiv_muscle_c):
        #Assure that we are not doing too much or too little. I.e. check where the muscles' credits are laying in relation to the baseline of 2
        #Means, easing training, if even the picked muscles are heavy over 2 or pushing (maybe temporarily) a little harder to keep up if there are many muscles way below 2
        #--------------------
        #after superset-grouping and smoothening, again an ease-down, possibly remove muscles from the schedule, while making sure supersets are kept grouped or removed as pair
        #todo
        #pay attention to count quads+glutes only as one exercise
        #------------
        #Already checked in arrange-func
#         quadglute=[-1,-1]
#         for i in range(0,len(picked_pre)):
#             if picked_pre[i].name=="quads":
#                 quadglute[0]=i
#             elif picked_pre[i].name=="glutes":
#                 quadglute[1]=i
#         #if quadglute[0]!=-1 and quadglute[1]==-1 or quadglute[0]==-1 and quadglute[1]!=-1:
#         if quadglute[0]==-1 and quadglute[1]==-1:
#             pass
#         elif quadglute[0]!=-1 and quadglute[1]!=-1:
#             indiv_muscle_c+=1
#         else:
#             globV.HCI.printStd("Bug detected in urgencyAdjust. Quads & Glutes are supposed to occur jointly. Exiting...")
#             sys.exit()
        
        pre_len=len(picked_pre)
        
        countDiff=indiv_muscle_c-pre_len
        if countDiff==0:#indiv_muscle_c==pre_len:
            return (picked_pre,indiv_muscle_c)
        elif countDiff>0:#indiv_muscle_c>pre_len:
            #keep up
            picked=picked_pre
            i=0
            while countDiff>0:
                while i<len(self.muscle_workingSet):
                    already_picked=0
                    j=0
                    while j<len(picked):
                    #for j in range(0,len(picked),1):
                        if self.muscle_workingSet[i]==picked[j]:
                            already_picked=1
                            break
                        j+=1
                    if already_picked==0:
                        picked.append(self.muscle_workingSet[i])
                        i+=1
                        break
                    i+=1
                countDiff-=1
                if self.group_by_superset==1:
                    pre_count=len(picked)
                    picked=self.workoutArrange_group_superset(picked)
                    post_count=len(picked)
                    post_diff=post_count-pre_count
                    countDiff-=post_diff
                    if countDiff<0:
                        #now we have to ease-down again. For that we pick one non-superset exercise with the highest credit aka lowest urgency
                        #The case might occur, where all are supersets and we are lying one exercise over the limit. In that case: Fuck it. just leave it like that. We are in a state of highered urgency anyways.
                        picked.sort(key=lambda x: x.muscle_class, reverse=True)
                        picked.sort(key=lambda x: x.urgency, reverse=True)
                        j=len(picked)-1
                        while j>0:
                            supset_check=self._is_supersetMuscle(picked[j])
                            if not supset_check[0]:
                                picked.pop(j)
                                countDiff-=1
                                break
                            j-=1
            return (picked,indiv_muscle_c)
        elif countDiff<0:#indiv_muscle_c<pre_len:
            #ease-down
            picked=[]
            picked_pre.sort(key=lambda x: x.muscle_class, reverse=True)
            picked_pre.sort(key=lambda x: x.urgency, reverse=True)
            final_c=0
            i=0
            bigMuscle_threshold=2
            while i<pre_len:
                if picked_pre[i].muscle_class==1:
                    final_c+=1
                    picked.append(picked_pre.pop(i))
                    pre_len-=1
                else:
                    i+=1
                if final_c>=bigMuscle_threshold:
                    break
    
            picked=self.workoutArrange_group_superset(picked)
            picked_len=len(picked)
            i=0
            while i<len(picked):
            #for i in range(0,len(picked),1):
                j=0
                pre_len=len(picked_pre)
                while j<pre_len:
                    if picked[i]==picked_pre[j]:
                        picked_pre.pop(j)
                        pre_len-=1
                    else:
                        j+=1
                i+=1

            countDiff=pre_len-(indiv_muscle_c-picked_len)#number entries to eliminate
            #This could result in a negative number, unlikely but possible, when already the whole _pre list was taken over to picked. And we do only have Supersets in it. In that case, since we are easing down anyways, remove the Superset with the lowest urgency
            if pre_len==countDiff:
                #already done
                return (picked,indiv_muscle_c)
            elif countDiff<0:
                #remove a superset
                picked.sort(key=lambda x: x.urgency, reverse=True)
                remove=""
                for i in range(0,len(self.supersets)):
                    if picked[len(picked)-1].idx==self.supersets[i][0]:
                        remove=self.superset[i][1]
                        break
                    elif picked[len(picked)-1].idx==self.supersets[i][1]:
                        remove=self.superset[i][0]
                        break
                picked.pop(len(picked)-1)
                i=0
                while i<len(picked):
                #for i in range(0,len(picked)):
                    if remove==picked[i].idx:
                        picked.pop(i)
                        break
                    i+=1
            else:
                #remove, until countDiff==0
                picked_pre.sort(key=lambda x: x.urgency, reverse=True)
#                 for l in range(0,len(picked)):
#                     globV.HCI.printStd("picked: %s"%(picked[l].idx))
                while countDiff>0:
                    if countDiff==1:
                        #Try to remove no superset, if a single exercise does not have a credit very much higher
                        supset_check=self._is_supersetMuscle(picked_pre[len(picked_pre)-1])
                        if not supset_check[0]:
                            picked_pre.pop(len(picked_pre)-1)
                            countDiff-=1
                        else:
                            i=len(picked_pre)-2
                            while i>=0:
                                #globV.HCI.printStd("test %s"%(picked_pre[i].idx))
                                if picked_pre[i].credit>=1+picked_pre[i].malus:#ToDo: Check Credit vs. Urgency
                                    supset_check=self._is_supersetMuscle(picked_pre[i])
                                    if not supset_check[0]:
                                        picked_pre.pop(i)
                                        countDiff-=1
                                        break
                                i-=1
                        if countDiff>0:
                            #Here now, one could do: Remove the highest superset and then add the first non-superset muscle from self.muscle_workingSet
                            #But I say: Fuck it, just leave it like that and train one muscle more this workout
                            break
                    elif countDiff==2:
                        #See if a superset is there to remove
                        i=len(picked_pre)-1
                        while i>=0:
                            supset_check=self._is_supersetMuscle(picked_pre[i])
                            if supset_check[0]:
                                picked_pre.pop(i)
                                countDiff-=1
                                remove=self.supersets[supset_check[1]][1-supset_check[2]]
                                j=0
                                while j<len(picked_pre):
                                #for j in range(0,len(picked_pre)):
                                    if remove==picked_pre[j].idx:
                                        picked_pre.pop(j)
                                        countDiff-=1
                                        break
                                    j+=1
                            if countDiff==0:
                                break
                            i-=1
                        if countDiff>0:#nothing really happened. So we remove just a non-superset exercise
                            picked_pre.pop(len(picked_pre)-1)
                            countDiff-=1
                    else:
                        #just remove one exercise respectively superset with the highest credit
                        supset_check=self._is_supersetMuscle(picked_pre[len(picked_pre)-1])
                        if supset_check[0]:
                            picked_pre.pop(len(picked_pre)-1)
                            countDiff-=1
                            remove=self.supersets[supset_check[1]][1-supset_check[2]]
                            j=0
                            while j<len(picked_pre):
                            #for j in range(0,len(picked_pre)):
                                if remove==picked_pre[j].idx:
                                    picked_pre.pop(j)
                                    countDiff-=1
                                    break
                                j+=1
                        else:
                            picked_pre.pop(len(picked_pre)-1)
                            countDiff-=1
                picked=picked+picked_pre
            #at the very final end, for the case all goes wrong, just do the wooden hammer and try one final time to remove a muscle, which is no superset
            countDiff=len(picked)-indiv_muscle_c
            while countDiff>0:
                i=len(picked)-1
                onlySupset=1
                while i>=0:
                    supset_check=self._is_supersetMuscle(picked[i])
                    if not supset_check[0]:
                        onlySupset=0
                        picked.pop(i)
                        countDiff-=1
                        break
                    i-=1
                if onlySupset==1:
                    break
            return (picked,indiv_muscle_c)
    def _muscle_reappend(self,musIdx):
        for i in range(0,len(self.muscle_workingSet)):
            if self.muscle_workingSet[i].idx==musIdx:
                self.muscle_workingSet.append(self.muscle_workingSet.pop(i))
    def workoutArrange_optimization_smoothen(self,picked_pre,indiv_muscle_c):
        #no delt_rear with rotator_cuff. Precedence to rotator_cuff
        #no delt_front with delt_side -> pop delt_front back
        #maybe no delt_rear with delt_side
        #No Quads&Glutes with lower_back -> pop-back the one with higher credit
        #only when difference in urgency is really big
        #todo
        picked=picked_pre
        replace=0
        
        i=len(picked)-1
        while i>=0:
            if picked[i].idx==muscleID.rotator_cuff.value[0]:
                j=len(picked)-1
                while j>=0:
                    if picked[j].idx==muscleID.delt_rear.value[0]:
                        replace+=1
                        self._muscle_reappend(picked[j].idx)
                        picked.pop(j)
                        if j<i:
                            i-=1
                        break
                    j-=1
            elif picked[i].idx==muscleID.delt_side.value[0]:
                j=len(picked)-1
                while j>=0:
#                     if picked[j].idx=="delt_front":
#                         replace+=1
#                         self._muscle_reappend(picked[j].idx)
#                         picked.pop(j)
#                         if j<i:
#                             i-=1
#                         continue
                    if picked[j].idx==muscleID.delt_rear.value[0]:
                        replace+=1
                        self._muscle_reappend(picked[j].idx)
                        picked.pop(j)
                        if j<i:
                            i-=1
                        break#continue
                    j-=1
            elif picked[i].idx==muscleID.lower_back.value[0]:
                j=len(picked)-1
                while j>=0:
                    if picked[j].idx==muscleID.quads_n_glutes.value[0]:#This assumes that quads and glutes can only occur together. Thus it only checks for one
                        replace+=1
                        if picked[j].urgency<picked[i].urgency:
                            self._muscle_reappend(picked[j].idx)
                            picked.pop(j)
                            if j<i:
                                i-=1
                        else:
                            self._muscle_reappend(picked[i].idx)
                            picked.pop(i)
                        break
                    j-=1
            i-=1
        
        #pop&append the removed ones to self.muscle_workingSet
        #then again self.muscles_assure_rest
        #this makes sure that the add-for-replacement works properly. In the worst case, the removed muscle becomes appended again
        #Version-History: An additional assure_rest is not required any more, since resting muscles are not part of the workingSet
        #self.muscles_assure_rest()
        
        while replace>0:
            for i in range(0,len(self.muscle_workingSet),1):
                already_picked=0
                j=0
                while j<len(picked):
                #for j in range(0,len(picked),1):
                    if self.muscle_workingSet[i]==picked[j]:
                        already_picked=1
                    j+=1
                if already_picked==0:
                    if replace>=2:
                        picked.append(self.muscle_workingSet[i])
                        replace-=1
                        size_pre=len(picked)
                        picked=self.workoutArrange_group_superset(picked)
                        size_post=len(picked)
                        if size_post>size_pre:
                            replace-=1
                    else:
                        supset_check=self._is_supersetMuscle(self.muscle_workingSet[i])
                        if not supset_check[0]:
                            picked.append(self.muscle_workingSet[i])
                            replace-=1
                            break
        return (picked,indiv_muscle_c)
    def workoutArrange_group_superset(self,picked_pre):
        added_new=0
        picked=[]
        set_count=0
        set_found=2
        for j in range(0,len(self.supersets),1):
            pre_len=len(picked_pre)
            i=0
            while i<pre_len:
                if picked_pre[i].idx==self.supersets[j][0]:
                    set_count+=1
                    set_found=0
                    picked.append(picked_pre.pop(i))
                    pre_len-=1
                elif picked_pre[i].idx==self.supersets[j][1]:
                    set_count+=1
                    set_found=1
                    picked.append(picked_pre.pop(i))
                    pre_len-=1
                else:
                    i+=1
            if set_count==1:
                added_new+=1
                if set_found==0:
                    for i in range(0,len(self.muscle_workingSet),1):
                        if self.muscle_workingSet[i].idx==self.supersets[j][1]:
                            picked.append(self.muscle_workingSet[i])
                elif set_found==1:
                    for i in range(0,len(self.muscle_workingSet),1):
                        if self.muscle_workingSet[i].idx==self.supersets[j][0]:
                            picked.append(self.muscle_workingSet[i])
            #elif set_count==2:
                #done. nothing more to do. superset already fully included
            #elif set_count==0:
                #done. nothing more to do. none of this superset is included
            set_count=0
            set_found=2
#         for k in range(0,len(picked),1):
#             globV.HCI.printStd(picked[k].idx)
#         globV.HCI.printStd("")
#         for k in range(0,len(picked_pre),1):
#             globV.HCI.printStd(picked_pre[k].idx)
        if added_new==0:
            #copy over all the rest
            #i=0
            #while i<len(picked_pre):
            #    picked.append(picked_pre.pop(0))
            #    i+=1
            picked=picked+picked_pre
        else:
            picked=picked+picked_pre
        return picked
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def compute_workoutSchedule_nextWorkout_arrange(self,iteration):
        #pick the appropriate muscles to train next workout
        #update history_future
        #In case multiple with the same or very equal urgency exist (more than can be trained with one workout), give precedence to big muscles
        #    Give precedence to big muscles only if the urgency driven selection does not already contain 2 or more big muscles
        #    Then check if inside the tolerance big muscles exist and pick as much until either 2 big muscles are picked or no more big muscles are laying inside the tolerance
        #Update self.schedule of picked with 1 -> Check for all muscles if len of schedule matches i and in case len is too short, append 0
        #Combine Quads & Glutes always together in one workout
        #Give special attention to abs and calves
        #---------------------
        #Calc the individual muscle count for this single workout -> Can diverge by a percentage, depending on the present urgencies
        #First at the very end ease-down or keep-up
        #Maximum +floor(50%) or -floor(30%) -- or maybe do a calculation for two levels of pressure. Low pressure results in 25% deviation and high pressure in 50%
        indiv_muscle_c=self.muscles_per_workout
        
        def _volumeScaling(indiv_muscle_c):
            #It is urgent, to train more, when a +self.muscles_per_workout to the total sum of credits after the current workout does not raise the average over 2
            #On the other hand, we can slack down, when such an increase raises the average over 2+average(all_malus)
            credit_average=0
            malus_ave=0
            bonus_ave=0
            urgency_ave=0
            for i in range(0,len(self.muscle_workingSet)):
                credit_average+=self.muscle_workingSet[i].credit
                malus_ave+=self.muscle_workingSet[i].malus
                bonus_ave+=self.muscle_workingSet[i].bonus
                urgency_ave+=self.muscle_workingSet[i].urgency
            credit_average/=len(self.muscle_workingSet)
            malus_ave/=len(self.muscle_workingSet)
            bonus_ave/=len(self.muscle_workingSet)
            urgency_ave/=len(self.muscle_workingSet)
            #globV.HCI.printStd("AveCred %2.2f | AveUrg %2.2f - %2.2f - %2.2f"%(credit_average,urgency_ave,malus_ave,bonus_ave))
            # if credit_average<=self.credit_center-malus_ave:
            if 1.0<=urgency_ave:
                indiv_muscle_c+=1
                globV.HCI.printStd("Scaling up")
            # elif credit_average>=self.credit_center+bonus_ave-malus_ave:
            elif -0.5>=urgency_ave:
                indiv_muscle_c-=1
                globV.HCI.printStd("Scaling down")
            return indiv_muscle_c
        #
        if cfghandle.cfgh_rt[cfghandle.keyVolScal]:
            indiv_muscle_c=_volumeScaling(indiv_muscle_c)
        
        picked=[]
        for i in range(0,self.muscles_per_workout,1):
            if self.muscle_workingSet[i].muscle_class==1:
                picked.append(self.muscle_workingSet[i])
        picked_big=len(picked)
        if picked_big<2:
            for j in range(self.muscles_per_workout,len(self.muscle_workingSet),1):
                #condition to do the following: The credit of a big muscle minus the precedence_tolerance is lower than the credit of position (last)
                #if self.muscle_workingSet[j].credit-self.muscle_workingSet[indiv_muscle_c-1].credit>=self.bigMuscle_precedence_tolerance:
                if self.muscle_workingSet[indiv_muscle_c-1].urgency-self.muscle_workingSet[j].urgency>=self.bigMuscle_precedence_tolerance:
                    break
                else:
                    if self.muscle_workingSet[j].muscle_class==1:
                        picked.append(self.muscle_workingSet[j])
                        picked_big+=1
                        #globV.HCI.printStd("tolerance %f"%(self.bigMuscle_precedence_tolerance))
                        #globV.HCI.printStd("adding precedence %s"%(self.muscle_workingSet[j].idx))
                if picked_big>=2:
                    break
            #misuse "picked_big" as a counter for "picked_total"
            i=0
            while picked_big<self.muscles_per_workout:
                if self.muscle_workingSet[i].muscle_class==2:
                    picked.append(self.muscle_workingSet[i])
                    picked_big+=1
                elif self.muscle_workingSet[i].muscle_class==1:
                    pass
                else:
                    globV.HCI.printErr("Malformed Muscle Setup (muscle_class aka big vs. small) for %s. Exiting..." % self.muscle_workingSet[i].name)
                    sys.exit()
                i+=1
        else:
            for i in range(0,self.muscles_per_workout,1):
                if self.muscle_workingSet[i].muscle_class==2:
                    picked.append(self.muscle_workingSet[i])
                elif self.muscle_workingSet[i].muscle_class==1:
                    pass
                else:
                    globV.HCI.printErr("Malformed Muscle Setup (muscle_class aka big vs. small) for %s. Exiting..." % self.muscle_workingSet[i].name)
                    sys.exit()
        #
        #self.debug_print_muscleList(picked)
        #Superset-Grouping
        if self.group_by_superset:
            picked=self.workoutArrange_group_superset(picked)
        #some further optimization
        #after superset-grouping and smoothening, ease-down or keep-up, possibly remove muscles from the schedule, while making sure supersets are kept grouped or removed as pair or adding muscles to keep-up in case to much urgency stocked up
        (picked,indiv_muscle_c)=self.workoutArrange_optimization_urgencyAdjust(picked,indiv_muscle_c)
        #make sure that no odd combination of the Deltoids arise, try to combine antagonizing muscles, ...
        (picked,indiv_muscle_c)=self.workoutArrange_optimization_smoothen(picked,indiv_muscle_c)
        #
        #Now assign exercises to the picked muscles
        #-> Herein, both the schedule for the picked muscles and the exercises are updated
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def _updateSchedule_wMatchingExe(matchMuscle,exei,matchingExe):
            matchingExe.schedule.append(matchMuscle.idx)
            #Match all entries of the exercises Intensity-List to the corresponding muscle
            for jintensity in matchingExe.muscleIntensity:
                for jmuscle in self.muscle_groups:
                    if jmuscle.idx==jintensity[0].value[0]:
                        if len(jmuscle.schedule)<iteration:
                            jmuscle.schedule.append(jintensity[1])
                        else:
                            jmuscle.schedule[iteration-1]+=jintensity[1]#iteration==len(jmuscle.schedule)
            #pickedExe.append(matchingExe)
            self.exercise_workingSet.pop(exei)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def _ordinary_pick_firstExercise(matchMuscle):
            next_muscle=False
            for exei, iexercise in enumerate(self.exercise_workingSet):
                for iintensity in iexercise.muscleIntensity:
                    if iintensity[0].value[0]==matchMuscle.idx:
                        if iintensity[1]>=exercise.servingThreshold:# (len(imuscle.schedule)<iteration or imuscle.schedule[iteration-1]<exercise.minimumServing*2/3)
                            _updateSchedule_wMatchingExe(matchMuscle,exei,iexercise)
                            next_muscle=True
                        break
                if next_muscle:
                    break
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        musclesToIntensify=picked[:]
        #pickedExe=[]
        for imuscle in musclesToIntensify:
            _ordinary_pick_firstExercise(imuscle)
        #Add exercises for muscles below minimumServing until exceeded
        while True:
            for index, jmuscle in enumerate(musclesToIntensify):
                if jmuscle.schedule[iteration-1]>exercise.minimumServing:
                    musclesToIntensify.pop(index)
            if 0>=len(musclesToIntensify):
                break
            for imuscle in musclesToIntensify:
                if len(imuscle.schedule)>=iteration and imuscle.schedule[iteration-1]>exercise.minimumServing:#Unlikely, but accumulated small servings of exercises picked for preceding muscles could already exceed the minimumServing
                    continue
                #For every muscle still in the set, here we are now definitively servingThreshold < x <= minimumServing
                #  Try to find an exercise that both brings it close to 1 and does not come too far down in the urgency-sorting
                if imuscle.schedule[iteration-1]<exercise.servingThreshold+0.55*(exercise.minimumServing-exercise.servingThreshold):
                    _ordinary_pick_firstExercise(imuscle)
                else:
                    muscleBoundary=0.5*exercise.muscleStats[imuscle.idx]['count']
                    muscleBoundary=max(muscleBoundary,1)
                    muscleBoundary=min(muscleBoundary,4)
                    foundMatching=0
                    bestDelta=100#Just to have something high
                    for exei, iexercise in enumerate(self.exercise_workingSet):
                        for iintensity in iexercise.muscleIntensity:
                            if iintensity[0].value[0]==imuscle.idx:
                                if iintensity[1]>=exercise.servingThreshold:
                                    wouldResult=imuscle.schedule[iteration-1]+iintensity[1]
                                    desiredTargetDelta=0.5*(1-exercise.minimumServing)
                                    if wouldResult>1-desiredTargetDelta and wouldResult<1+desiredTargetDelta:
                                        foundMatching=1
                                        newDelta=abs(1-wouldResult)
                                        if newDelta<bestDelta:
                                            bestDelta=newDelta
                                            bestMatch=(exei, iexercise)
                                    muscleBoundary-=1
                                break
                        if 0>=muscleBoundary:
                            break
                    if foundMatching:
                        _updateSchedule_wMatchingExe(imuscle,bestMatch[0],bestMatch[1])
                    else:
                        _ordinary_pick_firstExercise(imuscle)
        #
        #update future history aka schedule for remaining muscles and exercises
        for i in range(0,len(self.muscle_groups),1):#Just a Note: Here it is intentionally 'muscle_groups' and not 'only the workingSet'
            if len(self.muscle_groups[i].schedule)<iteration:
                self.muscle_groups[i].schedule.append(0)
        for iexercise in self.exercise_workingSet:
            if len(iexercise.schedule)<iteration:
                iexercise.schedule.append(0)
        for iexercise in self.exercises_excluded:
            if len(iexercise.schedule)<iteration:
                iexercise.schedule.append(0)
    def compute_workoutSchedule_nextWorkout(self,iteration):
        self.muscles_analyse_history()
        self.muscles_analyse_urgency()
        self.muscles_assure_rest()
        ##self.debug_print_credits()
        #self.debug_print_credits_sorted()
        #self.debug_print_urgency_workingSet()
        self.compute_workoutSchedule_nextWorkout_arrange(iteration)
    def compute_workoutSchedule(self):
        #for _ in range(0, 5, 1):
        try:
            for i in range(1, self.num_workout_toCompute+1, 1):
                self.compute_workoutSchedule_nextWorkout(i)
        except IndexError:
            globV.HCI.printErr("Insufficient Exercises. You may want to add some more Equipment-Capabilities.")
            return 1
        return 0
    #------------------------------------------------------------------------------------------
    def workoutScheduling_main(self):
        self.set()
        self.history_read()
        self.history_show_previousWorkoutSchedule_terminal()
        err=self.compute_workoutSchedule()
        if 0==err:
            self.history_show_computedWorkoutSchedule_terminal()
            
            self.push_schedule_toHistory()
            
            if self.history_write_userQuery():
                self.history_write()
        
        self.print_Fin()
#-----------------------------------------------------
