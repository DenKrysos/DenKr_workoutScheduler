#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-14

@author: Dennis Krummacker
'''

import os
import shutil


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV


def remove_pycache(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for dirname in dirnames:
            if dirname=='__pycache__':
                pycache_path=os.path.join(dirpath, dirname)
                globV.HCI.printStd(f'Removing: {pycache_path}')
                shutil.rmtree(pycache_path)