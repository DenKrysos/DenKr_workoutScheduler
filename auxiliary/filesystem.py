#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-10

@author: Dennis Krummacker
'''


import os
import json


##Project Settings
from settings import global_variables
from settings.path_and_file import (
    history_file_subpath
)




def history_create_file(path,file_full):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except OSError:
        print("Creation of the directory %s failed" % path)
    except:
        print("Creation of the directory %s failed" % path)
    #else:
        #print("Successfully created the directory %s " % path)
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
        print("Wrting of history-file %s failed" % ffull_tmp)
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