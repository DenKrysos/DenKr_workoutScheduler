#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2020-11-18
Last Update: 2023-04-16

@author: Dennis Krummacker
'''

import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont



##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV
from settings.path_and_file_exe import exePaths


from DenKr_essentials_py.Dev.pack_and_install import produce_exe_pyinstaller, move_exe_fromOutToExeDir

import settings.config_handler as cfghandle




class GUI_Operative_Functions:
    @classmethod
    def print_computed_schedule(cls,GUIObj,date=None):
        globV.HCI.switch_out(GUIObj.IOstream_result)
        GUIObj.workout.history_show_computedWorkoutSchedule(date)
        globV.HCI.restore_out()
    @classmethod
    def print_previous_schedule(cls,GUIObj):
        globV.HCI.switch_out(GUIObj.IOstream_past)
        GUIObj.workout.history_show_previousWorkoutSchedule()
        globV.HCI.restore_out()
    @classmethod
    def rewrite_computed_schedule(cls,GUIObj):
        GUIObj.IOstream_result.clear()
        selectedRadio=GUIObj.variables.cfgTabBasic.calendarRadio_var.get()
        if selectedRadio=="gen":
            GUIObj.IOstream_result.clear()
            cls.print_computed_schedule(GUIObj)
        elif selectedRadio=="cal":
            date=GUIObj.variables.cfgTabBasic.calEnt.get_date()
            GUIObj.IOstream_result.clear()
            cls.print_computed_schedule(GUIObj,date)
        else:
            print("Unknown option selected")
    @classmethod
    def history_write_userPrompt(cls,GUIObj):
        # scrollDown=[]
        # texts=[
        #     GUIObj.widgets.text_stdout,
        #     GUIObj.widgets.text_out2
        # ]
        # def scroll_textAreas_down_analyse():
        #     for i in range(len(texts)):
        #         visibleFraction=texts[i].yview()
        #         #print(f"1 {visibleFraction[1]}")
        #         if 1.0==visibleFraction[1]:
        #             scrollDown.append(1)
        #         else:
        #             scrollDown.append(0)
        # def scroll_textAreas_down():
        #     for i in range(len(scrollDown)):
        #         if 1==scrollDown[i]:
        #             print("2")
        #             texts[i].yview_moveto(1.0)
        # scroll_textAreas_down_analyse()
        visibleFraction=GUIObj.widgets.text_stdout.yview()
        if 1.0==visibleFraction[1]:
            GUIObj.state.scrollStdout=True
        GUIObj.widgets.userQuery_area_pack()
        # scroll_textAreas_down()
        GUIObj.IOstream_query.clear()
        globV.HCI.switch_out(GUIObj.IOstream_query)
        globV.HCI.printStd("»Shall the history-files be updated with the recent computation?«",end="")
        globV.HCI.restore_out()
    @classmethod
    def set_exercise_names(cls,GUIObj):
        GUIObj.state.exe_names=[sublist[0] for sublist in cfghandle.cfgSetup_rt[cfghandle.keySetupExe]]
        GUIObj.state.exe_names.sort()


def GUI_call_makeExe(GUIObj):
    globV.HCI.printStd("Production of Bundled-Exe called.")
    globV.HCI.printStd(f"Current Working-Directory:\n  -> {globV.progPath}\n")
    GUIObj.root.update_idletasks()
    #create a popup for safety query
    displaytxt="Producing Exe.\nYou sure?\nThis'll create directories \"build\"&\"out\"\nparallel to current Working-Dir\n(see StdOut-Window)."
    popup=tk.Toplevel(GUIObj.root)
    popup.title('Produce Exe')
    label=tk.Label(popup, text=displaytxt, font=('Helvetica', 12, tkfont.BOLD), bg='DarkOrange1', highlightthickness=0)
    button_yes=ttk.Button(popup, style="Top.DK.TButton", width=10, text="Yes")
    button_no=ttk.Button(popup, style="Top.DK.TButton", width=10, text="Cancel")
    popupwidth=label.winfo_reqwidth()+40
    popupheight=label.winfo_reqheight()+button_yes.winfo_reqheight()+30
    x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
    y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
    popup.geometry('{}x{}+{}+{}'.format(popupwidth,popupheight,x-popupwidth//2,y-popupheight//2))
    popup.config(bg='DarkOrange1')
    # popup.attributes('-alpha', 0.8)
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=1)
    label.grid(row=0,column=0, columnspan=2, padx=0, pady=(10,0), sticky=tk.NW+tk.E)
    button_yes.grid(row=1,column=0, padx=0, pady=(0,10))
    button_no.grid(row=1,column=1, padx=0, pady=(0,10))
    def button_yes_func():
        popup.destroy()
        produce_exe_pyinstaller(GUIObj)
    def button_no_func():
        popup.destroy()
    button_yes.configure(command=button_yes_func)
    button_no.configure(command=button_no_func)


def GUI_call_moveExe(GUIObj):
    env=exePaths()
    trgtDir=env.pathTop.replace("Programme","Program_exe")
    srcF=os.path.join(env.pathOutDir,env.exeNameRecent+".exe")
    trgtF=os.path.join(trgtDir,env.exeNameRecent+".exe")
    globV.HCI.printStd("")
    globV.HCI.printStd("Moving Bundled-Exe to DenKr's Dir for Operative-State:")
    globV.HCI.printStd(f"-> Src-File: {srcF}")
    globV.HCI.printStd(f"-> Dst-Directory: {trgtDir}")
    globV.HCI.printStd("Old .exe in the Target-Directory will be deleted.")
    globV.HCI.printStd("The Src-out-Directory will be removed.")
    globV.HCI.printStd("")
    GUIObj.root.update_idletasks()
    #
    #create a popup for safety query
    displaytxt="Moving Bundled-Exe.\n(See StdOut-Area)\nProceed?"
    popup=tk.Toplevel(GUIObj.root)
    popup.title('Moving Bundled-Exe')
    label=tk.Label(popup, text=displaytxt, font=('Helvetica', 12, tkfont.BOLD), bg='DarkOrange1', highlightthickness=0)
    button_yes=ttk.Button(popup, style="Top.DK.TButton", width=10, text="Yes")
    button_no=ttk.Button(popup, style="Top.DK.TButton", width=10, text="Cancel")
    popupwidth=label.winfo_reqwidth()+40
    popupheight=label.winfo_reqheight()+button_yes.winfo_reqheight()+30
    x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
    y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
    popup.geometry('{}x{}+{}+{}'.format(popupwidth,popupheight,x-popupwidth//2,y-popupheight//2))
    popup.config(bg='DarkOrange1')
    # popup.attributes('-alpha', 0.8)
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=1)
    label.grid(row=0,column=0, columnspan=2, padx=0, pady=(10,0), sticky=tk.NW+tk.E)
    button_yes.grid(row=1,column=0, padx=0, pady=(0,10))
    button_no.grid(row=1,column=1, padx=0, pady=(0,10))
    def button_yes_func():
        popup.destroy()
        move_exe_fromOutToExeDir(srcF,trgtF)
    def button_no_func():
        popup.destroy()
    button_yes.configure(command=button_yes_func)
    button_no.configure(command=button_no_func)





