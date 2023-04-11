#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
DenKr_workoutScheduler -- 

DenKr_workoutScheduler further description
    - Algorithm to compute a Workout Schedule
    - Implementation in Python (3)
                >>Dennis Krummacker<<

Created on 2020-11-18
                
Notes:
    - 

It defines:
    - 

@author:     Dennis Krummacker

@copyright:  

@license:    license

@contact:    dennis.krummacker@gmail.com
@deffield    updated: 2023-04-09
'''



## System Packages
import sys  # @UnusedImport
# import sysv_ipc  #System V IPC primitives (semaphores, shared memory and message queues) for Python
import signal, time, datetime  # @UnusedImport
# import math
from sys import argv
from builtins import object
#import builtins
#import numpy as numpy
#    numpy.lcm.reduce([40, 12, 20])
#import bz2
# from package.WindowManager_XServer import *  # @UnusedImport @UnusedWildImport
#from pprint import pprint
import random
from itertools import groupby
#import bisect


##DenKr Packages
from package.ansiescape import *  # @UnusedImport @UnusedWildImport
from auxiliary import math  # @UnusedImport @UnusedWildImport


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



if sys.version_info < (3,):#Compatibility, because xrange has changed to range from Python 2.x to 3
    range= xrange  # @UndefinedVariable @ReservedAssignment



##Other Files for Project
##Workout-Scheduler Packages
from muscle import muscle
from exercise import exercise
##Fundamental Project Settings
from settings import VersionInfo
##Regarding Arrangement/Ensemble
from settings.values import muscleIdentifier
##Individual Configuration
from _1cfg.configuration import upcomingOutput_Reverse, workouts_perWeek, num_workout_toCompute
##Global Variables
from settings import global_variables
















        
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
        self.workouts_perWeek=workouts_perWeek
        #self.bigMuscle_precedence_tolerance=7/self.workouts_perWeek-1
        self.num_workout_toCompute=num_workout_toCompute
        self.group_by_superset=1
    def set_phase2(self):
        #self.bigMuscle_precedence_tolerance=self.muscle_groups[0].malus*0.45
        self.bigMuscle_precedence_tolerance=0#Hem, I say, we calc this dynamically for every run on the position, where it is used
        muscles_perWeek_total=0.0
        i=0
        while i<len(self.muscle_groups):
            if self.muscle_groups[i].name!="glutes":#Because we assume that quads and glutes are most of the time trained in conjunction
                muscles_perWeek_total+=self.muscle_groups[i].wo_pW
            i+=1
        self.muscles_per_workout=int(muscles_perWeek_total//self.workouts_perWeek)
        if self.muscles_per_workout!=4:
            print("Attention! A \"muscles_per_workout\" of other than 4 was calculated. You might want to have a look into that (maybe overwrite the value directly, after \"set_phase2()\"). For most cases, 4 muscles per workout is an appropriate amount/value. This tool afterwards allows a reasonable deviation from that anyway to adjust individual workouts to the urgency of muscle groups.")
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def set_exercises(self):
        exercise.set_exercises(self.exercises,self.exercises_excluded)
    def set_muscles(self):
        muscle.set_muscles(self.muscle_groups, self.workouts_perWeek)
        self.supersets=(
            (muscleIdentifier.chest.value[0],muscleIdentifier.back.value[0]),
            (muscleIdentifier.biceps.value[0],muscleIdentifier.triceps.value[0])
        )
    def set(self):
        self.set_basics()
        self.set_muscles()
        self.set_exercises()
        self.set_phase2()
    #------------------------------------------------------------------------------------------
    def history_read(self):
        #[i.history_read_file() for i in self.muscle_groups]
        muscle.history_read_file(self.muscle_groups)
#        #check for consistency
#         name_first=self.muscle_groups[0].idx
#         len_first=len(self.muscle_groups[0].history)
#         for i in range(1,len(self.muscle_groups),1):
#             len_cur=len(self.muscle_groups[i].history)
#             if len_first!=len_cur:
#                 print("Malformed History: Unmatching lenghts. History of muscle \"%s\" is of different length (%d) than of muscle \"%s\" (%d)"%(name_first,len_first,self.muscle_groups[i].idx,len_cur))
        muscle.history_prepare_shortened_all(self.muscle_groups,self.workouts_perWeek)
        exercise.history_read_file(self.exercises,self.exercises_excluded)
        exercise.history_prepare_shortened_all(self.exercises,self.workouts_perWeek)
        exercise.history_prepare_shortened_all(self.exercises_excluded,self.workouts_perWeek)
    def history_write(self):
        #[i.history_write_file() for i in self.muscle_groups]
        muscle.history_write_file(self.muscle_groups)
        exercise.history_write_file(self.exercises,self.exercises_excluded)
    def history_write_userQuery(self):
        inputtry=0
        while 1:
            print("»Shall the history-files be updated with the recent computation?« (y/n)")
            inp=input()
            if inp=="y" or inp=="yes" or inp=="ja" or inp=="j" or inp=="1":
                print("-> »Updating History«")
                #inputtry=3
                return True
            elif inp=="n" or inp=="no" or inp=="nein" or inp=="n" or inp=="0":
                print("-> »NO Update to History«")
                #inputtry=3
                return False
            else:
                print("-> »Invalid Input.",end='')
                inputtry+=1
                if inputtry>=3:
                    print("«\n»Yeah, I propose we just cancel this...«\n")
                    return False
                else:
                    print(" Try again.«\n")
    def push_schedule_toHistory(self):
        muscle.history_push_schedule_all(self.muscle_groups)
        #muscle.history_prepare_shortened_all(self.muscle_groups,self.workouts_perWeek)
        exercise.history_push_schedule_all(self.exercises)
        exercise.history_push_schedule_all(self.exercises_excluded)
        #exercise.history_prepare_shortened_all(self.exercises,self.workouts_perWeek)
    #------------------------------------------------------------------------------------------
    def debug_print_muscles(self,lst,indiv_muscle_c):
        print("Debug - Muscles: (Counter: %d)"%(indiv_muscle_c))
        i=0
        while i<len(lst):
            print(lst[i].name)
            i+=1
        print("")
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
        print("Credits (Ave %2.2f): [ "%(cr_ave),end='')
        for i in range(0,len(printSet)-1,1):
            print("%s:%2.2f, "%(printSet[i].name,printSet[i].credit),end='')
        print("%s:%2.2f"%(printSet[len(printSet)-1].name,printSet[len(printSet)-1].credit),end='')
        print(" ]")
    def debug_print_credits(self):
        cr_ave=0
        for i in range(0,len(self.muscle_groups),1):
            cr_ave+=self.muscle_groups[i].credit
        cr_ave/=len(self.muscle_groups)
        print("Credits (Ave %2.2f): [ "%(cr_ave),end='')
        for i in range(0,len(self.muscle_groups)-1,1):
            print("%s:%2.2f, "%(self.muscle_groups[i].name,self.muscle_groups[i].credit),end='')
        print("%s:%2.2f"%(self.muscle_groups[len(self.muscle_groups)-1].name,self.muscle_groups[len(self.muscle_groups)-1].credit),end='')
        print(" ]")
    def debug_print_credits_workingSet_generic(self,trgtArray):
        cr_ave=0
        for i in range(0,len(trgtArray),1):
            cr_ave+=trgtArray[i].credit
        cr_ave/=len(trgtArray)
        print("WorkingSet[Cred] (Ave %2.2f): [ "%(cr_ave),end='')
        for i in range(0,len(trgtArray)-1,1):
            print("%s:%2.2f, "%(trgtArray[i].name,trgtArray[i].credit),end='')
        print("%s:%2.2f"%(trgtArray[len(trgtArray)-1].name,trgtArray[len(trgtArray)-1].credit),end='')
        print(" ]")
    def debug_print_credits_workingSet_muscle(self):
        self.debug_print_credits_workingSet_generic(self.muscle_workingSet)
    def debug_print_credits_workingSet_exercise(self):
        self.debug_print_credits_workingSet_generic(self.exercise_workingSet)
    def debug_print_urgency_workingSet_generic(self,trgtArray):
        urg_ave=0
        for i in range(0,len(trgtArray),1):
            urg_ave+=trgtArray[i].urgency
        urg_ave/=len(trgtArray)
        print("WorkingSet[Urg] (Ave %2.2f): [ "%(urg_ave),end='')
        for i in range(0,len(trgtArray)-1,1):
            print("%s:%2.2f, "%(trgtArray[i].name,trgtArray[i].urgency),end='')
        print("%s:%2.2f"%(trgtArray[len(trgtArray)-1].name,trgtArray[len(trgtArray)-1].urgency),end='')
        print(" ]")
    def debug_print_urgency_workingSet_muscle(self):
        self.debug_print_urgency_workingSet_generic(self.muscle_workingSet)
    def debug_print_urgency_workingSet_exercise(self):
        self.debug_print_urgency_workingSet_generic(self.exercise_workingSet)
    def debug_print_muscleList(self,mlst):
        lstlen=len(mlst)
        i=0
        while i<lstlen:
            print(mlst[i].name)
            i+=1
        print("")
    #------------------------------------------------------------------------------------------
    def history_trim_trimFiles(self):
        for x in self.muscle_groups:
            x.history=x.history_shortened
        self.history_write()
    def history_trim(self):
        #Trims the history-Files down to a number of entries corresponding to the least required amount (That is, the number of entries a calculation looks back to derive the urgency)
        self.set()
        self.history_read()
        inputtry=0
        while 1:
            print("»History Files Trimming called. Shall I proceed?«")
            print("    (Continue: y / yes / ja / j / 1)")
            print("    (Abort: n / no / nein / 0)")
            inp=input()
            if inp=="y" or inp=="yes" or inp=="ja" or inp=="j" or inp=="1":
                print("-> »Trimming History«")
                self.history_trim_trimFiles()
                return True
            elif inp=="n" or inp=="no" or inp=="nein" or inp=="0":
                print("-> »NOT Trimming History«")
                return False
            else:
                print("-> »Invalid Input.",end='')
                inputtry+=1
                if inputtry>=3:
                    print("«\n»Yeah, Ehem, I propose we just cancel this...«\n")
                    return False
                else:
                    print(" Try again.«\n")
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
                    print("%s - %s"%(imuscle.name,exeForThisMus[0][1].name))
                    if 1<len(exeForThisMus):
                        print(" ",end="")
                        for i in range(1,len(exeForThisMus),1):
                            print("  >& %s"%(exeForThisMus[i][1].name),end="")
                        print("")
            for j in range(len(exeForThisMus)-1,-1,-1):
                scheduled_exe.pop(exeForThisMus[j][0])
                leftEnt-=1
    def _history_show_previousWorkoutSchedule_element(self,exeList,index):
        print("===============")
        print("== Workout t-%d"%(index))
        print("---------------")
        self.__history_show_WorkoutSchedule_element_generic_reverse(exeList,index,"history_shortened")
        print("")
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

        print("######################")
        print("# Previous Workouts: #")
        i=numOutput
        while i>=1:
            self._history_show_previousWorkoutSchedule_element(exeList,i)
            i-=1
        print("#########################################")
        print("#########################################")
        print("#########################################\n")
        pass
    def _history_show_computedWorkoutSchedule_element(self,index):
        scheduled_exe=[]
        scheduled_mus=[]
        for iexercise in self.exercises:
            if 0<iexercise.schedule[index]:
                scheduled_exe.append(iexercise)
        for imuscle in self.muscle_groups:
            if 0<imuscle.schedule[index]:
                scheduled_mus.append(imuscle)
        print("===============")
        #print("== Workout %d"%(i+1))
        print("== DotW, 2023-MM-DD")
        print("---------------")
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
                    print("%s - %s"%(imuscle.name,exeForThisMus[0][1].name))
                    if 1<len(exeForThisMus):
                        print(" ",end="")
                        for i in range(1,len(exeForThisMus),1):
                            print("  >& %s"%(exeForThisMus[i][1].name),end="")
                        print("")
            for j in range(len(exeForThisMus)-1,-1,-1):
                scheduled_exe.pop(exeForThisMus[j][0])
                leftEnt-=1
        print("\n")
    def history_show_computedWorkoutSchedule(self,upcomingOutput_Reverse):
        print("######################")
        print("# Computed Schedule: #  (Reverse-Output: %s)"%(upcomingOutput_Reverse))
        if not upcomingOutput_Reverse:
            i=0
            while i<len(self.muscle_groups[0].schedule):
                self._history_show_computedWorkoutSchedule_element(i)
                i+=1
        elif upcomingOutput_Reverse:
            i=len(self.muscle_groups[0].schedule)-1
            while i>=0:
                self._history_show_computedWorkoutSchedule_element(i)
                i-=1
        else:
            print("Invalid Value given for \"upcomingOutput_Reverse\"")
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
    def muscles_assure_rest(self):
        #ToDo: Use the workouts per Week to determine the number of days between workouts or introduce an additional parameter for this (detailed workout spread across days) to make sure that a muscle has 48-72 h of rest
        #move muscles with no preceeding rest (i.e. was trained last workout) to the end of the list
        i=len(self.muscle_workingSet)-1
        while i>=0:
            joined_history=self.muscle_workingSet[i].history_shortened+self.muscle_workingSet[i].schedule
            hist_len=len(joined_history)
            if hist_len>0:
                if joined_history[hist_len-1]==1:
                    #self.muscle_workingSet.append(self.muscle_workingSet.pop(self.muscle_workingSet.index(5)))
                    #self.muscle_workingSet.append(self.muscle_workingSet.pop(i))
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
#             print("Bug detected in urgencyAdjust. Quads & Glutes are supposed to occur jointly. Exiting...")
#             exit()
        
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
#                     print("picked: %s"%(picked[l].idx))
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
                                #print("test %s"%(picked_pre[i].idx))
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
            if picked[i].idx==muscleIdentifier.rotator_cuff.value[0]:
                j=len(picked)-1
                while j>=0:
                    if picked[j].idx==muscleIdentifier.delt_rear.value[0]:
                        replace+=1
                        self._muscle_reappend(picked[j].idx)
                        picked.pop(j)
                        if j<i:
                            i-=1
                        break
                    j-=1
            elif picked[i].idx==muscleIdentifier.delt_side.value[0]:
                j=len(picked)-1
                while j>=0:
#                     if picked[j].idx=="delt_front":
#                         replace+=1
#                         self._muscle_reappend(picked[j].idx)
#                         picked.pop(j)
#                         if j<i:
#                             i-=1
#                         continue
                    if picked[j].idx==muscleIdentifier.delt_rear.value[0]:
                        replace+=1
                        self._muscle_reappend(picked[j].idx)
                        picked.pop(j)
                        if j<i:
                            i-=1
                        break#continue
                    j-=1
            elif picked[i].idx==muscleIdentifier.lower_back.value[0]:
                j=len(picked)-1
                while j>=0:
                    if picked[j].idx==muscleIdentifier.quads_n_glutes.value[0]:#This assumes that quads and glutes can only occur together. Thus it only checks for one
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
#             print(picked[k].idx)
#         print("")
#         for k in range(0,len(picked_pre),1):
#             print(picked_pre[k].idx)
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
        #It is urgent, to train more, when a +self.muscles_per_workout to the total sum of credits after the current workout does not raise the average over 2
        #On the other hand, we can slack down, when such an increase raises the average over 2+average(all_malus)
        if False:
            credit_average=0
            malus_ave=0
            bonus_ave=0
            for i in range(0,len(self.muscle_workingSet)):
                credit_average+=self.muscle_workingSet[i].credit
                malus_ave+=self.muscle_workingSet[i].malus
                bonus_ave+=self.muscle_workingSet[i].bonus
            credit_average/=len(self.muscle_workingSet)
            malus_ave/=len(self.muscle_workingSet)
            bonus_ave/=len(self.muscle_workingSet)
            #print("Aves %2.2f - %2.2f - %2.2f"%(credit_average,malus_ave,bonus_ave))
            if credit_average>=self.credit_center+bonus_ave-malus_ave:
                indiv_muscle_c-=1
                print("Scaling down")
            elif credit_average<=self.credit_center-malus_ave:
                indiv_muscle_c+=1
                print("Scaling up")
        
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
                        #print("tolerance %f"%(self.bigMuscle_precedence_tolerance))
                        #print("adding precedence %s"%(self.muscle_workingSet[j].idx))
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
                    print("Malformed Muscle Setup (muscle_class aka big vs. small) for %s. Exiting..." % self.muscle_workingSet[i].name)
                    exit()
                i+=1
        else:
            for i in range(0,self.muscles_per_workout,1):
                if self.muscle_workingSet[i].muscle_class==2:
                    picked.append(self.muscle_workingSet[i])
                elif self.muscle_workingSet[i].muscle_class==1:
                    pass
                else:
                    print("Malformed Muscle Setup (muscle_class aka big vs. small) for %s. Exiting..." % self.muscle_workingSet[i].name)
                    exit()
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
                    if jmuscle.idx==jintensity[0]:
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
                    if iintensity[0]==matchMuscle.idx:
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
                            if iintensity[0]==imuscle.idx:
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
        for i in range(1, self.num_workout_toCompute+1, 1):
            self.compute_workoutSchedule_nextWorkout(i)
    #------------------------------------------------------------------------------------------
    def workoutScheduling_main(self,upcomingOutput_Reverse):
        self.set()
        self.history_read()
        self.history_show_previousWorkoutSchedule()
        self.compute_workoutSchedule()
        self.history_show_computedWorkoutSchedule(upcomingOutput_Reverse)
        
        self.push_schedule_toHistory()
        
        if self.history_write_userQuery():
            self.history_write()
        
        print("\nFin.\nGood Success with your endeavours.\n")
        print("P.S.: Oh yeah, and remember to always do your fucking »Facepull«! ;oD")
        print("      And don't forget your »YTWL«...\n")
#-----------------------------------------------------






#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
## Approach 1
#-----------------------------------------------------

def DenKr_workoutScheduler_Main():
    err=0  # @UnusedVariable
    global global_var
    
    #make sure to have enough rest (no training on directly preceeding workouts)
    #calculate the inverse -> perWorkout (malus)
    #compare to history up to when it was 2 times trained
    #A muscle shall have a "credit" higher than 2. It looses its malus every workout it is not trained and gains +1 for every time it is trained
    
    #TODO Extension: One could check (inside smoothening or urgencyAdjust or assureRest or at general picking) for severe overtraining. See whether an included muscles credit would land double the bonus over the centerCredit. But this case shouldn't really arise in the current approach (by the numMusclePerWorkout calculation and the restricted history analysis)
    work=workout()
    work.workoutScheduling_main(upcomingOutput_Reverse)
    
    return 0

#------------------------------------------------------------------------------------------

def main_variant1():
    #ToDo: Allow to specify how much muscle-groups shall be trained per workout. (Currently it just uses 4 with sometimes 5, when a lot is pressing)
    #ToDo: Use the sets_perWeek
    #ToDo: User input query about Decision, if predefined Super-Sets shall be created (e.g. Chest always together with Back) or if all muscle groups are just treated completely individual and independent
    #ToDo: User input query whether the history shall be updated or not
    #ToDo: Display the previous 6 workouts (read from history), then calculate the upcoming 6 and display them, then the query about updating history
    #TODO: Teste die Sinnhaftigkeit des konkreten Wertes by self.bigMuscle_precedence_tolerance
    #ToDo: Eventuell "Facepull" als "eigenen Muskel" ergänzen, damit er häufig eingeplant wird. Dieser dann eventuell "on top"? Also bei solchen Workouts eine Übung mehr?
    #    -> Think about a thorough 'explicit' integration of YTWL
    #ToDo: For smoothening, a more sophisticated consideration of "related small & big muscle groups". That is, not combining small muscles together with big muscles, where compound-movements for the big muscle also attacks the small muscle. E.g. don't combine the front-delt in one workout with the chest
    #Optional, eher nicht: Add Scale_Up & Scale_Down again. Mag Sinn ergeben, um die Credits besser auszuglätten. Vielleicht aufeinander bezogen -> Wenn einmal up-scaled wurde den threshold verringern, welcher die kommenden Workouts down_scaled. Damit mag sich ergeben, dass ein workout mal ein (oder zwei) Muskeln mehr trainiert, wenn sie dringend anliegen und man dann ein kommendes Workout etwas kürzer gestalten kann. (Kann einerseits sinnvoll sein, um solche Muskelgruppen nicht zu lange zu pausieren und dann zu schnell aufeinander zwei Mal trainiert. Ist aber andererseits auch wieder dämlich, weil dann einzelne Workouts zu lang werden, was schlecht für das Testo-Level ist...)
    err=0  # @UnusedVariable
    #print("Call it with Python 3.7 or higher! This requires order-preserving dictionaries.")
    print("DenKr_workoutScheduler (v. %s)"%(VersionInfo.VERSION_DESCRIPTION))
    print(" (Path of Script: %s) [Here, the History is stored]"%(global_variables.progPath))
    print("")
    print("It calculates a progressing schedule for your resistance-training workout, i.e. tells you in which order you may train your muscle-groups.")
    print("In the files \"./_1cfg/configuration.py\" & \"./_1cfg/setup.py\" you may define your demands. That is, how many workouts you intend to do per week and how often per week individual muscles shall be attacked; as well as which types of exercises you want (in terms of required equipment) or the individual exercises themselves.")
    print("The default should provide a solid setup for most people up to advanced. However, if you are very advanced you may need to adjust the volume and for sure your total workouts per week.")
    print("The tool stores the calculated schedule as a history in text-files and loads them during a run, to maintain a consistant suitable flow. After startup you are first told (again) the last loaded workouts, then the new ones are presented on the terminal.")
    print("Before writing the history (i.e. appending the newly computed workouts), you are prompted a query on the console whether the persistent history files shall be updated or not. You can use this to just lookup the last preceding computation without creating a new one and unintentionally messing with the history files.")
    print("\n--------------------------------\n")
    print("This Workout-Scheduler has as baseline the assumption, that you work-out every second day (i.e. 3.5 times a week) and are with that able to attack the big muscles twice a week, the smalls once and abs & calves thrice in two weeks.")
    print("This scales very well if you adjust the total-workouts-per-week value and the workouts_perMuscle_perWeek to for instance attack them more fequently or with a higher volume in case you are more advanced.")
    print("You might want to use a workaround if you intend to work-out below the recommended baseline volume:")
    print("You could work with the default-values but work-out less frequently than every second day. By that, you are still attacking all muscles nicely proportoned but are leaving some extra gains because over surpluss regeneration.")
    print("\nWhat you still got to do: Pay attention to your back! Spread the work appropriately to all these different muscles on your back. This tool will only tell you to 'train your back/back-delts/lower-back'. As you know, there is a lot more. Rotator-Cuff, Teres major, Teres Minor, Infraspinatus, Supraspinatus and whatnot. Hence you have to decide to train a Deadlift, Facepull, Y- or W-movement and stuff to hit all the muscles back frequently. Use the workout recommendation for 'back/lower-back/back-delt/trapez' to choose exercises to complete all the back.")
    print("That is, of course, pretty much valid for all muscle groups. You are to fiddle around a little with the schedule recommendation of this tool.")
    print("Another Tipp: In times, when you are proposed a smaller workout - only 3 muscles or so - you may want to fill the hole with something beneficial instead of just stopping the workout early. Fill in an additional session of facepulls for example. Do some external rotation exercise. Hit some back shoulder / back muscles, which could use some additional training. Do some isolated lower-back movement, like bend down to hyper-extension. There's always something to do.")
    print("")
    print("Reverse Output:")
    print("Watch out for the Variable 'upcomingOutput_Reverse' inside the file './1cfg/configuration.py'.")
    print("Set this to '0' to print out the computed Workout-Schedule with rising number (Starting with Workout-1, going up to Workout-n).")
    print("Set it to '1' to print the Schedule 'reverse', i.e. with falling number (Starting with Workout-n, going down to Workout-1).")
    print("")
    print("Workout-Notation:")
    print("• When 'one exercise' is denotet in the form of actually two exercises, joined by \"->\", this specifies a \"Compund-Superset\".")
    print("  This means: Perform both exercises in direct succession without any break. You may give the first exercise like 60-80% of your power and finish off with the second; or perform the first nearly up to exhaustion and then use the second to finish towards nearly failure.")
    print("• You may also be proposed multiple distinct exercises. Denoted as \">&\". This happens, when a muscle shall be trained in the workout but the primarily picked exercise does not bring sufficient intensity. Then additional exercises are added.")
    print("  So you do all exercises, but more separated and not as rapid Superset. (Albeit doing as Superset would actually also be fine...)")
    print("")
    print("")
    err=DenKr_workoutScheduler_Main()
    return err
#------------------------------------------------------------------------------------------




#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
## Approach 2
#-----------------------------------------------------


def logfilewrite(aDirectionstring, aLinestring):
    global LogFile
    if not LogFile is None:
        LogFile.write(str(datetime.datetime.now().time()) + "\t" + aDirectionstring + "\t" + aLinestring + "\n")
        LogFile.flush()

#------------------------------------------------------------------------------------------

def ExampleMoreComplex_PythonDummy_Main():
    return 0

def main_variant2():
    LogFile = open("./logFileExample.txt", mode="w")
    
    err=ExampleMoreComplex_PythonDummy_Main()

    LogFile.close()
    return err
#------------------------------------------------------------------------------------------






#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
## Basic Stuff
#-----------------------------------------------------

def signal_handler__Ctrl_c(sig, frame):
    print('You pressed Ctrl+C!')
    LogFile.close()
    sys.exit(0)

#Return:
#  0 - No Arguments. Continue normal operation
#  1 - Cmd-Line Mux did all the work. Terminate
#  2 - Invalid Cmd-Line Arguments
#  3 - Reserved
def cmdLine_Mux(argc,argv):
    # todo
    if 0>=argc:
        return 0
    else:
        argc-=1
        curArg=0
        if argv[curArg]=="history":
            if 0<argc:
                argc-=1
                curArg+=1
                if argv[curArg]=="trim":
                    work=workout()
                    work.history_trim()
                    return 1
                else:
                    print("-> Invalid Cmd-Line Argument after \"trim\".")
                    return 2
            else:
                print("-> Insufficient Cmd-Line Arguments after \"trim\".")
                return 2
        else:
            print("-> Invalid Cmd-Line Argument.")
            return 2
def cmdLine_Mux__errHandling(argc,argv):
    err=cmdLine_Mux(argc,argv)
    if 0==err:
        pass
    elif 1==err:
        print("\nDone.")
        print(sys.exit())
    elif 2==err:
        print("\nExiting...")
        print(sys.exit())
    else:
        print(sys.exit())

#------------------------------------------------------------------------------------------

def main(argc,argv):
    SET_ansi_escape_use()
    #printansi(ansi_blue,"""I can even use colors!\n""")
    # - - - - - - - - -
    cmdLine_Mux__errHandling(argc,argv)
    # - - - - - - - - -
    err=main_variant1()
    #err=main_variant2()
    return err


if __name__ == '__main__':
    signal.signal(signal.SIGINT,signal_handler__Ctrl_c)
    #print('Number of arguments:',len(argv),'arguments.')
    #print('Argument List:',str(argv))
    argc = len(sys.argv)-1
    argv=sys.argv[1:]
    # - - - - - - - - -
    #global progPath # Declared in ./settings/global_variables and importet
    #print('sys.argv[0] =', sys.argv[0])
    global_variables.set_ProgramPath(__file__)
    # - - - - - - - - -
    main(argc,argv)
