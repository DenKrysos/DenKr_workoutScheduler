#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2023-04-14
Last Update: 2023-04-18

@author: Dennis Krummacker
'''


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV


import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
try:
    from tkcalendar import DateEntry
except ImportError:
    globV.HCI.printErr("============================================")
    globV.HCI.printErr("==  ERROR: Dependency missing: \"tkcalendar\".")
    globV.HCI.printErr("============================================")
    globV.HCI.printErr("--> This won't work without installing requirements...")
# from datetime import date


##DenKr Packages
from DenKr_essentials_py.GUI.GUI_tkinter_basic import GUI_variables
from DenKr_essentials_py.GUI.GUI_tkinter_elements import create_themeSelect_frame
from DenKr_essentials_py.order_tidyness import remove_pycache
from DenKr_essentials_py.Dev.pack_and_install import produce_exe_pyinstaller

##Other Files for Project
##Workout-Scheduler Packages
import settings.config_handler as cfghandle
from GUI.GUI_operative_functions import GUI_Operative_Functions as guif
from auxiliary.config_handling import cfg_runtime_writeThrough_storage, writeBack_cfghandle_to_runtime, configHandle_setup



#==========================================================================
#--------------------------------------------------------------------------
# Configuration Area
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def create_cfg_area(GUIObj):
    #--------------------------------------------
    # Element definition
    # - - - - - - - - - - - - - - - - - - - - - -
    frame_config=ttk.Frame(GUIObj.root, style="Config.DK.TFrame")
    # Top-Row: Heading, Label
    def create_topFrame():
        TopFrameBottomSep=ttk.Frame(frame_config, style="BottomSep.Top.DK.TFrame")
        topFrameBorder=ttk.Frame(TopFrameBottomSep, style="Border.Top.DK.TFrame")
        topFrameBorder.pack(fill=tk.BOTH,expand=tk.YES,padx=0,pady=(0,2))
        TopFrame=ttk.Frame(topFrameBorder, style="Top.DK.TFrame")
        TopFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=(0,5), pady=0)
        toplabel=ttk.Label(
            TopFrame,
            style="Heading1.DK.TLabel",
            text="Configuration"
        )
        ### Sub-Frame Packing
        toplabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NW)
        return TopFrameBottomSep
    topFrame=create_topFrame()
    # - - - - - - - - - - - - - - - - - - - - - -
    #
    # Create Config-Tabs
    def create_cfgTabs():
        cfgTabs=ttk.Notebook(frame_config, style='Config.DK.TNotebook')
        # - - - - - -
        #
        # Tab: Basic Configs
        def create_cfgTab_basic():
            # - - - - - -
            #Some Variables to be visible across
            GUIObj.variables.cfgTabBasic=GUI_variables()
            # - - - - - - - - - - - -
            # Tab-Basics
            tab_cfgBasic=ttk.Frame(cfgTabs, style="Config.DK.TFrame")
            # - - - - - - - - - - - -
            #
            # Sub-Frame: Values
            def create_subFrame_values():
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameVal=ttk.Frame(tab_cfgBasic, style="Config.DK.TFrame")
                def change_reverseOutput(*args):
                    select_bool=GUIObj.variables.cfgTabBasic.revOutput_var.get()
                    cfghandle.cfgh_rt[cfghandle.keyOutRev]=select_bool
                    guif.rewrite_computed_schedule(GUIObj)
                #GUIObj.state.stdOut_wordWrap=tk.NONE#WORD
                #
                revOutput_label=ttk.Label(subFrameVal, style="Config.DK.TLabel", text="Reverse Output:")
                GUIObj.variables.cfgTabBasic.revOutput_var=tk.BooleanVar()
                revOutput_checkbox=ttk.Checkbutton(subFrameVal, style="Config.DK.TCheckbutton", variable=GUIObj.variables.cfgTabBasic.revOutput_var)
                #
                def change_workoutsPerWeek(event):
                    try:
                        value=GUIObj.variables.cfgTabBasic.wo_pWeek_var.get()
                        cfghandle.cfgh_rt[cfghandle.keyWOpW]=value
                    except:
                        x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                        y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                        GUIObj.show_popup_simple('Not a valid number!',(x,y))
                GUIObj.variables.cfgTabBasic.wo_pWeek_var=tk.DoubleVar()
                wo_pWeek_label=ttk.Label(subFrameVal, style="Config.DK.TLabel", text="WorkoutsPerWeek:")
                wo_pWeek_entry=ttk.Entry(subFrameVal, style="Config.DK.TEntry", width=7, textvariable=GUIObj.variables.cfgTabBasic.wo_pWeek_var)
                #
                def change_numberWorkoutsToCompute(event):
                    value=GUIObj.variables.cfgTabBasic.num_toCompute_var.get()
                    cfghandle.cfgh_rt[cfghandle.keyNumComp]=value
                GUIObj.variables.cfgTabBasic.num_toCompute_var=tk.IntVar()
                num_toCompute_label=ttk.Label(subFrameVal, style="Config.DK.TLabel", text="Num-To-Compute:")
                num_toCompute_entry=ttk.Entry(subFrameVal, style="Config.DK.TEntry", width=7, textvariable=GUIObj.variables.cfgTabBasic.num_toCompute_var)
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                # revOutput_checkbox.configure(
                #     command=change_reverseOutput
                # )
                GUIObj.variables.cfgTabBasic.revOutput_var.set(cfghandle.cfgh_rt[cfghandle.keyOutRev])
                GUIObj.variables.cfgTabBasic.revOutput_var.trace("w",change_reverseOutput)
                #
                GUIObj.variables.cfgTabBasic.wo_pWeek_var.set(cfghandle.cfgh_rt[cfghandle.keyWOpW])
                wo_pWeek_entry.bind("<KeyRelease>", change_workoutsPerWeek)
                wo_pWeek_entry.bind("<FocusOut>", change_workoutsPerWeek)
                # Validation function to allow only numeric (decimal) input
                def validate_decimal_input(char, value):
                    if char.isdigit() or char == "." or char == "":
                        return True
                    else:
                        return False
                validate_cmd=GUIObj.root.register(validate_decimal_input)
                wo_pWeek_entry.configure(
                    validate="key",
                    validatecommand=(validate_cmd,"%S","%P")
                )
                #
                GUIObj.variables.cfgTabBasic.num_toCompute_var.set(cfghandle.cfgh_rt[cfghandle.keyNumComp])
                num_toCompute_entry.bind("<KeyRelease>", change_numberWorkoutsToCompute)
                num_toCompute_entry.bind("<FocusOut>", change_numberWorkoutsToCompute)
                # Validation function to allow only numeric (decimal) input
                def validate_numeric_input(char, value):
                    if char.isdigit() or char == "":
                        return True
                    else:
                        return False
                validate_cmd=GUIObj.root.register(validate_numeric_input)
                num_toCompute_entry.configure(
                    validate="key",
                    validatecommand=(validate_cmd,"%S","%P")
                )
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                revOutput_label.grid(row=row, column=col, padx=(0,10), pady=0, sticky=tk.E)
                col+=1
                revOutput_checkbox.grid(row=row, column=col, padx=0, pady=0, sticky=tk.W)
                row+=1
                col=0
                wo_pWeek_label.grid(row=row, column=col, padx=(0,10), pady=(5,0), sticky=tk.E)
                col+=1
                wo_pWeek_entry.grid(row=row, column=col, padx=0, pady=(5,0), sticky=tk.W)
                row+=1
                col=0
                num_toCompute_label.grid(row=row, column=col, padx=(0,10), pady=(5,0), sticky=tk.E)
                col+=1
                num_toCompute_entry.grid(row=row, column=col, padx=0, pady=(5,0), sticky=tk.W)
                row+=1
                col=0
                return subFrameVal
            subFrame_Values=create_subFrame_values()
            #
            # - - - - - - - - - - - -
            # Sub-Frame: Saving / Loading
            def create_subFrame_saveLoadReset():
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameSLR=ttk.Frame(tab_cfgBasic, style="Config.DK.TFrame")
                def save_config_persistent():
                    cfg_runtime_writeThrough_storage()
                def load_config_persistent():
                    configHandle_setup()
                    set_cfg_basic()
                def reset_config():#Only resets the displayed values, with what is present in the cfg_handle
                    writeBack_cfghandle_to_runtime()
                    set_cfg_basic()
                def print_help_config():
                    GUIObj.widgets.outTabs.select(0)
                    globV.HCI.switch_out(GUIObj.IOstream_std)
                    globV.HCI.printStd("")
                    globV.HCI.printStd("\"Persistent Storage\" Buttons:")
                    globV.HCI.printStd("  (Values changed in GUI do only affect the current Runtime. -> The tools operation uses these, but Files on Disk are not changed.)")
                    globV.HCI.printStd("- Reset: Resets Runtime/GUI Values back to what was last loaded.")
                    globV.HCI.printStd("- Load: Loads the cfg-File from Disk again and updates Runtime with its values.")
                    globV.HCI.printStd("- Save: Saves currently set Values persistently to cfg-File on Disk.")
                    globV.HCI.printStd("")
                    globV.HCI.restore_out()
                # Button for Saving current Cfg
                config_saveLoad_label=ttk.Label(subFrameSLR, style="Config.DK.TLabel", text="Persistent-Config:")
                config_reset_button=ttk.Button(subFrameSLR, style="Config.DK.TButton", text="Reset")
                config_reset_button.configure(command=reset_config)
                config_save_button=ttk.Button(subFrameSLR, style="Config.DK.TButton", text="Save")
                config_save_button.configure(command=save_config_persistent)
                config_load_button=ttk.Button(subFrameSLR, style="Config.DK.TButton", text="Load")
                config_load_button.configure(command=load_config_persistent)
                config_saveload_help_button=ttk.Button(subFrameSLR, style="Config.DK.TButton", text="?")
                config_saveload_help_button.configure(command=print_help_config)
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                config_saveLoad_label.grid(row=row, column=col, columnspan=4, padx=(0,0), pady=(0,5), sticky=tk.NW)
                row+=1
                col=0
                config_reset_button.grid(row=row, column=col, padx=(0,7), pady=0, sticky=tk.W)
                col+=1
                config_load_button.grid(row=row, column=col, padx=7, pady=0, sticky=tk.W)
                col+=1
                config_save_button.grid(row=row, column=col, padx=7, pady=0, sticky=tk.W)
                col+=1
                config_saveload_help_button.grid(row=row, column=col, padx=(7,0), pady=0)
                row+=1
                col=0
                return subFrameSLR
            subFrame_SaveLoad=create_subFrame_saveLoadReset()
            #
            # - - - - - - - - - - - -
            # Sub-Frame: Calendar
            def create_subFrame_calendar():
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameCal=ttk.Frame(tab_cfgBasic, style="Config.DK.TFrame")
                def on_calendarRadio_select(*args):
                    #print(f"{date.year}-{date.month}-{date.day}")
                    guif.rewrite_computed_schedule(GUIObj)
                def on_calendar_update(*args):
                    GUIObj.variables.cfgTabBasic.calendarRadio_var.set('cal')
                calendarContainer=ttk.Frame(subFrameCal, style="Config.DK.TFrame")
                calendar_label=ttk.Label(calendarContainer, style="Config.DK.TLabel", text="Date in Schedule:")
                GUIObj.variables.cfgTabBasic.calendarRadio_var=tk.StringVar()
                calendarRButt_gen=ttk.Radiobutton(calendarContainer, style="Config.DK.TRadiobutton", text="Generic", variable=GUIObj.variables.cfgTabBasic.calendarRadio_var, value="gen", command=on_calendarRadio_select)
                calendarRButt_cal=ttk.Radiobutton(calendarContainer, style="Config.DK.TRadiobutton", text="Calendar", variable=GUIObj.variables.cfgTabBasic.calendarRadio_var, value="cal", command=on_calendarRadio_select)
                #cal_stringVar=tk.StringVar()
                GUIObj.variables.cfgTabBasic.calEnt=DateEntry(calendarContainer,date_pattern='yyyy-MM-dd',selectmode='day')#, textvariable=cal_stringVar)#,year=today.year, month=today.month, day=today.day)
                calendar_label.grid(row=0, column=0, columnspan=3, pady=(0,7), sticky=tk.NW)
                calendarRButt_cal.grid(row=1, column=0, sticky=tk.NW)
                calendarRButt_gen.grid(row=2, column=0, sticky=tk.NW)
                GUIObj.variables.cfgTabBasic.calEnt.grid(row=1, column=1, padx=(7,0), sticky=tk.W)
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                #today=date.today()
                #cal_stringVar.trace('w',on_calendar_update)
                GUIObj.variables.cfgTabBasic.calEnt.bind("<<DateEntrySelected>>", on_calendar_update) 
                GUIObj.variables.cfgTabBasic.calendarRadio_var.set("gen")
                GUIObj.variables.cfgTabBasic.calendarRadio_var.trace('w',on_calendarRadio_select)
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                calendarContainer.grid(row=row, column=col, columnspan=3, padx=(0,10), pady=(0,0), sticky=tk.NW+tk.E)
                row+=1
                col=0
                return subFrameCal
            subFrame_Calendar=create_subFrame_calendar()
            #
            # - - - - - - - - - - - -
            # Sub-Frame: Current Layout adjust
            def create_subFrame_layoutAdjust():
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameLayout=ttk.Frame(tab_cfgBasic, style="Config.DK.TFrame")
                def change_wordWrap():
                    select=wordWrap_var.get()
                    if select:
                        GUIObj.state.stdOut_wordWrap=tk.WORD
                    else:
                        GUIObj.state.stdOut_wordWrap=tk.NONE
                    GUIObj.widgets.text_stdout.configure(wrap=GUIObj.state.stdOut_wordWrap)
                wordWrap_label=ttk.Label(subFrameLayout, style="Config.DK.TLabel", text="StdOut Word-Wrap:")
                wordWrap_var=tk.BooleanVar()
                wordWrap_checkbox=ttk.Checkbutton(subFrameLayout, style="Config.DK.TCheckbutton", variable=wordWrap_var)
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                if tk.WORD==GUIObj.state.stdOut_wordWrap:
                    wordWrap_var.set(True)
                else:#tk.NONE
                    wordWrap_var.set(False)
                wordWrap_checkbox.configure(
                    command=change_wordWrap
                )
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                wordWrap_label.grid(row=row, column=col, padx=(0,10), pady=(0,0), sticky=tk.E)
                col+=1
                wordWrap_checkbox.grid(row=row, column=col, padx=0, pady=(0,0), sticky=tk.W)
                row+=1
                col=0
                return subFrameLayout
            subFrame_Layout=create_subFrame_layoutAdjust()
            #
            # - - - - - - - - - - - -
            # Sub-Frame: New/Next Computation
            def create_subFrame_newComputation():
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFramenewComp=ttk.Frame(tab_cfgBasic, style="Config.DK.TFrame")
                def button_new_computation():
                    del GUIObj.workout
                    GUIObj.new_computation()
                compute_label=ttk.Label(subFramenewComp, style="Config.DK.TLabel", text="New Computation:")
                compute_button=ttk.Button(subFramenewComp, style="Config.DK.TButton", text="Compute")
                compute_button.configure(command=button_new_computation)
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                compute_label.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=(0,0), pady=(0,8))
                row+=1
                col=0
                compute_button.pack(anchor=tk.N, side=tk.TOP, padx=(0,0), pady=0)
                return subFramenewComp
            subFrame_newComp=create_subFrame_newComputation()
            #
            #--------------------------------------------
            # Element Configuration
            # - - - - - - - - - - - - - - - - - - - - - -
            def set_cfg_basic():
                GUIObj.variables.cfgTabBasic.revOutput_var.set(cfghandle.cfgh_rt[cfghandle.keyOutRev])
                GUIObj.variables.cfgTabBasic.wo_pWeek_var.set(cfghandle.cfgh_rt[cfghandle.keyWOpW])
                GUIObj.variables.cfgTabBasic.num_toCompute_var.set(cfghandle.cfgh_rt[cfghandle.keyNumComp])
            #set_cfg_basic()# Don't do it here, because this would trigger functions, which require settings that are only performed after this wrapping function is called. Initial value assignment is done right after creating the variables. This function is then only called by the Load/Reset buttons
            #
            #--------------------------------------------
            # Packing & Grid Config (Tab Cfg-Basic)
            # - - - - - - - - - - - - - - - - - - - - - -
            subFrame_Values.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10,0))
            saveSep=ttk.Separator(tab_cfgBasic, orient=tk.HORIZONTAL)
            saveSep.pack(side=tk.TOP, fill=tk.X, pady=(15,10))
            subFrame_SaveLoad.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0,0))
            calendarSep=ttk.Separator(tab_cfgBasic, orient=tk.HORIZONTAL)
            calendarSep.pack(side=tk.TOP, fill=tk.X, pady=15)
            subFrame_Calendar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0,0))
            layoutSep=ttk.Separator(tab_cfgBasic, orient=tk.HORIZONTAL)
            layoutSep.pack(side=tk.TOP, fill=tk.X, pady=15)
            subFrame_Layout.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0,0))
            compSep=ttk.Separator(tab_cfgBasic, orient=tk.HORIZONTAL)
            compSep.pack(side=tk.TOP, fill=tk.X, pady=(15,10))
            subFrame_newComp.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(20,10))
            # - - - - - - - - - - - - - - - - - - - - - - - -
            return tab_cfgBasic
        cfgTab_basic=create_cfgTab_basic()
        # - - - - - -
        #
        # Tab: Config Muscles
        def create_cfgTab_muscle():
            tab_cfgMuscle=ttk.Frame(cfgTabs, style="Config.DK.TFrame")
            return tab_cfgMuscle
        cfgTab_muscle=create_cfgTab_muscle()
        # - - - - - -
        #
        # Tab: Dev Tools
        def create_cfgTab_DevTools():
            tab_devTools=ttk.Frame(cfgTabs, style="Config.DK.TFrame")
            def create_subFrame_clear():
                subFrame_clear=ttk.LabelFrame(tab_devTools, style="Config.DK.TLabelframe", text='Clear')
                button_pycache=ttk.Button(subFrame_clear, style="Config.DK.TButton", width=10, text="Pycache")
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                button_pycache.configure(
                    command=lambda:remove_pycache(globV.progPath)
                )
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                button_pycache.pack(side=tk.TOP, padx=10, pady=(0,5))
                return subFrame_clear
            subFrame_clear=create_subFrame_clear()
            def create_subFrame_makeExe():
                subFrame_makeExe=ttk.LabelFrame(tab_devTools, style="Config.DK.TLabelframe", text='Produce Exe')
                button_makeExe=ttk.Button(subFrame_makeExe, style="Config.DK.TButton", width=10, text="PyInstaller")
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                button_makeExe.configure(
                    command=produce_exe_pyinstaller
                )
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                button_makeExe.pack(side=tk.TOP, padx=10, pady=(0,5))
                return subFrame_makeExe
            subFrame_makeExe=create_subFrame_makeExe()
            themeSelection=create_themeSelect_frame(GUIObj,tab_devTools)
            #--------------------------------------------
            # Packing & Grid Config (Tab Cfg-Basic)
            # - - - - - - - - - - - - - - - - - - - - - -
            row=0
            col=0
            subFrame_clear.grid(row=row, column=col, padx=(5,0), pady=(5,0))
            col+=1
            subFrame_makeExe.grid(row=row, column=col, padx=(5,0), pady=(5,0))
            row+=1
            col=0
            themeSelection.grid(row=row, column=col, padx=10, pady=(10,0))
            row+=1
            col=0
            #--------------------------------------------
            # Dev, Testing & Debugging
            # - - - - - - - - - - - - - - - - - - - - - -
            debugSep=ttk.Separator(tab_devTools, orient=tk.HORIZONTAL)
            debugSep.grid(row=row, column=col, columnspan=10, pady=(15,10), sticky=tk.W+tk.E)
            row+=1
            col=0
            def debugTestButton():
                GUIObj.widgets.outTabs.select(0)
                globV.HCI.switch_out(GUIObj.IOstream_std)
                globV.HCI.printStd("test test test test test test test test test test test test test test ",end="")
                globV.HCI.restore_out()
                GUIObj.widgets.text_out2.yview_moveto(1.0)
            #Button for Testing
            dbgTest_button=tk.Button(tab_devTools, text="Test")
            dbgTest_button.configure(command=debugTestButton)
            dbgTest_button.grid(row=row, column=col, padx=10, pady=10)
            return tab_devTools
        cfgTab_DevTools=create_cfgTab_DevTools()
        # - - - - - - - - - - - - - - - - - - - - - -
        # Add Tabs to the Notebook
        cfgTabs.add(cfgTab_basic, text='Basic')
        #cfgTabs.tab(0,state=tk.NORMAL)
        #cfgTabs.tab(0,style="Config.DK.TNotebook.Tab")
        #cfgTabs.tab(0,state=tk.DISABLED)
        cfgTabs.add(cfgTab_DevTools, text='Dev')
        return cfgTabs
    cfgTabs=create_cfgTabs()
    # - - - - - - - - - -
    #
    # Create User-Query Area
    # (Actually not done here, but in the middle-Test-Area in "GUI_tkinter.py"
    def create_userQuery_area():
        userQuery_area=ttk.Frame(frame_config, style="Config.DK.TFrame")
        def create_topFrame():
            topFrameBorder=ttk.Frame(userQuery_area, style="Border.Top.DK.TFrame")
            topFrame=ttk.Frame(topFrameBorder, style="Top.DK.TFrame")
            topFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=(0,5), pady=0)
            toplabel=ttk.Label(
                topFrame,
                style="Heading1.DK.TLabel",
                text="User Query/Input"
            )
            ### Sub-Frame Packing
            toplabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NW)
            return topFrameBorder
        topFrame=create_topFrame()
        text=tk.Text(userQuery_area, wrap=tk.WORD, width=25,height=6, borderwidth=0)
        button_yes=ttk.Button(userQuery_area, style="Config.DK.TButton", width=7, text="Yes")
        # button_yes.configure(command=reset_config)
        button_no=ttk.Button(userQuery_area, style="Config.DK.TButton", width=7, text="No")
        # button_no.configure(command=save_config_persistent)
        #--------------------------------------------
        # Element Configuration
        #   Maybe reconfigured after Function-Call
        # - - - - - - - - - - - - - - - - - - - - - -
        text.configure(
            font=(GUIObj.fontDefault, 12, tkfont.BOLD),
            background=GUIObj.color_txtArea_bg,
            foreground=GUIObj.color_txtArea_fg,
            selectbackground=GUIObj.color_txtArea_selectbg,
            selectforeground=GUIObj.color_txtArea_selectfg,
            state=tk.DISABLED
        )
        #--------------------------------------------
        # Packing & Grid Config
        # - - - - - - - - - - - - - - - - - - - - - -
        userQuery_area.columnconfigure(0, weight=1)
        userQuery_area.columnconfigure(1, weight=1)
        topFrame.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky=tk.NW+tk.E)
        text.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky=tk.NW+tk.SE)
        button_yes.grid(row=2, column=0, padx=0, pady=0, sticky=tk.N)
        button_no.grid(row=2, column=1, padx=0, pady=0, sticky=tk.N)
        #--------------------------------------------
        # Operation
        # - - - - - - - - - - - - - - - - - - - - - -
        GUIObj.set_outStream_query(text)
        return userQuery_area
    #userQuery_area=create_userQuery_area()
    

    #--------------------------------------------
    # Packing & Grid Config
    # - - - - - - - - - - - - - - - - - - - - - -
    # Main-Frame
    topFrame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
    cfgTabs.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
    #userQuery_area.pack(anchor=tk.SW, side=tk.BOTTOM, fill=tk.X, expand=tk.YES)
    
    return frame_config













