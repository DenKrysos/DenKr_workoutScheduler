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
import DenKr_essentials_py.importMe_fundamental  # @UnusedImport


## System Packages
import sys  # @UnusedImport
import os
# import sysv_ipc  #System V IPC primitives (semaphores, shared memory and message queues) for Python
import signal
#import time
import datetime
# import math
#import builtins
#import numpy as numpy
#    numpy.lcm.reduce([40, 12, 20])
#import bz2
# from DenKr_essentials_py.WindowManager_XServer import *  # @UnusedImport @UnusedWildImport
#from pprint import pprint

## Installation / exe-Packaging
# Currently, I recommend using PyInstaller
#    pip install -U pyinstaller
#    pyinstaller DenKr_workoutScheduler_main.py




##DenKr Packages
from DenKr_essentials_py.ansiescape import *  # @UnusedImport @UnusedWildImport
from auxiliary import math  # @UnusedImport @UnusedWildImport
from DenKr_essentials_py.cmdLine import cmdLine_Mux
from DenKr_essentials_py.order_tidyness import remove_pycache
from DenKr_essentials_py.dependency_management import assure_dependencies
from auxiliary.config_handling import configHandle_setup
from commonFeatures.bits_and_pieces import print_introduction
##GUI
from GUI.GUI_tkinter import DKWoSched_GUI


##Other Files for Project
##Workout-Scheduler Packages
from workoutScheduler.workout import workout
##Regarding Arrangement/Ensemble
from settings.values import useMeth
from settings.path_and_file import (
    requirements_path,
    requirements_fName_plain,
    requirements_fName_GUI,
)
##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV
##Individual Configuration
import settings.config_handler as cfghandle



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# REFERENCES / Online RESOURCES
#
# Online Interpreter to quickly Test stuff:
#   https://www.programiz.com/python-programming/online-compiler/





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
    configHandle_setup()
    if useMeth.Terminal==cfghandle.cfgh_rt[cfghandle.keyUseMeth]:
        assure_dependencies(os.path.join(globV.inherentDataFilePath,requirements_path),requirements_fName_plain)
        print_introduction()
        err=DenKr_workoutScheduler_Main()
        return 0
    elif useMeth.GUI==cfghandle.cfgh_rt[cfghandle.keyUseMeth]:
        assure_dependencies(os.path.join(globV.inherentDataFilePath,requirements_path),requirements_fName_GUI)
        GUI_instance=DKWoSched_GUI()  # @UnusedVariable
        return 0
    else:
        globV.HCI.printErr("Invalid Value configured for \"usageMethodolgy\" in \"./_1cfg/configuration.py\".")
        globV.HCI.printErr("   -> Terminating...")
        return 2
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
#  2 - Insufficient Number of Arguments
#  3 - Invalid Cmd-Line Arguments
#  4 - Reserved
class cmdLine_Mux_DKWOSched(cmdLine_Mux):
    #------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __del__(self):
        super().__del__()
    #------------------------------------------------------------------------------------------
    def cmdLine_Mux(self):
        # todo
        if 0>=self.targc:
            return 0
        else:
            if self.argv[self.curArg]=="history":
                err=self.cmdLine_Mux__oneLevelDeeper("history")
                if err:
                    return err
                if self.argv[self.curArg]=="trim":
                    work=workout()
                    work.history_trim_query()
                    return 1
                else:
                    globV.HCI.printStd(f"-> Invalid Cmd-Line Argument after \"trim\": \'{self.argv[self.curArg]}\'")
                    return 3
            elif self.argv[self.curArg]=="clear":
                err=self.cmdLine_Mux__oneLevelDeeper("clear")
                if err:
                    return err
                if self.argv[self.curArg]=="pycache":
                    remove_pycache(globV.progPath)
                    return 1
                else:
                    globV.HCI.printStd(f"-> Invalid Cmd-Line Argument after \"pycache\": \'{self.argv[self.curArg]}\'")
                    return 3
            else:
                globV.HCI.printStd(f"-> Invalid Cmd-Line Argument: \'{self.argv[self.curArg]}\'")
                return 3
    #------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------

def main(args):
    SET_ansi_escape_use()
    #printansi(ansi_blue,"""I can even use colors!\n""")
    # - - - - - - - - -
    args.cmdLine_Mux__errHandling()
    # - - - - - - - - -
    err=main_variant1()
    #err=main_variant2()
    return err


if __name__ == '__main__':
    signal.signal(signal.SIGINT,signal_handler__Ctrl_c)
    args=cmdLine_Mux_DKWOSched()
    # - - - - - - - - -
    #global progPath # Declared in ./settings/global_variables and importet
    #globV.HCI.printStd('sys.argv[0] =', sys.argv[0])
    globV.set_ProgramPath(__file__)
    # - - - - - - - - -
    main(args)
