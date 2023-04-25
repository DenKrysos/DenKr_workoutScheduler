#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-24

@author: Dennis Krummacker
'''

import copy


##Workout-Scheduler Packages
from auxiliary.config_handling import configHandle_dumpPersistent, configHandle_readPersistent
##Fundamental Project Settings
from settings.path_and_file import (
    GUI_cfg_file_path,
    GUI_cfg_file_prefix,
    GUI_cfg_file_fName,
    GUI_cfg_file_fExt
)




#--------------------------------------------------------------------------
class KEY_GUICfgH:
    RetainGeometry="retainGeometry"
    SizeX="sizeX"
    SizeY="sizeY"
    PosX="posX"
    PosY="posY"
#--------------------------------------------------------------------------




def secure_window_geometry(GUIObj, sizeX,sizeY, posX,posY):
    GUIObj.taskbarheight=75
    sizeX=min(sizeX,GUIObj.screenX)
    sizeY=min(sizeY,GUIObj.screenY-GUIObj.taskbarheight)
    posX=max(posX,0)
    posY=max(posY,0)
    screenSafetyPadding=75
    posX=min(posX,GUIObj.screenX-screenSafetyPadding)
    posY=min(posY,GUIObj.screenY-screenSafetyPadding)
    return sizeX,sizeY,posX,posY


def window_pos_center(GUIObj, sizeX,sizeY):
    posX=GUIObj.screenX//2-sizeX//2
    posY=(GUIObj.screenY-GUIObj.taskbarheight)//2-sizeY//2
    return posX,posY








def GUIflush_runtime_to_cfghandle(GUIObj):
    GUIObj.cfgHandle=copy.deepcopy(GUIObj.cfgHandle_rt)

def GUIwriteBack_cfghandle_to_runtime(GUIObj):
    GUIObj.cfgHandle_rt=copy.deepcopy(GUIObj.cfgHandle)


def carryOver_windowGeometry(dst,src):
    dst[KEY_GUICfgH.SizeX]=src[KEY_GUICfgH.SizeX]
    dst[KEY_GUICfgH.SizeY]=src[KEY_GUICfgH.SizeY]
    dst[KEY_GUICfgH.PosX]=src[KEY_GUICfgH.PosX]
    dst[KEY_GUICfgH.PosY]=src[KEY_GUICfgH.PosY]

def carryOver_windowGeometry_dependent(GUIObj):
    if True==GUIObj.cfgHandle[KEY_GUICfgH.RetainGeometry]:
        carryOver_windowGeometry(GUIObj.cfgHandle_rt,GUIObj.cfgHandle)

def carryOver_allRead(dst,readCfg):
    dst[KEY_GUICfgH.RetainGeometry]=readCfg[KEY_GUICfgH.RetainGeometry]
    carryOver_windowGeometry(dst,readCfg)








def GUIconfigHandle_updateStorage(GUIObj):
    GUIflush_runtime_to_cfghandle(GUIObj)
    configHandle_dumpPersistent(GUIObj.cfgHandle,GUI_cfg_file_path,GUI_cfg_file_prefix+GUI_cfg_file_fName+GUI_cfg_file_fExt)



def GUIconfigHandle_readIn(GUIObj):
    err=configHandle_readPersistent(GUIObj.cfgHandle,GUI_cfg_file_path,GUI_cfg_file_prefix+GUI_cfg_file_fName+GUI_cfg_file_fExt,carryOver_allRead)
    if not 0==err:
        GUIObj.cfgHandle=copy.deepcopy(GUIObj.cfgHandle_rt)
        GUIconfigHandle_updateStorage(GUIObj)
    GUIObj.cfgHandle_rt[KEY_GUICfgH.RetainGeometry]=GUIObj.cfgHandle[KEY_GUICfgH.RetainGeometry]
    carryOver_windowGeometry_dependent(GUIObj)



