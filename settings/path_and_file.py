#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18

@author: Dennis Krummacker
'''


#-----------------------------------------------------
history_file_subpath="0history"
history_file_bkp_subpath="bkp"
history_file_fExt=".json"
# - - - - - - -
history_file_prefix_muscle="1-"
history_file_fname_muscle="muscle"
history_file_prefix_exercise="2-"
history_file_fname_exercise="exercise"
# - - - - - - -
# Update also this, in case of adding, removing or changing a History-File:
history_files_all={
    history_file_prefix_muscle+history_file_fname_muscle+history_file_fExt,
    history_file_prefix_exercise+history_file_fname_exercise+history_file_fExt
}
#-----------------------------------------------------