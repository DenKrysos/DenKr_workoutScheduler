#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-10

@author: Dennis Krummacker
'''


## Some Fundamentals
import package.importMe_fundamental  # @UnusedImport


## System Packages
import os
import json
import datetime


##Project Settings
from settings import global_variables
from settings.path_and_file import (
    history_file_subpath,
    history_file_bkp_subpath,
    history_files_all
)




def history_create_file(path,file_full):
    _assure_Dir_exists(path)
    try:
        f = open(file_full, mode='w', encoding = 'utf-8')
    except FileNotFoundError:
        print("Creation of history-file %s failed" % file_full)
        return
    except:
        print("Creation of history-file %s failed" % file_full)
        return
    #finally:
        #f.close()
    return f




def file_json_write(fName,writeData):
    fpath=os.path.join(global_variables.progPath,history_file_subpath)
    ffull_tmp=os.path.join(fpath,fName+".tmp")
    ffull=os.path.join(fpath,fName)
    if os.path.exists(ffull_tmp):# We don't want that: First delete existing one
        os.remove(ffull_tmp)
    try:
        #f = open(ffull_tmp, mode='w', encoding = 'utf-8')
        f=history_create_file(fpath,ffull_tmp)
        #File Operations
        json.dump(writeData,f,sort_keys=False,indent=2)
        f.close()
    except:
        print("Writing of history-file %s failed" % ffull_tmp)
        return
    #finally:
        #f.close()
    #Replace actual File with temp-one
    if os.path.exists(ffull):
        os.remove(ffull)
    os.rename(ffull_tmp,ffull)




def file_json_read(fName):
    fpath=os.path.join(global_variables.progPath,history_file_subpath)
    ffull=os.path.join(fpath,fName)
    try:
        f = open(ffull, mode='r', encoding = 'utf-8')
        # perform file operations
        try:
            readF=json.load(f)
        except json.decoder.JSONDecodeError:
            readF={}
        #self.history = json.loads(bz2.BZ2File(ffull).read().decode())
        f.close()
    except FileNotFoundError:
        #f = self.history_create_file(fpath,ffull)
        readF={}
    #finally:
        #f.close()
    return readF




def file_backup_asMove(fName,fExt):
    fpath_src=os.path.join(global_variables.progPath,history_file_subpath)
    fpath_dst=os.path.join(fpath_src,history_file_bkp_subpath)
    ffull_src=os.path.join(fpath_src,fName+fExt)
    dateToday=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    ffull_dst=os.path.join(fpath_dst,fName+"_"+dateToday+fExt)
    _assure_Dir_exists(fpath_dst)
    #ToDo: Proper Error-Handling
    try:
        os.rename(ffull_src,ffull_dst)
    except:
        print("Could not create History-File Backup \"%s\"."%(fName+fExt))



def directory_history_tidy():
    histDir=os.path.join(global_variables.progPath,history_file_subpath)
    dateToday=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    bkpDir=os.path.join(histDir,history_file_bkp_subpath,"tidy_"+dateToday)
    with os.scandir(histDir) as iter:
        for entry in iter:
            if os.path.isfile(entry.path):
                if not entry.name in history_files_all:
                    _assure_Dirs_exist(bkpDir)
                    try:
                        full_dst=os.path.join(bkpDir,entry.name)
                        os.rename(entry.path,full_dst)
                    except:
                        print("While tidying up History-Dir, could not move File \"%s\" to \"%s\"."%(entry.name,bkpDir))




#=====================================================
#-----------------------------------------------------
#=====================================================


#Create all missing subdirectories
def _assure_Dirs_exist(fullPath):
    os.makedirs(fullPath, exist_ok=True)


#Only creates the last directory
def _assure_Dir_exists(fullPath):
    try:
        os.mkdir(fullPath)
    except FileExistsError:
        pass
    except OSError:
        print("Creation of the directory %s failed" % fullPath)
    except:
        print("Creation of the directory %s failed" % fullPath)
    #else:
        #print("Successfully created the directory %s " % path)


#=====================================================
#-----------------------------------------------------
#=====================================================


def file_json_read_singleArray(fName):
    fpath=os.path.join(global_variables.progPath,history_file_subpath)
    ffull=os.path.join(fpath,fName)
    try:
        f = open(ffull, mode='r', encoding = 'utf-8')
        # perform file operations
        try:
            readF=json.load(f)
        except json.decoder.JSONDecodeError:
            readF=[]
        #self.history = json.loads(bz2.BZ2File(ffull).read().decode())
        f.close()
    except FileNotFoundError:
        #f = self.history_create_file(fpath,ffull)
        readF=[]
    #finally:
        #f.close()
    return readF