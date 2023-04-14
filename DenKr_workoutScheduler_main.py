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


## Some Fundamentals
import package.importMe_fundamental  # @UnusedImport


## System Packages
import sys  # @UnusedImport
# import sysv_ipc  #System V IPC primitives (semaphores, shared memory and message queues) for Python
import signal
#import time
import datetime
# import math
from sys import argv
#import builtins
#import numpy as numpy
#    numpy.lcm.reduce([40, 12, 20])
#import bz2
# from package.WindowManager_XServer import *  # @UnusedImport @UnusedWildImport
#from pprint import pprint




##DenKr Packages
from package.ansiescape import *  # @UnusedImport @UnusedWildImport
from auxiliary import math  # @UnusedImport @UnusedWildImport


##Other Files for Project
##Workout-Scheduler Packages
from workoutScheduler.workout import workout
##Fundamental Project Settings
from settings import VersionInfo
##Global Variables
from settings import global_variables





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
    work.workoutScheduling_main()
    
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
    print("")
    print("What you still got to do: Pay attention to your bigger muscle-groups, like your back! Spread the work appropriately to all these different muscles on your back. Some exercises you are proposed for your 'back/back-delts/lower-back/...' can be performed in variation to shift the intensity focus. As you know, there is a lot more than just 'Back' or 'Rotator-Cuff'. Teres major, Teres Minor, Infraspinatus, Supraspinatus and whatnot. Hence you are recommended to think along and decide how you precisely execute an exercise to hit all the single muscles and train them evenly.")
    print(" Tl;dr: Use the workout recommendation to get the Muscle-groups and Exercises to do but feel free to vary the execution in order to fully hit all single muscles with equal intensity. That is, of course, pretty much valid for all muscle groups. You are to fiddle around a little with the schedule recommendation of this tool.")
    print("Another Tipp: In times, when you are proposed a smaller workout - only 3 muscles or so - you may want to fill the hole with something beneficial instead of just stopping the workout early. Fill in an additional session of facepulls for example. Do some external rotation exercise. Hit some back shoulder / back muscles, which could use some additional training. Do some isolated lower-back movement, like bend down to hyper-extension. There's always something to do.")
    print("")
    print("Reverse Output:")
    print("Watch out for the Variable 'upcomingOutput_Reverse' inside the file \"./_1cfg/configuration.py\".")
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
                    work.history_trim_query()
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
