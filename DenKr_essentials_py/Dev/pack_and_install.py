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
from settings.VersionInfo import VERSION_DESCRIPTION



##DenKr Packages
from DenKr_essentials_py.order_tidyness import remove_pycache




def produce_exe_pyinstaller(GUIObj):
    installer_thread=threading.Thread(target=produce_exe_pyinstaller_thread, args=(GUIObj,))
    installer_thread.start()
    
#Todo: As soon as this is used for a second project: Adjust it to be more generalized, pass the main-File, Program-Name and additional-data-files as arguments or something.
def produce_exe_pyinstaller_thread(GUIObj):
    #Setting up some values
    pathRel='..'
    pathTop=os.path.join(globV.progPath,pathRel)
    pathBuildDir=os.path.join(pathTop,'build')
    pathOutDir=os.path.join(pathTop,'out')
    #
    exeName=f'''DenKr_workoutScheduler_{VERSION_DESCRIPTION}'''
    mainFile='''DenKr_workoutScheduler_main.py'''
    srcDir='''src'''
    #Preparing the Cmd and Cmd-Line-Arguments for PyInstaller
    cmd='''Python -m PyInstaller'''
    cmdLineArgs=[
        f'''--name=\"{exeName}\"'''
    ,
        '''--onefile'''
    ,
        f'''--specpath=\"{pathBuildDir}\"'''
    ,
        f'''--workpath=\"{pathBuildDir}\"'''
    ,
        f'''--distpath=\"{pathOutDir}\"'''
    ]
    dataFiles=[
        ('''settings''', '''requirements_GUI.txt''')
    ,
        ('''settings''', '''requirements_plain.txt''')
    ]
    for df in dataFiles:
        dfPath=os.path.join(pathRel,srcDir)
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
    globV.HCI.printStd(f"Opening threaded live Subprocess Pipe to PyInstaller with:\n  -> {cmd}\n")
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
    if 0==returnCode:
        shutil.rmtree(pathBuildDir)


