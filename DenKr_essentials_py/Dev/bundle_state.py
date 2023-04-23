#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-19

@author: Dennis Krummacker
'''

#System Packages
import sys





def check_whether_executedAsExe():
    '''
    Returns whether it is running as a "Bundled Executable" (when packed with 'PyInstaller').
    From "PyInstaller-Doc":
    When a bundled app starts up, the bootloader sets the sys.frozen attribute and stores the absolute path to the bundle folder in sys._MEIPASS.
    For a one-folder bundle, this is the path to that folder.
    For a one-file bundle, this is the path to the temporary folder created by the bootloader.
    '''
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # The app is running as an exe
        # print(getattr(sys,'frozen'))
        # print(sys.executable)
        # app_path=os.path.dirname(sys.executable)
        # print(f"App path (Exe): {app_path}")
        return True
    else:
        # The app is running from a Python interpreter
        # app_path=os.path.dirname(os.path.abspath(__file__))
        # print(f"App path (Interpreted-Script): {app_path}")
        return False
