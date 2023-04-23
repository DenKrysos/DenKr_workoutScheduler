#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18

@author: Dennis Krummacker
'''

#=======================================================
# in case of adding, removing or changing a History- or persistent Config-File:
#  --> Look at the very bottom of this file
#=======================================================



#-----------------------------------------------------
history_file_subpath="0history"
history_file_bkp_subpath="bkp"
history_file_fExt=".json"
# - - - - - - -
history_file_prefix_muscle="2_1-"
history_file_fname_muscle="muscle"
history_file_prefix_exercise="2_2-"
history_file_fname_exercise="exercise"
#-----------------------------------------------------




#-----------------------------------------------------
config_file_subpath=history_file_subpath
config_file_fExt=".json"
# - - - - - - -
config_file_prefix="1_1-"
config_file_fname="config"
configSetup_file_prefix="1_2-"
configSetup_file_fname="config_setup"
#-----------------------------------------------------





#-----------------------------------------------------
requirements_fName_plain="requirements_plain.txt"
requirements_fName_GUI="requirements_GUI.txt"
requirements_path="settings"
#-----------------------------------------------------





#-----------------------------------------------------
Executable_Name="DenKr_workoutScheduler"
#-----------------------------------------------------





#-----------------------------------------------------
# Update also this, in case of adding, removing or changing a History- or persistent Config-File:
history_files_all={
    history_file_prefix_muscle+history_file_fname_muscle+history_file_fExt,
    history_file_prefix_exercise+history_file_fname_exercise+history_file_fExt,
    config_file_prefix+config_file_fname+config_file_fExt,
    configSetup_file_prefix+configSetup_file_fname+config_file_fExt
}
#-----------------------------------------------------