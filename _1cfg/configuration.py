#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-09

@author: Dennis Krummacker
'''
###############################################
###   Dev-Notes                 ###############
###   (irrelevant for users)    ###############
#==============================================
# The Config-Strucute, used internally in the app is created in "./settings/config_handler.py"
# -> Adjust this as well, in case config-variables change, are added or removed.
#==============================================
#
###############################################
###   Required Imports      ###################
###   (just leave alone)    ###################
#==============================================
from settings.values import equipID, useMeth
#==============================================




###############################################
###   Usage-Methodology                ########
###   (how do you wish to interface?)  ########
#==============================================
# Valid Values (see "./settings/values.py"):
#    .Terminal
#    .GUI
usageMethodology=useMeth.GUI
#==============================================




###############################################
###   Formatting-Settings            ##########
###   (for formatting the Output)    ##########
#==============================================
upcomingOutput_Reverse=False
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
    equipID.Bodyweight:True,
    equipID.Sling:True,
    equipID.ResistanceBand:True,
    equipID.Dumbbell:True,
    equipID.Barbell:False,
    equipID.PullUpBar:True,
    equipID.SimpleBench:False,# A simple Bench/Step, something where you can lie on to elevate your body and have your arms free to go deeper than your body
    equipID.MountBench:False,# A sophisticated Bench with a mount attached for a barbell
    equipID.CablePull:False,
    equipID.Gym:False
}
#==============================================