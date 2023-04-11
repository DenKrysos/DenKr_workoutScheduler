#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-09

@author: Dennis Krummacker
'''
###############################################
###   Required Imports      ###################
###   (just leave alone)    ###################
#==============================================
from settings.values import equipmentIdentifier
#==============================================




###############################################
###   Formatting-Settings            ##########
###   (for formatting the Output)    ##########
#==============================================
upcomingOutput_Reverse=True
#==============================================




##################################################
###   Computation-Configuration               ####
###   (influences the Schedule-Computation)   ####
#=================================================
#- How often you intent to workout per week. DEFAULT: 3.5
workouts_perWeek=3.5
#- How many Workouts shall be computet per run. DEFAULT: int(workouts_perWeek*2)
num_workout_toCompute=int(workouts_perWeek*2)
#=================================================




######################################################################
###   Equipment-Capabilities                                     #####
###   (for you to adjust which Equipment you have at disposal)   #####
#=====================================================================
exercisesToInclude={
    equipmentIdentifier.Bodyweight.value[0]:True,
    equipmentIdentifier.Sling.value[0]:True,
    equipmentIdentifier.ResistanceBand.value[0]:True,
    equipmentIdentifier.Dumbbell.value[0]:True,
    equipmentIdentifier.Barbell.value[0]:False,
    equipmentIdentifier.PullUpBar.value[0]:True,
    equipmentIdentifier.SimpleBench.value[0]:False,# A simple Bench/Step, something where you can lie on to elevate your body and have your arms free to go deeper than your body
    equipmentIdentifier.MountBench.value[0]:False,# A sophisticated Bench with a mount attached for a barbell
    equipmentIdentifier.CablePull.value[0]:False,
    equipmentIdentifier.Gym.value[0]:False
}
#==============================================