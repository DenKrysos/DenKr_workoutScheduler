#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-10

@author: Dennis Krummacker
'''

## System Packages
import os
import json
import copy


##DenKr Packages
from auxiliary.filesystem import create_file
from DenKr_essentials_py.struct_handling import convert_tuple_to_list
from DenKr_essentials_py.sort_search import search_sorted_list


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV
##Workout-Scheduler Packages
from settings.values import equipID, muscleID, useMeth, SetupExeIdx
##Individual Configuration
import settings.config_handler as cfghandle
##Fundamental Project Settings
from settings.path_and_file import (
    config_file_subpath,
    config_file_fExt,
    config_file_prefix,
    config_file_fname,
    configSetup_file_prefix,
    configSetup_file_fname
)



def sort_exercises_muscleIntensity(exeArray):
    for exe in exeArray:
        exe[SetupExeIdx.INTENSITY].sort(key=lambda x: x[1], reverse=True)

def clean_undefined_EnumEntries(cfgSetup):
    for exercise in cfgSetup[cfghandle.keySetupExe]:
        for i, val in enumerate(exercise[SetupExeIdx.EQUIPMENT]):
            if val==equipID.undef:
                exercise[SetupExeIdx.EQUIPMENT].pop(i)
        for i, lst in enumerate(exercise[SetupExeIdx.INTENSITY]):
            if lst[0]==muscleID.undef:
                exercise[SetupExeIdx.INTENSITY].pop(i)





#USAGE for Conversion:
# To simply convert to string, just use:
#    json.dumps(convert_keys(test))
# Use the provided hook to pass a function that let's you choose how to convert
#   - Means, define a function, like the enun_names(), then:
#    json.dumps(convert_keys(test, enum_names))
# Similarly for the reverse process. The "convert_keys()" stays the same, but you may define a "names_to_enum()", then:
#    convert_keys(json.loads(json_data), names_to_enum)
#
#NOTE: Instead of converting values beforehand, one could just leave them alone and pass "default=str" to the dump() function, like
#           json.dump(convertedDat,f,sort_keys=False,indent=2,default=str)
# But to have things consistent, I implemented it here the way, that everything is converted upfront and reverted after reading.
def convert_keys(obj, convert=str):
    if isinstance(obj, list):
        return [convert_keys(i, convert) for i in obj]
    if isinstance(obj, tuple):
        return tuple(convert_keys(i, convert) for i in obj)
    if not isinstance(obj, dict):
        return obj
    return {convert(k): convert_keys(v, convert) for k, v in obj.items()}

def convert_keyAndVal(obj, convertKey=str, convertVal=lambda x:x):
    if isinstance(obj, list):
        return [convert_keyAndVal(i, convertKey, convertVal) for i in obj]
    if isinstance(obj, tuple):
        return tuple(convert_keyAndVal(i, convertKey, convertVal) for i in obj)
    if isinstance(obj, dict):
        return {convertKey(k): convert_keyAndVal(v, convertKey, convertVal) for k, v in obj.items()}
    else:
        return convertVal(obj)
# - - - - - - - - - - - - - - - - - - - - - - - -
def enum_names_forKey(key):
    if isinstance(key, equipID):
        return "equipID."+key.name
    elif isinstance(key, muscleID):
        return "muscleID."+key.name
    elif isinstance(key, useMeth):
        return "useMeth."+key.name
    return str(key)

def names_to_enum_forKey(key):
    trgtEnum=None
    if key.startswith("equipID."):
        trgtEnum=equipID
        key=key[len("equipID."):]
    elif key.startswith("muscleID."):
        key=key[len("muscleID."):]
        trgtEnum=muscleID
    elif key.startswith("useMeth."):
        key=key[len("useMeth."):]
        trgtEnum=useMeth
    else:
        return key
    try:
        return trgtEnum[key]
    except KeyError:
        return key
# - - - - - - - - - - - - - - - - - - - - - - - -
def enum_names_forVal(val):
    #Forward Conversion shall not stringify other types
    if isinstance(val, equipID):
        return "equipID."+val.name
    elif isinstance(val, muscleID):
        return "muscleID."+val.name
    elif isinstance(val, useMeth):
        return "useMeth."+val.name
    return val

def names_to_enum_forVal(val):
    if isinstance(val, str):
        #Equal for reverse conversion
        return names_to_enum_forKey(val)
    else:
        return val




#This converts the Enum Keys upfront
def configHandle_dumpPersistent(cfgObj,pathSub,fName):
    fpath=os.path.join(globV.progPath,pathSub)
    ffull_tmp=os.path.join(fpath,fName+".tmp")
    ffull=os.path.join(fpath,fName)
    convertedDat=convert_keyAndVal(cfgObj,enum_names_forKey,enum_names_forVal)
    if os.path.exists(ffull_tmp):# We don't want that: First delete existing one
        os.remove(ffull_tmp)
    try:
        #f = open(ffull_tmp, mode='w', encoding = 'utf-8')
        f=create_file(fpath,ffull_tmp)
        #File Operations
        json.dump(convertedDat,f,sort_keys=False,indent=2)
        f.close()
    except Exception as exc:
        globV.HCI.printErr(f"Writing of Cfg-File failed: \"{ffull_tmp}\".")
        globV.HCI.printErr(f"  --> {exc}")
        return
    #finally:
        #f.close()
    #Replace actual File with temp-one
    if os.path.exists(ffull):
        os.remove(ffull)
    os.rename(ffull_tmp,ffull)


#This also clears away entries that are of Enum-Value "undefined"
def configHandle_updateStorage():
    configHandle_dumpPersistent(
        cfghandle.cfg_handle,
        config_file_subpath,
        config_file_prefix+config_file_fname+config_file_fExt
    )
    clean_undefined_EnumEntries(cfghandle.cfgSetup_handle)
    configHandle_dumpPersistent(
        cfghandle.cfgSetup_handle,
        config_file_subpath,
        configSetup_file_prefix+configSetup_file_fname+config_file_fExt
    )


def flush_runtime_to_cfghandle():
    cfghandle.cfg_handle=copy.deepcopy(cfghandle.cfgh_rt)
    cfghandle.cfgSetup_handle=copy.deepcopy(cfghandle.cfgSetup_rt)


def writeBack_cfghandle_to_runtime():
    cfghandle.cfgh_rt=copy.deepcopy(cfghandle.cfg_handle)
    cfghandle.cfgSetup_rt=copy.deepcopy(cfghandle.cfgSetup_handle)


def cfg_runtime_writeThrough_storage():
    flush_runtime_to_cfghandle()
    configHandle_updateStorage()








def configHandle_readPersistent(cfgObj,pathSub,fName,carryOverFunc):
    fpath=os.path.join(globV.progPath,pathSub)
    ffull=os.path.join(fpath,fName)
    try:
        f=open(ffull, mode='r', encoding = 'utf-8')
        # perform file operations
        try:
            readDat=json.load(f)
        except json.decoder.JSONDecodeError:
            return 2
        f.close()
    except FileNotFoundError:
        configHandle_dumpPersistent(cfgObj,pathSub,fName)
        return 1
    revertedDat=convert_keyAndVal(readDat, names_to_enum_forKey, names_to_enum_forVal)
    carryOverFunc(cfgObj,revertedDat)
    return 0
# - - - - - - - - - - - - - - -
def carryOver_entries_basicCfg(trgt,src):
    for k, v in trgt.items():
        if isinstance(k, dict):
            try:
                carryOver_entries_basicCfg(v,src[k])
                del src[k]
            except KeyError:
                pass
        else:
            try:
                trgt[k]=src[k]
                del src[k]
            except KeyError:
                pass
    # for k, v in src.items():
    #     if isinstance(k, dict):
    #         trgt[k]={}
    #         carryOver_entries_setupCfg(trgt[k],v)
    #     else:
    #         trgt[k]=v
    #         del src[k]
# - - - - - - - - - - - - - - -
def carryOver_entries_setupCfg(trgt,src):
    src[cfghandle.keySetupMuscle].sort(key=lambda x: x[0].value[0], reverse=False)
    src[cfghandle.keySetupExe].sort(key=lambda x: x[0], reverse=False)
    for i in range(len(trgt[cfghandle.keySetupMuscle])):
        entry=trgt[cfghandle.keySetupMuscle][i]
        index=search_sorted_list(src[cfghandle.keySetupMuscle],entry[0].value[0],key=lambda x: x[0].value[0])
        if -1==index:
            continue
        trgt[cfghandle.keySetupMuscle][i]=src[cfghandle.keySetupMuscle][index]
        src[cfghandle.keySetupMuscle].pop(index)
    for i in range(len(trgt[cfghandle.keySetupExe])):
        entry=trgt[cfghandle.keySetupExe][i]
        index=search_sorted_list(src[cfghandle.keySetupExe],entry[0],key=lambda x: x[0])
        if -1==index:
            continue
        trgt[cfghandle.keySetupExe][i]=src[cfghandle.keySetupExe][index]
        src[cfghandle.keySetupExe].pop(index)
    # For now, I decide to also carry over entries from the cfg-file that are actually not predefined.
    # In case of the Basic Cfg-Values, they would just do nothing, hence not done for this.
    # In case of the Setup-Cfg, they add additional exercises, which are indeed used. (And probably muscles, which cannot properly be used, since the Enum doesn't support them)
    #  (I know, I could have directly written over all read values, but maybe in the future I want to change that behavior, then I just have to delete the part below
    trgt[cfghandle.keySetupMuscle].extend(src[cfghandle.keySetupMuscle])
    trgt[cfghandle.keySetupExe].extend(src[cfghandle.keySetupExe])
# - - - - - - - - - - - - - - -


def configHandle_init():
    #No need to init "cfghandle.cfg_handle". Already done at declaration
    #No need to init "cfghandle.cfgSetup_handle". Already done at declaration
    cfghandle.cfgSetup_handle=copy.deepcopy(cfghandle.cfgSetup_handle_inherent)
    convert_tuple_to_list(cfghandle.cfgSetup_handle)
    cfghandle.cfgSetup_handle[cfghandle.keySetupMuscle].sort(key=lambda x: x[0].value[0], reverse=False)
    cfghandle.cfgSetup_handle[cfghandle.keySetupExe].sort(key=lambda x: x[0], reverse=False)


def configHandle_setup():
    configHandle_init()
    configHandle_readPersistent(
        cfghandle.cfg_handle,
        config_file_subpath,
        config_file_prefix+config_file_fname+config_file_fExt,
        carryOver_entries_basicCfg
    )
    configHandle_readPersistent(
        cfghandle.cfgSetup_handle,
        config_file_subpath,
        configSetup_file_prefix+configSetup_file_fname+config_file_fExt,
        carryOver_entries_setupCfg
    )
    sort_exercises_muscleIntensity(cfghandle.cfgSetup_handle[cfghandle.keySetupExe])
    writeBack_cfghandle_to_runtime()#Runtime Copy






