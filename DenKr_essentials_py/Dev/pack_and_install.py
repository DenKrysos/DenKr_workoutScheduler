#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-19

@author: Dennis Krummacker
'''

#System Packages
import os
import shutil
import subprocess
import threading


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV

from settings.path_and_file_exe import exePaths

from auxiliary.filesystem import _assure_Dirs_exist



##DenKr Packages
from DenKr_essentials_py.order_tidyness import remove_pycache




def produce_exe_pyinstaller(GUIObj):
    installer_thread=threading.Thread(target=produce_exe_pyinstaller_thread, args=(GUIObj,))
    installer_thread.start()
    
#Todo: As soon as this is used for a second project: Adjust it to be more generalized, pass the main-File, Program-Name and additional-data-files as arguments or something.
def produce_exe_pyinstaller_thread(GUIObj):
    #Setting up some values
    env=exePaths()
    mainFile='''DenKr_workoutScheduler_main.py'''
    #Preparing the Cmd and Cmd-Line-Arguments for PyInstaller
    cmd='''Python -m PyInstaller'''
    cmdLineArgs=[
        f'''--name=\"{env.exeNameRecent}\"'''
    ,
        '''--onefile'''
    ,
    #     '''--windowed'''
    # ,
    #     f'''--icon=\"{iconDir}\"'''
    # ,
        f'''--specpath=\"{env.pathBuildDir}\"'''
    ,
        f'''--workpath=\"{env.pathBuildDir}\"'''
    ,
        f'''--distpath=\"{env.pathOutDir}\"'''
    ]
    dataFiles=[
        ('''settings''', '''requirements_GUI.txt''')
    ,
        ('''settings''', '''requirements_plain.txt''')
    ,
        ('''GUI''', '''DenKr.ico''')
    ]
    dfRootPath=os.path.join(env.pathRel,env.srcDir)
    for df in dataFiles:
        dfPath=dfRootPath[:]
        for it in df:
            dfPath=os.path.join(dfPath,it)
        dfModule=''
        for i in range(0,len(df)-1):
            if not 0==len(dfModule):
                dfModule+='.'#ToDo Possible Bug-Source, how are Submodules to be concatenated here for PyInstaller? Via "." or "/"? I think, with dots, like here
            dfModule+=df[i]
        cmdoption=f'''\"{dfPath};{dfModule}\"'''
        cmdLineArgs.append(
            f"--add-data {cmdoption}"
        )
    hiddenImports=[
        '''babel.numbers'''
    ]
    for hi in hiddenImports:
        cmdLineArgs.append(
            f"--hidden-import \"{hi}\""
        )
    cmdLineArgs.append(
        f'''\"{os.path.join(globV.progPath,mainFile)}\"'''
    )
    for it in cmdLineArgs:
        cmd+=" "+it
    #Just, why not?
    remove_pycache(globV.progPath)
    globV.HCI.printStd("")
    displayCmd=""
    openQuot=0
    escape=False
    for char in cmd:
        if ' '==char and 0==openQuot:
            displayCmd+='\n\t'
        else:
            displayCmd+=char
        if '"'==char and False==escape:
            if 0==openQuot:
                openQuot=1
            else:
                openQuot=0
        # if '\\'==char and False==escape:
        #     escape=True
        # else:
        #     escape=False
    globV.HCI.printStd(f"Opening threaded live Subprocess Pipe to PyInstaller with:\n  -> {displayCmd}\n")
    GUIObj.root.update_idletasks()
    globV.HCI.sout.switch_to_queueMode()
    globV.HCI.serr.switch_to_queueMode()
    def _read_output(streamIn,printFuncAttr):
        printFunc=getattr(globV.HCI, printFuncAttr)
        GUIObj.root.update_idletasks()
        while True:
            output=streamIn.readline().decode()
            if output=='':
                break
            printFunc(output.strip())
            GUIObj.root.update_idletasks()
    def read_output_std(streamIn):
        _read_output(streamIn,'printStd')
    def read_output_err(streamIn):
        _read_output(streamIn,'printErr')
    #Run the thing and redirect its stdout and stderr to separate pipes
    process=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Create threads to read the output of the subprocess in real-time
    stdout_thread=threading.Thread(target=read_output_std, args=(process.stdout,))
    stderr_thread=threading.Thread(target=read_output_err, args=(process.stderr,))
    #Todo this currently assumes that the function can only be called via the GUI. If some time it shall also be called from Terminal, adjust the stream-handling
    stdout_thread.start()
    stderr_thread.start()
    # Wait for the threads to finish
    stdout_thread.join()
    stderr_thread.join()
    # Wait for the subprocess to complete
    returnCode=process.wait()
    globV.HCI.sout.switch_to_directMode()
    globV.HCI.serr.switch_to_directMode()
    GUIObj.root.update_idletasks()
    # Print the returncode, output and error messages
    globV.HCI.printStd(f"\nPyInstaller returned: {returnCode}")
    globV.HCI.printStd("")
    # globV.HCI.printStd(f"PyInstaller returned: {result.returncode}")
    # globV.HCI.printStd(f"PyInstaller's output:\n{result.stdout}")
    # globV.HCI.printStd("PyInstaller's error:")
    # globV.HCI.printErr(f"{result.stderr}")
    globV.HCI.printStd("")
    def clean_oldExe():
        for file in os.listdir(env.pathOutDir):
            if not file==env.exeNameRecent+".exe":
                if os.path.isfile(os.path.join(env.pathOutDir, file)):
                    os.remove(os.path.join(env.pathOutDir,file))
                else:
                    shutil.rmtree(os.path.join(env.pathOutDir, file))
    clean_oldExe()
    if 0==returnCode:
        shutil.rmtree(env.pathBuildDir)



def move_exe_fromOutToExeDir(srcF,trgtF):
    trgtDir=os.path.dirname(trgtF)
    env=exePaths()
    def clean_oldExe_dst():
        for file in os.listdir(trgtDir):
            if os.path.isfile(os.path.join(trgtDir, file)):
                if -1!=file.find(env.exeName):
                    if not file==env.exeNameRecent+".exe":
                        os.remove(os.path.join(trgtDir,file))
    clean_oldExe_dst()
    try:
        _assure_Dirs_exist(trgtDir)
        os.rename(srcF,trgtF)
    except FileNotFoundError:
        globV.HCI.printErr(f"Could not move File\n-> \"{srcF}\"\n\tto\n-> \"{trgtF}\".\n(Source-File not existent)")# no need for "or Destination-Directory" because missing Dirs are created
    except:
        globV.HCI.printErr(f"Could not move File\n-> \"{srcF}\"\n\tto\n-> \"{trgtF}\".")
    def clean_outDir():
        shutil.rmtree(env.pathOutDir)
    try:
        clean_outDir()
    except FileNotFoundError:
        pass
    except Exception as e:
        globV.HCI.printErr(f"While moving exe, occurred exception: {e}")


