#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2020-11-18
Last Update: 2023-04-16

@author: Dennis Krummacker
'''



##Other Files for Project
##Fundamental Project Settings
from settings import VersionInfo
##Regarding Arrangement/Ensemble
from settings.path_and_file import (
    config_file_subpath,
    config_file_fExt,
    config_file_prefix,
    config_file_fname
)
##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV



#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
## Basic Stuff
#-----------------------------------------------------
def print_introduction():
    #globV.HCI.printStd("Call it with Python 3.7 or higher! This requires order-preserving dictionaries.")
    globV.HCI.printStd("DenKr_workoutScheduler (v. %s)"%(VersionInfo.VERSION_DESCRIPTION))
    #globV.HCI.printStd(" (Path of Script: %s) [Here, the History is stored]"%(globV.progPath))
    globV.print_progPath()
    globV.HCI.printStd("")
    globV.HCI.printStd("It calculates a progressing schedule for your resistance-training workout, i.e. tells you in which order you may train your muscle-groups.")
    globV.HCI.printStd("The tool can be vastly configured to suit your demands. That is, how many workouts you intend to do per week and how often per week individual muscles shall be attacked; as well as which types of exercises you want (in terms of required equipment) or the individual exercises themselves. Furthermore, more minor configurations are supported, like adjusting the output format.")
    globV.HCI.printStd("In the files \"./_1cfg/configuration.py\" & \"./_1cfg/setup.py\" come the default values. Actually, values from '.json' files from the directory \"./0history\" are taken. From the onset, the .json files don't exist but are created/updated on each successful run. Missing files/values are initiated with values from the default-delivering .py files.")
    globV.HCI.printStd("The default should provide a solid setup for most people up to advanced. However, if you are very advanced you may need to adjust the volume and for sure your total workouts per week.")
    globV.HCI.printStd("The tool stores the calculated schedule as a history in text-files and loads them during a run, to maintain a consistant suitable flow. After startup you are first told (again) the last loaded workouts, then the new ones are presented on the terminal.")
    globV.HCI.printStd("Before writing the history (i.e. appending the newly computed workouts), you are prompted a query on the console whether the persistent history files shall be updated or not. You can use this to just lookup the last preceding computation without creating a new one and unintentionally messing with the history files.")
    globV.HCI.printStd("\n--------------------------------\n")
    globV.HCI.printStd("This Workout-Scheduler has as baseline the assumption, that you work-out every second day (i.e. 3.5 times a week) and are with that able to attack the big muscles twice a week, the smalls once and abs & calves thrice in two weeks.")
    globV.HCI.printStd("This scales very well if you adjust the total-workouts-per-week value and the workouts_perMuscle_perWeek to, for instance, attack them more fequently or with a higher volume in case you are more advanced.")
    globV.HCI.printStd("You might want to use a workaround if you intend to work-out below the recommended baseline volume:")
    globV.HCI.printStd("You could work with the default-values but work-out less frequently than every second day. By that, you are still attacking all muscles nicely proportoned but are leaving some extra gains because over surpluss regeneration.")
    globV.HCI.printStd("")
    globV.HCI.printStd("What you still got to do: Pay attention to your bigger muscle-groups, like your back! Spread the work appropriately to all these different muscles on your back. Some exercises you are proposed for your 'back/back-delts/lower-back/...' can be performed in variation to shift the intensity focus. As you know, there is a lot more than just 'Back' or 'Rotator-Cuff'. Teres major, Teres Minor, Infraspinatus, Supraspinatus and whatnot. Hence you are recommended to think along and decide how you precisely execute an exercise to hit all the single muscles and train them evenly.")
    globV.HCI.printStd(" Tl;dr: Use the workout recommendation to get the Muscle-groups and Exercises to do but feel free to vary the execution in order to fully hit all single muscles with equal intensity. That is, of course, pretty much valid for all muscle groups. You are to fiddle around a little with the schedule recommendation of this tool.")
    globV.HCI.printStd("Another Tipp: In times, when you are proposed a smaller workout - only 3 muscles or so - you may want to fill the hole with something beneficial instead of just stopping the workout early. Fill in an additional session of facepulls for example. Do some external rotation exercise. Hit some back shoulder / back muscles, which could use some additional training. Do some isolated lower-back movement, like bend down to hyper-extension. There's always something to do.")
    globV.HCI.printStd("")
    globV.HCI.printStd("Reverse Output:")
    globV.HCI.printStd("Watch out for the Variable 'upcomingOutput_Reverse' inside the file \"./_1cfg/configuration.py\".")
    globV.HCI.printStd("Set this to '0' to print out the computed Workout-Schedule with rising number (Starting with Workout-1, going up to Workout-n).")
    globV.HCI.printStd("Set it to '1' to print the Schedule 'reverse', i.e. with falling number (Starting with Workout-n, going down to Workout-1).")
    globV.HCI.printStd("")
    globV.HCI.printStd("GUI:")
    globV.HCI.printStd(f"In case, you are working on terminal now, but like to use the GUI, open the File \"./{config_file_subpath}/{config_file_prefix+config_file_fname+config_file_fExt}\" and change 'UsageMethodology' to \"useMeth.GUI\".")
    globV.HCI.printStd("")
    globV.HCI.printStd("Workout-Notation:")
    globV.HCI.printStd("• When 'one exercise' is denotet in the form of actually two exercises, joined by \"->\", this specifies a \"Compound-Superset\".")
    globV.HCI.printStd("  This means: Perform both exercises in direct succession without any break. You may give the first exercise like 60-80% of your power and finish off with the second; or perform the first nearly up to exhaustion and then use the second to finish towards nearly failure.")
    globV.HCI.printStd("• You may also be proposed multiple distinct exercises. Denoted as \">&\". This happens, when a muscle shall be trained in the workout but the primarily picked exercise does not bring sufficient intensity. Then additional exercises are added.")
    globV.HCI.printStd("  So you do all exercises, but more separated and not as rapid Superset. (Albeit doing as Superset would actually also be fine...)")
    globV.HCI.printStd("")
    globV.HCI.printStd("")
#------------------------------------------------------------------------------------------
