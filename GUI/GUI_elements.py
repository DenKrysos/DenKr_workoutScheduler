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
from DenKr_essentials_py.GUI.GUI_tkinter_basic import GUI_variables, GUI_widgets
from DenKr_essentials_py.GUI.GUI_tkinter_elements import create_themeSelect_frame
from DenKr_essentials_py.order_tidyness import remove_pycache
from DenKr_essentials_py.sort_search import search_sorted_list
from DenKr_essentials_py.GUI.GUI_assissting import KEY_GUICfgH

##Other Files for Project
##Workout-Scheduler Packages
import settings.config_handler as cfghandle
from GUI.GUI_operative_functions import GUI_Operative_Functions as guif
from GUI.GUI_operative_functions import GUI_call_makeExe, GUI_call_moveExe
from auxiliary.config_handling import cfg_runtime_writeThrough_storage, writeBack_cfghandle_to_runtime, configHandle_setup
from settings.values import equipID, muscleID, SetupExeIdx
from settings.values import BOILERPLATE as valuesBP



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
        #Some Variables to be visible across
        _create_subFrame_saveLoadReset=None
        set_muscleValues=None
        set_exerciseValues=None
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
                #
                def change_reverseOutput(*args):
                    select_bool=GUIObj.variables.cfgTabBasic.revOutput_var.get()
                    cfghandle.cfgh_rt[cfghandle.keyOutRev]=select_bool
                    guif.rewrite_computed_schedule(GUIObj)
                #GUIObj.state.stdOut_wordWrap=tk.NONE#WORD
                revOutput_label=ttk.Label(subFrameVal, style="Config.DK.TLabel", text="Reverse Output:")
                GUIObj.variables.cfgTabBasic.revOutput_var=tk.BooleanVar()
                revOutput_checkbox=ttk.Checkbutton(subFrameVal, style="Config.DK.TCheckbutton", variable=GUIObj.variables.cfgTabBasic.revOutput_var)
                #
                def change_workoutsPerWeek(event):
                    try:
                        value=GUIObj.variables.cfgTabBasic.wo_pWeek_var.get()
                        try:
                            if value.is_integer():
                                value=int(value)
                        except:
                            pass
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
                    try:
                        value=GUIObj.variables.cfgTabBasic.num_toCompute_var.get()
                        try:
                            if value.is_integer():
                                value=int(value)
                        except:
                            pass
                        cfghandle.cfgh_rt[cfghandle.keyNumComp]=value
                    except:
                        x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                        y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                        GUIObj.show_popup_simple('Not a valid number!',(x,y))
                GUIObj.variables.cfgTabBasic.num_toCompute_var=tk.IntVar()
                num_toCompute_label=ttk.Label(subFrameVal, style="Config.DK.TLabel", text="Num-To-Compute:")
                num_toCompute_entry=ttk.Entry(subFrameVal, style="Config.DK.TEntry", width=7, textvariable=GUIObj.variables.cfgTabBasic.num_toCompute_var)
                #
                def change_volumeScal(*args):
                    select_bool=GUIObj.variables.cfgTabBasic.volumeScal_var.get()
                    cfghandle.cfgh_rt[cfghandle.keyVolScal]=select_bool
                volumeScal_label=ttk.Label(subFrameVal, style="Config.DK.TLabel", text="Volume Scaling:")
                volumeScal_subFrame=ttk.Frame(subFrameVal, style="Config.DK.TFrame")
                GUIObj.variables.cfgTabBasic.volumeScal_var=tk.BooleanVar()
                volumeScal_checkbox=ttk.Checkbutton(volumeScal_subFrame, style="Config.DK.TCheckbutton", variable=GUIObj.variables.cfgTabBasic.volumeScal_var)
                volumeScal_helpButton=ttk.Button(volumeScal_subFrame, style="Config.DK.TButton", text="?")
                volumeScal_checkbox.pack(side=tk.LEFT)
                volumeScal_helpButton.pack(side=tk.RIGHT)
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
                wo_pWeek_entry.configure(
                    validate="key",
                    validatecommand=(GUIObj.cmds.validate_decimal_input,"%S","%P")
                )
                #
                GUIObj.variables.cfgTabBasic.num_toCompute_var.set(cfghandle.cfgh_rt[cfghandle.keyNumComp])
                num_toCompute_entry.bind("<KeyRelease>", change_numberWorkoutsToCompute)
                num_toCompute_entry.bind("<FocusOut>", change_numberWorkoutsToCompute)
                num_toCompute_entry.configure(
                    validate="key",
                    validatecommand=(GUIObj.cmds.validate_numeric_input,"%S","%P")
                )
                #
                GUIObj.variables.cfgTabBasic.volumeScal_var.set(cfghandle.cfgh_rt[cfghandle.keyVolScal])
                GUIObj.variables.cfgTabBasic.volumeScal_var.trace("w",change_volumeScal)
                def volumeScaling_Help():
                    GUIObj.widgets.outTabs.select(0)
                    globV.HCI.switch_out(GUIObj.IOstream_std)
                    globV.HCI.printStd("")
                    globV.HCI.printStd("This tool proposes a schedule with a certain number of Muscles to train per workout.")
                    globV.HCI.printStd("In the Setup for the Muscles \"_1cfg/setup.py\" respectively \"0history/1_2-config_setup.json\" the value 'Workouts-per-Week' can be defined for each muscle. The sum of these results in a 'Total-Muscles-per-Week'.")
                    globV.HCI.printStd("Divided by Workouts-per-Week gives the Muscles-per-Workout.")
                    globV.HCI.printStd("Most certainly, this won't result in a round integer, while the number of muscles per workout proposed in the schedule of course has to be a whole number.")
                    globV.HCI.printStd("If the Volume-Scaling is disabled, the tool bends the numbers a little, so that it can nicely work with whole numbers. In this approach, the \"Workouts-per-Week\" per muscle so-to-speak serve to provide a ratio for the muscles.")
                    globV.HCI.printStd("If the Volume-Scaling is enabled, the tools tries to achieve the Total Number by allowing itself to add an additional muscle every now and then to a workout.")
                    globV.HCI.printStd("")
                    globV.HCI.restore_out()
                volumeScal_helpButton.configure(command=volumeScaling_Help)
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
                volumeScal_label.grid(row=row, column=col, padx=(0,10), pady=(5,0), sticky=tk.E)
                col+=1
                volumeScal_subFrame.grid(row=row, column=col, padx=0, pady=(5,0), sticky=tk.W+tk.E)
                row+=1
                col=0
                return subFrameVal
            subFrame_Values=create_subFrame_values()
            #
            # - - - - - - - - - - - -
            # Sub-Frame: Saving / Loading
            def create_subFrame_saveLoadReset(parent):
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameSLR_centeringWrapper=ttk.Frame(parent, style="Config.DK.TFrame")
                subFrameSLR=ttk.Frame(subFrameSLR_centeringWrapper, style="Config.DK.TFrame")
                def save_config_persistent():
                    cfg_runtime_writeThrough_storage()
                def load_config_persistent():
                    configHandle_setup()
                    guif.set_exercise_names(GUIObj)
                    set_cfg_basic()
                    set_muscleValues()
                    #set_exerciseValues()#Triggered by setting the Filter
                    GUIObj.widgets.cfgTabExercise.filter_dropdown.current(0)
                def reset_config():#Only resets the displayed values, with what is present in the cfg_handle
                    writeBack_cfghandle_to_runtime()
                    guif.set_exercise_names(GUIObj)
                    set_cfg_basic()
                    set_muscleValues()
                    #set_exerciseValues()
                    GUIObj.widgets.cfgTabExercise.filter_dropdown.current(0)
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
                #
                subFrameSLR.pack(anchor=tk.N, side=tk.TOP)
                #
                return subFrameSLR_centeringWrapper
            nonlocal _create_subFrame_saveLoadReset
            _create_subFrame_saveLoadReset=create_subFrame_saveLoadReset
            subFrame_SaveLoad=create_subFrame_saveLoadReset(tab_cfgBasic)
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
                calendar_label=ttk.Label(calendarContainer, style="Heading2.Config.DK.TLabel", text="Date in Schedule:")
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
            # Sub-Frame: Calendar
            def create_subFrame_equipCfg():
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameEquipCfg=ttk.Frame(tab_cfgBasic, style="Config.DK.TFrame")
                # - - - - - - - - -
                equipCfg_label_frame=ttk.Frame(subFrameEquipCfg, style="Config.DK.TFrame")
                equipCfg_label=ttk.Label(equipCfg_label_frame,style="Heading2.Config.DK.TLabel",text="Equipment Capabilities:")
                equipCfg_helpButton=ttk.Button(equipCfg_label_frame, style="Config.DK.TButton", text="?")
                #
                def on_equipCfg_helpButton(event):
                    globV.HCI.printStd("")
                    globV.HCI.printStd("Equipment Capabilities:")
                    globV.HCI.printStd("- This tells, which equipment capabilities you have at your disposal to carry out your workout.")
                    globV.HCI.printStd("- The same values can be set for each exercise, where it is to be understood as \"Enabling Equipment\": Equipment that is required to perform the exercise, in the sense that having access to it grants you the capability to do.")
                    globV.HCI.printStd("    Multiple can be set simultaneously per exercise, where they are logically linked as \"or\", meaning that having one is sufficient (and not all together are required).")
                    globV.HCI.printStd("So here you select what you got and only exercises that are enabled by that equipments are included into the computation.")
                    globV.HCI.printStd("")
                equipCfg_helpButton.bind("<ButtonRelease-1>", on_equipCfg_helpButton)
                #
                equipCfg_label_frame.columnconfigure(0, weight=1)
                equipCfg_label.grid(row=0,column=0,sticky=tk.NW)
                equipCfg_helpButton.grid(row=0,column=1,sticky=tk.E)
                equipCfg_label_frame.grid(row=0,column=0,columnspan=2,pady=(0,0),sticky=tk.NW+tk.E)
                # - - - - - - - - -
                subFrameEquipCfg.columnconfigure(0, weight=0)
                subFrameEquipCfg.columnconfigure(1, weight=1)
                row=1
                col=0
                GUIObj.variables.cfgTabBasic.equipCfg_vars={}
                def update_equipCfg(key):
                    selectVal=GUIObj.variables.cfgTabBasic.equipCfg_vars[key].get()
                    cfghandle.cfgh_rt[cfghandle.keyExeEquip][key]=selectVal
                for key, val in cfghandle.cfgh_rt[cfghandle.keyExeEquip].items():
                    equipCfg_label=ttk.Label(subFrameEquipCfg, style="Config.DK.TLabel", text=key.value[1])
                    GUIObj.variables.cfgTabBasic.equipCfg_vars[key]=tk.BooleanVar()
                    GUIObj.variables.cfgTabBasic.equipCfg_vars[key].set(val)
                    volumeScal_checkbox=ttk.Checkbutton(subFrameEquipCfg, style="Config.DK.TCheckbutton", variable=GUIObj.variables.cfgTabBasic.equipCfg_vars[key])
                    volumeScal_checkbox.configure(command=lambda k=key:update_equipCfg(k))
                    equipCfg_label.grid(row=row,column=col,sticky=tk.E)
                    col+=1
                    volumeScal_checkbox.grid(row=row,column=col,padx=(5,0),sticky=tk.W)
                    row+=1
                    col=0
                return subFrameEquipCfg
            subFrameEquipCfg=create_subFrame_equipCfg()
            #
            # - - - - - - - - - - - -
            # Sub-Frame: Current Layout adjust
            def create_subFrame_layoutAdjust():
                #--------------------------------------------
                # Element definition
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameLayout=ttk.Frame(tab_cfgBasic, style="Config.DK.TFrame")
                wordWrap_label=ttk.Label(subFrameLayout, style="Config.DK.TLabel", text="StdOut Word-Wrap:")
                wordWrap_var=tk.BooleanVar()
                wordWrap_checkbox=ttk.Checkbutton(subFrameLayout, style="Config.DK.TCheckbutton", variable=wordWrap_var)
                #
                retainWinGeo_label=ttk.Label(subFrameLayout, style="Config.DK.TLabel", text="Retain Window-Geo:")
                retainWinGeo_var=tk.BooleanVar()
                retainWinGeo_checkbox=ttk.Checkbutton(subFrameLayout, style="Config.DK.TCheckbutton", variable=retainWinGeo_var)
                #
                retainWinGeo_helpButton=ttk.Button(subFrameLayout, style="Config.DK.TButton", text="?")
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                def change_wordWrap():
                    select=wordWrap_var.get()
                    if select:
                        GUIObj.state.stdOut_wordWrap=tk.WORD
                    else:
                        GUIObj.state.stdOut_wordWrap=tk.NONE
                    GUIObj.widgets.text_stdout.configure(wrap=GUIObj.state.stdOut_wordWrap)
                if tk.WORD==GUIObj.state.stdOut_wordWrap:
                    wordWrap_var.set(True)
                else:#tk.NONE
                    wordWrap_var.set(False)
                wordWrap_checkbox.configure(
                    command=change_wordWrap
                )
                #
                retainWinGeo_var.set(GUIObj.cfgHandle_rt[KEY_GUICfgH.RetainGeometry])
                def on_retainWinGeo_change(*args):
                    selectVal=retainWinGeo_var.get()
                    GUIObj.cfgHandle_rt[KEY_GUICfgH.RetainGeometry]=selectVal
                    GUIObj.cfgHandle_changed=True
                retainWinGeo_var.trace('w',on_retainWinGeo_change)
                #
                def on_retainWinGeo_helpButton(event):
                    globV.HCI.printStd("")
                    globV.HCI.printStd("»Retain Window Geometry«")
                    globV.HCI.printStd("- A mere Window/GUI Layout Option.")
                    globV.HCI.printStd("-> If checked, the window memorizes its Geometry (Size and Position) on Closing and restores them on next startup.")
                    globV.HCI.printStd("-> If disabled, the window starts up with a default size centered on the screen.")
                    globV.HCI.printStd("")
                retainWinGeo_helpButton.bind("<ButtonRelease-1>", on_retainWinGeo_helpButton)
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                subFrameLayout.columnconfigure(2, weight=1)
                row=0
                col=0
                wordWrap_label.grid(row=row, column=col, padx=(0,10), pady=(0,0), sticky=tk.E)
                col+=1
                wordWrap_checkbox.grid(row=row, column=col, padx=0, pady=(0,0), sticky=tk.W)
                row+=1
                col=0
                retainWinGeo_label.grid(row=row, column=col, padx=(0,10), pady=(0,0), sticky=tk.E)
                col+=1
                retainWinGeo_checkbox.grid(row=row, column=col, padx=0, pady=(0,0), sticky=tk.W)
                col+=1
                retainWinGeo_helpButton.grid(row=row, column=col, padx=(0,0), pady=(0,0), sticky=tk.E)
                #
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
                compute_label=ttk.Label(subFramenewComp, style="Heading1.Config.DK.TLabel", text="New Computation")
                compute_button=ttk.Button(subFramenewComp, style="Config.DK.TButton", text="Compute")
                compute_button.configure(command=button_new_computation)
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0  #@UnusedVariable
                compute_label.pack(side=tk.TOP, anchor=tk.N, padx=(0,0), pady=(0,8))
                row+=1
                col=0  #@UnusedVariable
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
                GUIObj.variables.cfgTabBasic.volumeScal_var.set(cfghandle.cfgh_rt[cfghandle.keyVolScal])
                for key, val in GUIObj.variables.cfgTabBasic.equipCfg_vars.items():
                    GUIObj.variables.cfgTabBasic.equipCfg_vars[key].set(cfghandle.cfgh_rt[cfghandle.keyExeEquip][key])
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
            equipCfgSep=ttk.Separator(tab_cfgBasic, orient=tk.HORIZONTAL)
            equipCfgSep.pack(side=tk.TOP, fill=tk.X, pady=(15,10))
            subFrameEquipCfg.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0,0))
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
            # Tab-Basics
            tab_cfgMuscle=ttk.Frame(cfgTabs, style="Config.DK.TFrame")
            # - - - - - - - - - - - -
            #Some Variables to be visible across
            GUIObj.variables.cfgTabMuscle=GUI_variables()
            GUIObj.widgets.cfgTabMuscle=GUI_widgets()
            # - - - - - - - - - - - -
            curr_selectedMuscle=None
            #
            # Sub-Frame: Select Muscle-to-edit
            def create_subFrame_muscleSelect():
                subFrame_muscleSelect=ttk.Frame(tab_cfgMuscle, style="Config.DK.TFrame")
                #--------------------------------------------
                # Element Definition
                # - - - - - - - - - - - - - - - - - - - - - -
                GUIObj.variables.cfgTabMuscle.muscleSelect=tk.StringVar()
                muscleSelect_label=ttk.Label(subFrame_muscleSelect, style="Heading1.Config.DK.TLabel", text="Muscle:")
                muscleSelect_dropdown=ttk.Combobox(subFrame_muscleSelect, style="Config.DK.TCombobox", textvariable=GUIObj.variables.cfgTabMuscle.muscleSelect, state="readonly")
                #
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                muscleSelect_dropdown.configure(height=25)
                def _curr_selectedMuscle():
                    idx=muscleSelect_idxMap[GUIObj.variables.cfgTabMuscle.muscleSelect.get()]
                    muscle=cfghandle.cfgSetup_rt[cfghandle.keySetupMuscle][idx]
                    return idx, muscle
                nonlocal curr_selectedMuscle
                curr_selectedMuscle=_curr_selectedMuscle
                #
                muscleSelect_idxMap={}
                for i, muscle in enumerate(cfghandle.cfgSetup_rt[cfghandle.keySetupMuscle]):
                    muscleSelect_idxMap[muscle[0].value[1]]=i
                def on_muscleSelect(*args):
                    _, muscle=curr_selectedMuscle()
                    wo_pWeek_val=muscle[2]
                    sets_pWeek_val=muscle[3]
                    # try:
                    #     formatted_value="{:.0f}".format(wo_pWeek_val) if wo_pWeek_val.is_integer() else f"{wo_pWeek_val}"
                    #     GUIObj.widgets.cfgTabMuscle.muscleSelect_wo_pWeek_entry.delete(0,tk.END)
                    #     GUIObj.widgets.cfgTabMuscle.muscleSelect_wo_pWeek_entry.insert(tk.END,formatted_value)
                    # except:
                    #     GUIObj.variables.cfgTabMuscle.wo_pWeek_var.set(wo_pWeek_val)
                    # try:
                    #     formatted_value="{:.0f}".format(sets_pWeek_val) if sets_pWeek_val.is_integer() else f"{sets_pWeek_val}"
                    #     GUIObj.widgets.cfgTabMuscle.muscleSelect_sets_pWeek_entry.delete(0,tk.END)
                    #     GUIObj.widgets.cfgTabMuscle.muscleSelect_sets_pWeek_entry.insert(0,formatted_value)
                    # except:
                    #     GUIObj.variables.cfgTabMuscle.sets_pWeek_var.set(sets_pWeek_val)
                    try:
                        if wo_pWeek_val.is_integer():
                            wo_pWeek_val=int(wo_pWeek_val)
                    except:
                        pass
                    GUIObj.variables.cfgTabMuscle.wo_pWeek_var.set(wo_pWeek_val)
                    try:
                        if sets_pWeek_val.is_integer():
                            sets_pWeek_val=int(sets_pWeek_val)
                    except:
                        pass
                    GUIObj.variables.cfgTabMuscle.sets_pWeek_var.set(sets_pWeek_val)
                muscleSelect_dropdown.configure(values=list(muscleSelect_idxMap.keys()))
                muscleSelect_dropdown.current(0)
                muscleSelect_dropdown.bind("<<ComboboxSelected>>", on_muscleSelect)
                nonlocal set_muscleValues
                set_muscleValues=on_muscleSelect
                #
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                subFrame_muscleSelect.columnconfigure(0, weight=1)
                muscleSelect_label.grid(row=row, column=col, padx=0, pady=(10,0), sticky=tk.N)
                row+=1
                muscleSelect_dropdown.grid(row=row, column=col, padx=0, pady=(10,0), sticky=tk.N)
                row+=1
                col=0
                #
                return subFrame_muscleSelect
            subFrame_muscleSelect=create_subFrame_muscleSelect()
            # - - - - - - - - - - - -
            #
            # Sub-Frame: Values-per-Muscle
            def create_subFrame_valPerMuscle():
                subFrame_valPerMuscle=ttk.Frame(tab_cfgMuscle, style="Config.DK.TFrame")
                #--------------------------------------------
                # Element Definition
                # - - - - - - - - - - - - - - - - - - - - - -
                nonlocal curr_selectedMuscle
                muscleSelect_wo_pWeek_label=ttk.Label(subFrame_valPerMuscle, style="Config.DK.TLabel", text="WorkoutsPerWeek:")
                GUIObj.variables.cfgTabMuscle.wo_pWeek_var=tk.DoubleVar()
                muscleSelect_wo_pWeek_entry=ttk.Entry(subFrame_valPerMuscle, style="Config.DK.TEntry", width=7, textvariable=GUIObj.variables.cfgTabMuscle.wo_pWeek_var, state=tk.NORMAL)
                muscleSelect_sets_pWeek_label=ttk.Label(subFrame_valPerMuscle, style="Config.DK.TLabel", text="Sets-per-Week:")
                GUIObj.variables.cfgTabMuscle.sets_pWeek_var=tk.DoubleVar()
                muscleSelect_sets_pWeek_entry=ttk.Entry(subFrame_valPerMuscle, style="Config.DK.TEntry", width=7, textvariable=GUIObj.variables.cfgTabMuscle.sets_pWeek_var, state=tk.NORMAL)
                #
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                def change_workoutsPerWeek_muscle(event):
                    try:
                        value=GUIObj.variables.cfgTabMuscle.wo_pWeek_var.get()
                        try:
                            if value.is_integer():
                                value=int(value)
                        except:
                            pass
                        _, muscle=curr_selectedMuscle()
                        muscle[2]=value
                    except:
                        x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                        y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                        GUIObj.show_popup_simple('Not a valid number!',(x,y))
                muscleSelect_wo_pWeek_entry.bind("<KeyRelease>", change_workoutsPerWeek_muscle)
                muscleSelect_wo_pWeek_entry.bind("<FocusOut>", change_workoutsPerWeek_muscle)
                muscleSelect_wo_pWeek_entry.configure(
                    validate="key",
                    validatecommand=(GUIObj.cmds.validate_decimal_input,"%S","%P")
                )
                #
                def change_setsPerWeek(event):
                    try:
                        value=GUIObj.variables.cfgTabMuscle.sets_pWeek_var.get()
                        try:
                            if value.is_integer():
                                value=int(value)
                        except:
                            pass
                        _, muscle=curr_selectedMuscle()
                        muscle[3]=value
                    except:
                        x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                        y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                        GUIObj.show_popup_simple('Not a valid number!',(x,y))
                muscleSelect_sets_pWeek_entry.bind("<KeyRelease>", change_setsPerWeek)
                muscleSelect_sets_pWeek_entry.bind("<FocusOut>", change_setsPerWeek)
                muscleSelect_sets_pWeek_entry.configure(
                    validate="key",
                    validatecommand=(GUIObj.cmds.validate_decimal_input,"%S","%P")
                )
                #
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                muscleSelect_wo_pWeek_label.grid(row=row, column=col, padx=(0,10), pady=(10,0), sticky=tk.N)
                col+=1
                muscleSelect_wo_pWeek_entry.grid(row=row, column=col, padx=0, pady=(10,0), sticky=tk.N)
                row+=1
                col=0
                muscleSelect_sets_pWeek_label.grid(row=row, column=col, padx=(0,10), pady=(10,0), sticky=tk.N)
                col+=1
                muscleSelect_sets_pWeek_entry.grid(row=row, column=col, padx=0, pady=(10,0), sticky=tk.N)
                row+=1
                col=0
                return subFrame_valPerMuscle
            subFrame_valPerMuscle=create_subFrame_valPerMuscle()
            #
            set_muscleValues()
            #
            # - - - - - - - - - - - -
            nonlocal _create_subFrame_saveLoadReset
            subFrame_SaveLoad=_create_subFrame_saveLoadReset(tab_cfgMuscle)
            # - - - - - - - - - - - -
            #
            # Sub-Frame: Values-per-Muscle
            def create_subFrame_muscleHelp():
                subFrame_muscleHelp=ttk.Frame(tab_cfgMuscle, style="Config.DK.TFrame")
                #--------------------------------------------
                # Element Definition
                # - - - - - - - - - - - - - - - - - - - - - -
                button_muscle_help=ttk.Button(subFrame_muscleHelp, style="Config.DK.TButton", width=7, text="Info")
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                def muscleSetup_helpButton():
                    GUIObj.widgets.outTabs.select(0)
                    globV.HCI.switch_out(GUIObj.IOstream_std)
                    globV.HCI.printStd("")
                    globV.HCI.printStd("The preset values of the initally shipped Muscle-profile works reasonably well for having 3.5 Workouts-per-Week with 4 Muscles per Workout.")
                    globV.HCI.printStd("But actually, this is a little too low Volume. The Profile in \"muscle.py\" called \"muscle_setup_default\" would be more like the optimum volume. But this would require about 5-6 Muscles per Workout or 4-5 Workouts-per-Week, which would be most likely too much a dedication for most people.")
                    globV.HCI.printStd("So you might very well work with this profile here and still live on with a good and calm conscience.")
                    globV.HCI.printStd("Furthermore, now you can consider making use of the \"Volume Scaling\" Option, which allows the computation to include an additional muscle every now and then.")
                    globV.HCI.printStd("I would assess that leaving the values like initially set works well with deactivated Volume-Scaling.")
                    globV.HCI.printStd("Active Volume-Scaling might add a fifth muscle too often for many people. So, when using the option, you might want to lower Chest-&-Back to 1.55, Lower-back to 0.75, Quads&Glutes to 1.4.")
                    globV.HCI.printStd("")
                    globV.HCI.restore_out()
                button_muscle_help.configure(command=muscleSetup_helpButton)
                #--------------------------------------------
                button_muscle_help.pack(side=tk.TOP, anchor=tk.N)
                return subFrame_muscleHelp
            subFrame_muscleHelp=create_subFrame_muscleHelp()
            #
            #--------------------------------------------
            # Packing & Grid Config
            # - - - - - - - - - - - - - - - - - - - - - -
            subFrame_muscleSelect.pack(side=tk.TOP, fill=tk.X)
            subFrame_valPerMuscle.pack(side=tk.TOP, fill=tk.X)
            saveSep=ttk.Separator(tab_cfgMuscle, orient=tk.HORIZONTAL)
            saveSep.pack(side=tk.TOP, fill=tk.X, pady=(15,10))
            subFrame_SaveLoad.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0,0))
            helpSep=ttk.Separator(tab_cfgMuscle, orient=tk.HORIZONTAL)
            helpSep.pack(side=tk.TOP, fill=tk.X, pady=(60,10))
            subFrame_muscleHelp.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0,0))
            #
            return tab_cfgMuscle
        cfgTab_muscle=create_cfgTab_muscle()
        #
        # Tab: Config Muscles
        def create_cfgTab_exercise():
            # Tab-Basics
            cfgTab_exercise=ttk.Frame(cfgTabs, style="Config.DK.TFrame")
            # - - - - - - - - - - - -
            #Some Variables to be visible across
            GUIObj.variables.cfgTabExercise=GUI_variables()
            GUIObj.widgets.cfgTabExercise=GUI_widgets()
            #
            GUIObj.variables.cfgTabExercise.Intensity_vars=[]#Herein Lists are stored that each contain [MuscleID, Intensity]
            GUIObj.widgets.cfgTabExercise.Intensity_wids=[]
            # - - - - - - - - - - - -
            curr_selectedExe=None
            #
            # Sub-Frame: Select Muscle-to-edit
            def create_subFrame_exeSelect():
                subFrame_exeSelect=ttk.Frame(cfgTab_exercise, style="Config.DK.TFrame")
                #--------------------------------------------
                # Element Definition
                # - - - - - - - - - - - - - - - - - - - - - -
                GUIObj.variables.cfgTabExercise.exeFilter=tk.StringVar()
                filter_label=ttk.Label(subFrame_exeSelect, style="Config.DK.TLabel", text="Filter:")
                filter_dropdown=ttk.Combobox(subFrame_exeSelect, style="Config.DK.TCombobox", textvariable=GUIObj.variables.cfgTabExercise.exeFilter, state="readonly")
                GUIObj.widgets.cfgTabExercise.filter_dropdown=filter_dropdown
                #
                GUIObj.variables.cfgTabExercise.exeSelect=tk.StringVar()
                exeSelect_labelFrame=ttk.Frame(subFrame_exeSelect, style="Config.DK.TFrame")
                exeSelect_label=ttk.Label(exeSelect_labelFrame, style="Heading1.Config.DK.TLabel", text="Exercise:")
                exeSelect_dropdown=ttk.Combobox(subFrame_exeSelect, style="exeSelect.Config.DK.TCombobox", width=28, textvariable=GUIObj.variables.cfgTabExercise.exeSelect, state="readonly")
                GUIObj.widgets.cfgTabExercise.exeSelect_dropdown=exeSelect_dropdown
                #
                GUIObj.variables.cfgTabExercise.displayExeName=ttk.Label(subFrame_exeSelect, style="Text.Config.DK.TLabel")
                #
                exeSelect_addRemButtons=ttk.Frame(exeSelect_labelFrame, style="Config.DK.TFrame")
                exeSelect_minus_button=ttk.Button(exeSelect_addRemButtons, style="Groove.Config.DK.TButton", width=3, text="-")
                exeSelect_plus_button=ttk.Button(exeSelect_addRemButtons, style="Ridge.Config.DK.TButton", width=3, text="+")
                exeSelect_minus_button.grid(row=0,column=0)
                exeSelect_plus_button.grid(row=0,column=1,padx=(3,0))
                #
                exeSelect_labelFrame.columnconfigure(0, weight=1)
                exeSelect_label.grid(row=0,column=0,sticky=tk.N)
                exeSelect_addRemButtons.grid(row=0,column=1,padx=(0,5),sticky=tk.SE)
                #
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                GUIObj.ttkStyle.configure("exeSelect.Config.DK.TCombobox", postoffset=(0,0,200,0))
                filter_dropdown.configure(height=25)
                exeSelect_dropdown.configure(height=25)
                GUIObj.variables.cfgTabExercise.displayExeName.configure(wraplength=190)
                def _curr_selectedFilter():
                    filterVal=GUIObj.variables.cfgTabExercise.exeFilter.get()
                    if '<ALL>'==filterVal:
                        muscle=None
                    else:
                        idxMuscle=filterMuscle_idxMap[filterVal]
                        muscle=cfghandle.cfgSetup_rt[cfghandle.keySetupMuscle][idxMuscle]
                    return muscle
                def _curr_selectedExe():
                    select=GUIObj.variables.cfgTabExercise.exeSelect.get()
                    if ''==select:
                        idx=None
                        exe=None
                    else:
                        idx=exeSelect_idxMap[select]
                        exe=cfghandle.cfgSetup_rt[cfghandle.keySetupExe][idx]
                    return idx, exe
                exeSelect_idxMap={}
                #
                filterMuscle_idxMap={}
                def set_filterSelect_items():
                    nonlocal filterMuscle_idxMap
                    filterMuscle_idxMap={'<ALL>':0}
                    i=0
                    for muscle in cfghandle.cfgSetup_rt[cfghandle.keySetupMuscle]:
                        filterMuscle_idxMap[muscle[0].value[1]]=i
                        i+=1
                    filterMuscle_idxMap['<ALL>']=i
                set_filterSelect_items()
                def on_filterMuscleSelect(*args):
                    set_exeSelect_items()
                    exeSelect_dropdown_items=exeSelect_dropdown['values']
                    if 0<len(exeSelect_dropdown_items):
                        exeSelect_dropdown.current(0)
                    else:
                        GUIObj.variables.cfgTabExercise.exeSelect.set('')
                        set_exerciseValues()
                filter_dropdown.configure(values=list(filterMuscle_idxMap.keys()))
                filter_dropdown.current(0)
                #filter_dropdown.bind("<<ComboboxSelected>>", on_filterMuscleSelect)
                GUIObj.variables.cfgTabExercise.exeFilter.trace("w", on_filterMuscleSelect)
                #
                nonlocal curr_selectedExe
                curr_selectedExe=_curr_selectedExe
                #
                def set_exeSelect_items():
                    nonlocal exeSelect_idxMap
                    exeSelect_idxMap={}
                    filterMus=_curr_selectedFilter()
                    if filterMus is None:
                        for i, exe in enumerate(cfghandle.cfgSetup_rt[cfghandle.keySetupExe]):
                            exeSelect_idxMap[exe[SetupExeIdx.NAME]]=i
                    else:
                        filterMus=filterMus[0]
                        for i, exe in enumerate(cfghandle.cfgSetup_rt[cfghandle.keySetupExe]):
                            intensities=exe[SetupExeIdx.INTENSITY]
                            for intens in intensities:
                                if intens[0]==filterMus:
                                    exeSelect_idxMap[exe[SetupExeIdx.NAME]]=i
                                    break
                    exeSelect_dropdown.configure(values=list(exeSelect_idxMap.keys()))
                set_exeSelect_items()
                #
                def on_exeSelect(*args):
                    destroy_subFrame_exeEquip()
                    destroy_subFrame_exeIntensity()
                    GUIObj.widgets.cfgTabExercise.exeName_ent.grid_forget()
                    GUIObj.widgets.cfgTabExercise.exeName_ent.configure(style="Config.DK.TEntry")
                    GUIObj.widgets.cfgTabExercise.exeInherent_label.grid_forget()
                    _, exe=curr_selectedExe()
                    if exe is None:
                        GUIObj.set_txt_label_widget(GUIObj.variables.cfgTabExercise.displayExeName,'')
                        GUIObj.variables.cfgTabExercise.exeName_var.set('')
                        GUIObj.variables.cfgTabExercise.exeActive_var.set(0)
                        GUIObj.variables.cfgTabExercise.exePrecedence_var.set('')
                    else:
                        if 1==exe[SetupExeIdx.INHERENT]:
                            GUIObj.widgets.cfgTabExercise.exeInherent_label.grid_cmd()
                        else:
                            GUIObj.widgets.cfgTabExercise.exeName_ent.grid_cmd()
                        GUIObj.set_txt_label_widget(GUIObj.variables.cfgTabExercise.displayExeName,exe[SetupExeIdx.NAME])
                        GUIObj.variables.cfgTabExercise.exeName_var.set(exe[SetupExeIdx.NAME])
                        GUIObj.variables.cfgTabExercise.exeActive_var.set(exe[SetupExeIdx.ENABLED])
                        exePrecedence_val=exe[SetupExeIdx.PRECEDENCE]
                        try:
                            if exePrecedence_val.is_integer():
                                exePrecedence_val=int(exePrecedence_val)
                        except:
                            pass
                        GUIObj.variables.cfgTabExercise.exePrecedence_var.set(exePrecedence_val)
                        set_subFrame_exeEquip()
                        set_subFrame_exeIntensity()
                exeSelect_dropdown.current(0)
                #exeSelect_dropdown.bind("<<ComboboxSelected>>", on_exeSelect)
                GUIObj.variables.cfgTabExercise.exeSelect.trace("w", on_exeSelect)
                nonlocal set_exerciseValues
                set_exerciseValues=on_exeSelect
                #
                def on_add_exercise(event):
                    new=valuesBP.empty_exercise()
                    guif.set_exercise_names(GUIObj)
                    i=2
                    while not -1==search_sorted_list(GUIObj.state.exe_names, new[SetupExeIdx.NAME]):
                        new[SetupExeIdx.NAME]=f"<new{i}>"
                        i+=1
                    cfghandle.cfgSetup_rt[cfghandle.keySetupExe].append(new)
                    GUIObj.widgets.cfgTabExercise.filter_dropdown.current(0)
                    allItems=GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.cget('values')
                    GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.current(len(allItems)-1)
                    guif.set_exercise_names(GUIObj)
                def on_rem_exercise(event):
                    def rem_exercise_do():
                        exeIdx, exe=curr_selectedExe()
                        curFilterSelect=GUIObj.widgets.cfgTabExercise.filter_dropdown.current()
                        curExeSelect=GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.current()
                        cfghandle.cfgSetup_rt[cfghandle.keySetupExe].pop(exeIdx)
                        GUIObj.widgets.cfgTabExercise.filter_dropdown.current(curFilterSelect)
                        exeItems=GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.cget('values')
                        if len(exeItems)>curExeSelect:
                            GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.current(curExeSelect)
                        else:
                            GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.current(len(exeItems)-1)
                    def rem_exercise_popup():
                        x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                        y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                        # »Remove currently selected Exercise?«
                        #  (? See StdOut-Area)
                        GUIObj.show_popup_simple('»Exercise removed«\n(See StdOut-Area)',(x,y))
                    def rem_exercise_printInfo():
                        globV.HCI.printErr("- Remark that changes are not persistent until clicked on \"Save\".")
                        globV.HCI.printErr("     (Otherwise, they do only affect the current runtime, but don't alter Files.)")
                        globV.HCI.printErr("- Removing an exercise will only remove it from the .json-Storage-File (besides the current runtime).")
                        globV.HCI.printErr("- If the exercise is pre-shipped with the Application's internal database (Inherent Exercise), it'll come back into computation with next startup and will be added again to the .json-File on subsequent \"Save\" with default values.")
                        globV.HCI.printErr("- If you intend to remove the exercise from your Schedule computation, consider just disabling its \"Enabled\" Flag.")
                        globV.HCI.printErr("- Custom added Exercises are solely kept persistent in the .json-File.")
                        globV.HCI.printErr("     (Hence, removed such ones will be unrevocably lost upon \"Saving\".")
                    rem_exercise_printInfo()
                    rem_exercise_popup()
                    rem_exercise_do()
                exeSelect_plus_button.bind("<ButtonRelease-1>", on_add_exercise)
                exeSelect_minus_button.bind("<ButtonRelease-1>", on_rem_exercise)
                #
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                subFrame_exeSelect.columnconfigure(0, weight=1)
                subFrame_exeSelect.columnconfigure(1, weight=1)
                filter_label.grid(row=row, column=col, padx=0, pady=(15,0), sticky=tk.N)
                col+=1
                filter_dropdown.grid(row=row, column=col, padx=0, pady=(15,0), sticky=tk.N)
                row+=1
                col=0
                exeSelect_labelFrame.grid(row=row, column=col, columnspan=2, padx=0, pady=(10,0), sticky=tk.NW+tk.E)
                row+=1
                exeSelect_dropdown.grid(row=row, column=col, columnspan=2, padx=0, pady=(10,0), sticky=tk.N)
                row+=1
                col=0
                GUIObj.variables.cfgTabExercise.displayExeName.grid(row=row, column=col, columnspan=2, padx=0, pady=(10,0), sticky=tk.NW+tk.E)
                row+=1
                col=0
                #
                return subFrame_exeSelect
            subFrame_exeSelect=create_subFrame_exeSelect()
            #
            # Sub-Frame: Select Muscle-to-edit
            def create_subFrame_exeVal():
                subFrame_exeVal=ttk.Frame(cfgTab_exercise, style="Config.DK.TFrame")
                #--------------------------------------------
                # Element Definition
                # - - - - - - - - - - - - - - - - - - - - - -
                GUIObj.variables.cfgTabExercise.exeName_var=tk.StringVar()
                exeName_ent=ttk.Entry(subFrame_exeVal, style="Config.DK.TEntry", width=30, textvariable=GUIObj.variables.cfgTabExercise.exeName_var)
                GUIObj.widgets.cfgTabExercise.exeName_ent=exeName_ent
                #
                exeInherent_label_frame=ttk.Frame(subFrame_exeVal, style="Config.DK.TFrame")
                exeInherent_label=ttk.Label(exeInherent_label_frame, style="Italic.Config.DK.TLabel", text="Inherent Exercise")
                exeInherent_label_helpButton=ttk.Button(exeInherent_label_frame, style="Flat.Config.DK.TButton", width=1, text="?")
                exeInherent_label_frame.columnconfigure(1, weight=1)
                exeInherent_label_helpButton.grid(row=0,column=0,padx=(5,0),sticky=tk.W)
                exeInherent_label.grid(row=0,column=1,sticky=tk.N)
                GUIObj.widgets.cfgTabExercise.exeInherent_label=exeInherent_label_frame
                #
                exeActive_label=ttk.Label(subFrame_exeVal, style="Config.DK.TLabel", text="Enabled:")
                GUIObj.variables.cfgTabExercise.exeActive_var=tk.BooleanVar()
                exeActive_checkbox=ttk.Checkbutton(subFrame_exeVal, style="Config.DK.TCheckbutton", variable=GUIObj.variables.cfgTabExercise.exeActive_var)
                #
                exePrecedence_label=ttk.Label(subFrame_exeVal, style="Config.DK.TLabel", text="Precedence:")
                GUIObj.variables.cfgTabExercise.exePrecedence_var=tk.DoubleVar()
                GUIObj.widgets.cfgTabExercise.exePrecedence_entry=ttk.Entry(subFrame_exeVal, style="Config.DK.TEntry", width=7, textvariable=GUIObj.variables.cfgTabExercise.exePrecedence_var, state=tk.NORMAL)
                #
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                def change_exeName(exe,name):
                    #Check for duplicate
                    if -1==search_sorted_list(GUIObj.state.exe_names,name):
                        exe[SetupExeIdx.NAME]=name
                        return 0
                    else:
                        return -1
                # def focusIn_exeName(event):
                #     _, exe=curr_selectedExe()
                #     event.widget.oldName=exe[SetupExeIdx.NAME]
                def focusOut_exeName(event):
                    _, exe=curr_selectedExe()
                    name=GUIObj.variables.cfgTabExercise.exeName_var.get()
                    if name==exe[SetupExeIdx.NAME]:
                        return
                    else:
                        err=change_exeName(exe,name)
                        if 0==err:
                            exeName_ent.configure(style="Config.DK.TEntry")
                            #To update the Dropdown-List of the Exercises with the new name
                            curFilterSelect=GUIObj.widgets.cfgTabExercise.filter_dropdown.current()
                            curExeSelect=GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.current()
                            GUIObj.widgets.cfgTabExercise.filter_dropdown.current(curFilterSelect)
                            GUIObj.widgets.cfgTabExercise.exeSelect_dropdown.current(curExeSelect)
                            guif.set_exercise_names(GUIObj)
                            return
                        else:
                            exeName_ent.configure(style="Error.Config.DK.TEntry")
                            x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                            y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                            GUIObj.show_popup_simple('Duplicate!\nExercise-Name already existent.',(x,y))
                #exeName_ent.bind("<KeyRelease>", change_exeName)
                #exeName_ent.bind("<FocusIn>", focusIn_exeName)
                exeName_ent.bind("<FocusOut>", focusOut_exeName)
                def change_exeEnabled(*args):
                    _, exe=curr_selectedExe()
                    if not exe is None:
                        select_bool=GUIObj.variables.cfgTabExercise.exeActive_var.get()
                        exe[SetupExeIdx.ENABLED]=select_bool
                GUIObj.variables.cfgTabExercise.exeActive_var.trace("w",change_exeEnabled)
                #
                def change_exePrecedence(event):
                    try:
                        value=GUIObj.variables.cfgTabExercise.exePrecedence_var.get()
                        try:
                            if value.is_integer():
                                value=int(value)
                        except:
                            pass
                        _, exe=curr_selectedExe()
                        if not exe is None:
                            exe[SetupExeIdx.PRECEDENCE]=value
                    except:
                        x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                        y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                        GUIObj.show_popup_simple('Not a valid number!',(x,y))
                GUIObj.widgets.cfgTabExercise.exePrecedence_entry.bind("<KeyRelease>", change_exePrecedence)
                GUIObj.widgets.cfgTabExercise.exePrecedence_entry.bind("<FocusOut>", change_exePrecedence)
                GUIObj.widgets.cfgTabExercise.exePrecedence_entry.configure(
                    validate="key",
                    validatecommand=(GUIObj.cmds.validate_decimal_input,"%S","%P")
                )
                #
                def on_exeInherent_helpButton(event):
                    globV.HCI.printStd("")
                    globV.HCI.printStd("»Inherent Exercise:«")
                    globV.HCI.printStd("- Means that the Exercise comes shipped and pre-configured with the Application.")
                    globV.HCI.printStd("    (Default Values are always available within the App.)")
                    globV.HCI.printStd("- You can change it's values.")
                    globV.HCI.printStd("- You cannot really delete the Exercise: When doing anyways, it'll come back on next startup with default values (and will be saved again to .json-File Persistent-Storage upon subsequent \"Save\").")
                    globV.HCI.printStd("- In case you don't want to have the Exercise in your Schedule Computation, just unset it's \"Enabled\" flag.")
                    globV.HCI.printStd("")
                exeInherent_label_helpButton.bind("<ButtonRelease-1>", on_exeInherent_helpButton)
                #
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                row=0
                col=0
                subFrame_exeVal.columnconfigure(0, weight=1)
                subFrame_exeVal.columnconfigure(1, weight=1)
                exeName_ent.grid_cmd=lambda cmdRow=row,cmdCol=col:exeName_ent.grid(row=cmdRow, column=cmdCol, columnspan=2, padx=0, pady=(10,0), sticky=tk.N)
                GUIObj.widgets.cfgTabExercise.exeInherent_label.grid_cmd=lambda cmdRow=row,cmdCol=col:GUIObj.widgets.cfgTabExercise.exeInherent_label.grid(row=cmdRow, column=cmdCol, columnspan=2, padx=0, pady=(6,0), sticky=tk.NW+tk.E)
                row+=1
                exeActive_label.grid(row=row, column=col, padx=(0,10), pady=(10,0), sticky=tk.E)
                col+=1
                exeActive_checkbox.grid(row=row, column=col, padx=0, pady=(10,0), sticky=tk.W)
                row+=1
                col=0
                exePrecedence_label.grid(row=row, column=col, padx=(0,10), pady=(5,0), sticky=tk.E)
                col+=1
                GUIObj.widgets.cfgTabExercise.exePrecedence_entry.grid(row=row, column=col, padx=0, pady=(5,0), sticky=tk.W)
                row+=1
                col=0
                #
                return subFrame_exeVal
            subFrame_exeVal=create_subFrame_exeVal()
            #
            # Sub-Frame: Select Muscle-to-edit
            ###    persistent Data for it
            exeEquip_enumMap={}
            for equ in equipID:
                exeEquip_enumMap[equ.value[1]]=equ
            ###   Function to dynamically (re)-create it
            def create_subFrame_exeEquip():
                subFrame_exeEquip=ttk.Frame(cfgTab_exercise, style="Config.DK.TFrame")
                lFrame_exeEquip=ttk.LabelFrame(subFrame_exeEquip, style="Config.DK.TLabelframe", text='Enabling Equipment')
                add_exeEquip_Button=ttk.Button(lFrame_exeEquip, style="Ridge.Config.DK.TButton", width=2, text="+")
                GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance=[]
                GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance.append(subFrame_exeEquip)
                GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance.append(lFrame_exeEquip)
                GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance.append(add_exeEquip_Button)
                #--------------------------------------------
                # Element Definition
                # - - - - - - - - - - - - - - - - - - - - - -
                nonlocal exeEquip_enumMap
                #We need multiple sub-lists to store: Line-Frame, Dropdown, Remove-Button
                #  (Less space in the variable-area required)
                GUIObj.variables.cfgTabExercise.Equip_vars=[[]]
                GUIObj.widgets.cfgTabExercise.Equip_wids=[[],[],[]]
                subListCBox=0
                subListButton=1
                subListLF=2
                #
                def on_exeEquipSelect(event):
                    selectEqu=event.widget.get()
                    selectVal=exeEquip_enumMap[selectEqu]
                    _, exe=curr_selectedExe()
                    exe[SetupExeIdx.EQUIPMENT][event.widget.widget_idx]=selectVal
                #
                _, exe=curr_selectedExe()
                def _add_widget_and_var(i):
                    lineFrame=ttk.Frame(lFrame_exeEquip, style="Config.DK.TFrame")
                    GUIObj.widgets.cfgTabExercise.Equip_wids[subListLF].append(lineFrame)
                    equip=exe[SetupExeIdx.EQUIPMENT][i]
                    var=tk.StringVar()
                    cbox=ttk.Combobox(lineFrame, style="Config.DK.TCombobox", height=25, textvariable=var, state="readonly")
                    cbox.widget_idx=i
                    cbox.configure(values=list(exeEquip_enumMap.keys()))
                    for j, item in enumerate(cbox['values']):
                        if item==equip.value[1]:
                            cbox.current(j)
                            break
                    cbox.bind("<<ComboboxSelected>>", on_exeEquipSelect)
                    rem_exeEquip_Button=ttk.Button(lineFrame, style="Groove.Config.DK.TButton", width=2, text="-")
                    rem_exeEquip_Button.widget_idx=i
                    def on_rem_exeEquip(event):
                        _, exe=curr_selectedExe()
                        exe[SetupExeIdx.EQUIPMENT].pop(event.widget.widget_idx)
                        GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance[2].pack_forget()
                        subFrame_exeEquip_destroyWidgets_startingAt(event.widget.widget_idx)
                        _create_widgets_startingAt(event.widget.widget_idx)
                        GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance[2].pack_cmd()
                    rem_exeEquip_Button.bind("<ButtonRelease-1>", on_rem_exeEquip)
                    #
                    GUIObj.variables.cfgTabExercise.Equip_vars[subListCBox].append(var)
                    GUIObj.widgets.cfgTabExercise.Equip_wids[subListCBox].append(cbox)
                    GUIObj.widgets.cfgTabExercise.Equip_wids[subListButton].append(rem_exeEquip_Button)
                    #
                    cbox.grid(row=0,column=0,padx=(0,3),pady=(0,0),sticky=tk.E)
                    rem_exeEquip_Button.grid(row=0,column=1,padx=(0,0),pady=(0,0),sticky=tk.W)
                    lineFrame.pack(anchor=tk.N, side=tk.TOP, padx=(4,4), pady=(2,3))
                def _create_widgets_startingAt(index):
                    for i in range(index,len(exe[SetupExeIdx.EQUIPMENT])):
                        _add_widget_and_var(i)
                #
                _create_widgets_startingAt(0)
                #
                def on_add_exeEquip(event):
                    _, exe=curr_selectedExe()
                    exe[SetupExeIdx.EQUIPMENT].append(equipID.undef)
                    event.widget.pack_forget()
                    _add_widget_and_var(len(exe[SetupExeIdx.EQUIPMENT])-1)
                    event.widget.pack_cmd()
                #
                add_exeEquip_Button.bind("<ButtonRelease-1>", on_add_exeEquip)
                #
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                # lFrame_exeEquip.columnconfigure(0, weight=1)
                # lFrame_exeEquip.rowconfigure(0, weight=1)
                # lFrame_exeEquip.rowconfigure(1, weight=0)
                add_exeEquip_Button.pack_cmd=lambda:add_exeEquip_Button.pack(anchor=tk.N, side=tk.TOP, pady=(2,3))
                add_exeEquip_Button.pack_cmd()
                #
                # lFrame_exeEquip.pack(anchor=tk.N, side=tk.TOP, pady=(10,0))
                subFrame_exeEquip.columnconfigure(0, weight=1)
                subFrame_exeEquip.columnconfigure(1, weight=1)
                subFrame_exeEquip.rowconfigure(0, weight=1)
                lFrame_exeEquip.grid(row=0,column=0,rowspan=2,padx=(0,3),sticky=tk.NE)
                #
                return subFrame_exeEquip
            def set_subFrame_exeEquip():
                subFrame_exeEquip=create_subFrame_exeEquip()
                subFrame_exeEquip.grid(row=GUIObj.variables.cfgTabExercise.Row_subFrame_exeEquip, column=col, pady=(10,0), sticky=tk.NW+tk.E)
            def subFrame_exeEquip_destroyWidgets_startingAt(index):
                for i, sublist in enumerate(GUIObj.widgets.cfgTabExercise.Equip_wids):
                    for j in range(index,len(sublist)):
                        widget=sublist[j]
                        widget.destroy()
                    GUIObj.widgets.cfgTabExercise.Equip_wids[i]=sublist[0:index]
                for i, sublist in enumerate(GUIObj.variables.cfgTabExercise.Equip_vars):
                    for j in range(index,len(sublist)):
                        var=sublist[j]
                        #var.set('')
                        del var
                    GUIObj.variables.cfgTabExercise.Equip_vars[i]=sublist[0:index]
            def destroy_subFrame_exeEquip():
                if hasattr(GUIObj.widgets.cfgTabExercise,'Equip_wids_singleInstance'):
                    for widget in GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance:
                        # widget.pack_forget()
                        widget.destroy()
                    subFrame_exeEquip_destroyWidgets_startingAt(0)
                    del GUIObj.widgets.cfgTabExercise.Equip_wids_singleInstance
                    del GUIObj.variables.cfgTabExercise.Equip_vars
                    del GUIObj.widgets.cfgTabExercise.Equip_wids
            #
            # Sub-Frame: Select Muscle-to-edit
            ###    persistent Data for it
            exeIntens_enumMap={}
            for mus in muscleID:
                exeIntens_enumMap[mus.value[1]]=mus
            ###   Function to dynamically (re)-create it
            def create_subFrame_exeIntensity():
                subFrame_exeIntensity=ttk.Frame(cfgTab_exercise, style="Config.DK.TFrame")
                lFrame_exeIntensity=ttk.LabelFrame(subFrame_exeIntensity, style="Config.DK.TLabelframe", text='Intensity')
                add_exeIntensity_Button=ttk.Button(lFrame_exeIntensity, style="Ridge.Config.DK.TButton", width=2, text="+")
                GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance=[]
                GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance.append(subFrame_exeIntensity)
                GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance.append(lFrame_exeIntensity)
                GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance.append(add_exeIntensity_Button)
                #--------------------------------------------
                # Element Definition
                # - - - - - - - - - - - - - - - - - - - - - -
                nonlocal exeIntens_enumMap
                #We need multiple sub-lists to store: Line-Frame, Dropdown, Entry, Remove-Button
                #  (Less space in the variable-area required)
                GUIObj.variables.cfgTabExercise.Intensity_vars=[[],[]]
                GUIObj.widgets.cfgTabExercise.Intensity_wids=[[],[],[],[]]
                subListCBox=0
                subListEntry=1
                subListLF=2
                subListButton=3
                #
                def on_exeIntensMuscleSelect(event):
                    selectEqu=event.widget.get()
                    selectVal=exeIntens_enumMap[selectEqu]
                    _, exe=curr_selectedExe()
                    exe[SetupExeIdx.INTENSITY][event.widget.widget_idx][0]=selectVal
                #
                def on_exeIntensityChange(event):
                    try:
                        variable=event.widget.var
                        value=variable.get()
                        try:
                            if value.is_integer():
                                value=int(value)
                        except:
                            pass
                        _, exe=curr_selectedExe()
                        exe[SetupExeIdx.INTENSITY][event.widget.widget_idx][1]=value
                    except:
                        x=GUIObj.widgets.text_stdout.winfo_rootx()+GUIObj.widgets.text_stdout.winfo_width()//2
                        y=GUIObj.widgets.text_stdout.winfo_rooty()+GUIObj.widgets.text_stdout.winfo_height()//4
                        GUIObj.show_popup_simple('Not a valid number!',(x,y))
                #
                _, exe=curr_selectedExe()
                def _add_widget_and_var(i):
                    lineFrame=ttk.Frame(lFrame_exeIntensity, style="Config.DK.TFrame")
                    GUIObj.widgets.cfgTabExercise.Intensity_wids[subListLF].append(lineFrame)
                    intens=exe[SetupExeIdx.INTENSITY][i]
                    varCbox=tk.StringVar()
                    cbox=ttk.Combobox(lineFrame, style="Config.DK.TCombobox", height=25, width=15, textvariable=varCbox, state="readonly")
                    cbox.widget_idx=i
                    cbox.configure(values=list(exeIntens_enumMap.keys()))
                    for j, item in enumerate(cbox['values']):
                        if item==intens[0].value[1]:
                            cbox.current(j)
                            break
                    cbox.bind("<<ComboboxSelected>>", on_exeIntensMuscleSelect)
                    varEnt=tk.DoubleVar()
                    varEnt.set(intens[1])
                    entry=ttk.Entry(lineFrame, style="Config.DK.TEntry", textvariable=varEnt, width=5, state=tk.NORMAL)
                    entry.var=varEnt
                    entry.widget_idx=i
                    entry.bind("<KeyRelease>", on_exeIntensityChange)
                    entry.bind("<FocusOut>", on_exeIntensityChange)
                    entry.configure(
                        validate="key",
                        validatecommand=(GUIObj.cmds.validate_decimal_input,"%S","%P")
                    )
                    #
                    rem_exeIntensity_Button=ttk.Button(lineFrame, style="Groove.Config.DK.TButton", width=2, text="-")
                    rem_exeIntensity_Button.widget_idx=i
                    def on_rem_exeIntensity(event):
                        _, exe=curr_selectedExe()
                        exe[SetupExeIdx.INTENSITY].pop(event.widget.widget_idx)
                        GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance[2].pack_forget()
                        subFrame_exeIntensity_destroyWidgets_startingAt(event.widget.widget_idx)
                        _create_widgets_startingAt(event.widget.widget_idx)
                        GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance[2].pack_cmd()
                    rem_exeIntensity_Button.bind("<ButtonRelease-1>", on_rem_exeIntensity)
                    #
                    GUIObj.variables.cfgTabExercise.Intensity_vars[subListCBox].append(varCbox)
                    GUIObj.widgets.cfgTabExercise.Intensity_wids[subListCBox].append(cbox)
                    GUIObj.variables.cfgTabExercise.Intensity_vars[subListEntry].append(varEnt)
                    GUIObj.widgets.cfgTabExercise.Intensity_wids[subListEntry].append(entry)
                    GUIObj.widgets.cfgTabExercise.Intensity_wids[subListButton].append(rem_exeIntensity_Button)
                    #
                    cbox.grid(row=0,column=0,padx=(0,2),pady=(0,0),sticky=tk.E)
                    entry.grid(row=0,column=1,padx=(0,3),pady=0,sticky=tk.W)
                    rem_exeIntensity_Button.grid(row=0,column=2,padx=(0,0),pady=(0,0),sticky=tk.W)
                    lineFrame.pack(anchor=tk.N, side=tk.TOP, padx=(2,2), pady=(2,3))
                def _create_widgets_startingAt(index):
                    for i in range(index,len(exe[SetupExeIdx.INTENSITY])):
                        _add_widget_and_var(i)
                #
                _create_widgets_startingAt(0)
                #
                def on_add_exeIntensity(event):
                    _, exe=curr_selectedExe()
                    exe[SetupExeIdx.INTENSITY].append([muscleID.undef,0])
                    event.widget.pack_forget()
                    _add_widget_and_var(len(exe[SetupExeIdx.INTENSITY])-1)
                    event.widget.pack_cmd()
                #
                add_exeIntensity_Button.bind("<ButtonRelease-1>", on_add_exeIntensity)
                #
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                add_exeIntensity_Button.pack_cmd=lambda:add_exeIntensity_Button.pack(anchor=tk.N, side=tk.TOP, pady=(2,3))
                add_exeIntensity_Button.pack_cmd()
                #
                subFrame_exeIntensity.columnconfigure(0, weight=1)
                subFrame_exeIntensity.columnconfigure(1, weight=1)
                subFrame_exeIntensity.rowconfigure(0, weight=1)
                lFrame_exeIntensity.grid(row=0,column=0,rowspan=2,padx=(0,3),sticky=tk.NE)
                #
                return subFrame_exeIntensity
            def set_subFrame_exeIntensity():
                subFrame_exeIntensity=create_subFrame_exeIntensity()
                subFrame_exeIntensity.grid(row=GUIObj.variables.cfgTabExercise.Row_subFrame_exeIntensity, column=col, pady=(10,0), sticky=tk.NW+tk.E)
            def subFrame_exeIntensity_destroyWidgets_startingAt(index):
                for i, sublist in enumerate(GUIObj.widgets.cfgTabExercise.Intensity_wids):
                    for j in range(index,len(sublist)):
                        widget=sublist[j]
                        widget.destroy()
                    GUIObj.widgets.cfgTabExercise.Intensity_wids[i]=sublist[0:index]
                for i, sublist in enumerate(GUIObj.variables.cfgTabExercise.Intensity_vars):
                    for j in range(index,len(sublist)):
                        var=sublist[j]
                        del var
                    GUIObj.variables.cfgTabExercise.Intensity_vars[i]=sublist[0:index]
            def destroy_subFrame_exeIntensity():
                if hasattr(GUIObj.widgets.cfgTabExercise,'Intensity_wids_singleInstance'):
                    for widget in GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance:
                        widget.destroy()
                    subFrame_exeIntensity_destroyWidgets_startingAt(0)
                    del GUIObj.widgets.cfgTabExercise.Intensity_wids_singleInstance
                    del GUIObj.variables.cfgTabExercise.Intensity_vars
                    del GUIObj.widgets.cfgTabExercise.Intensity_wids
            #
            # - - - - - - - - - - - -
            nonlocal _create_subFrame_saveLoadReset
            subFrame_SaveLoad=_create_subFrame_saveLoadReset(cfgTab_exercise)
            # - - - - - - - - - - - -
            #
            #--------------------------------------------
            # Packing & Grid Config
            # - - - - - - - - - - - - - - - - - - - - - -
            cfgTab_exercise.columnconfigure(0, weight=1)
            row=0
            col=0
            subFrame_exeSelect.grid(row=row, column=col, sticky=tk.NW+tk.E)
            row+=1
            subFrame_exeVal.grid(row=row, column=col, sticky=tk.NW+tk.E)
            row+=1
            GUIObj.variables.cfgTabExercise.Row_subFrame_exeEquip=row
            row+=1
            GUIObj.variables.cfgTabExercise.Row_subFrame_exeIntensity=row
            row+=1
            saveSep=ttk.Separator(cfgTab_exercise, orient=tk.HORIZONTAL)
            saveSep.grid(row=row, column=col, pady=(15,10), sticky=tk.NW+tk.E)
            row+=1
            subFrame_SaveLoad.grid(row=row, column=col, sticky=tk.NW+tk.E)
            #
            set_exerciseValues()
            #
            return cfgTab_exercise
        cfgTab_exercise=create_cfgTab_exercise()
        # - - - - - -
        #
        # Tab: Dev Tools
        def create_cfgTab_DevTools():
            tab_devTools=ttk.Frame(cfgTabs, style="Config.DK.TFrame")
            #
            def create_subFrame_fileButtons():
                subFrame_fileButtons=ttk.Frame(tab_devTools, style="Config.DK.TFrame")
                def create_subFrame_clear():
                    subFrame_clear=ttk.LabelFrame(subFrame_fileButtons, style="Config.DK.TLabelframe", text='Clear')
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
                    button_pycache.pack(side=tk.TOP, padx=5, pady=(0,5))
                    return subFrame_clear
                subFrame_clear=create_subFrame_clear()
                def create_subFrame_makeExe():
                    subFrame_makeExe=ttk.LabelFrame(subFrame_fileButtons, style="Config.DK.TLabelframe", text='Produce Exe')
                    button_makeExe=ttk.Button(subFrame_makeExe, style="Config.DK.TButton", width=10, text="PyInstaller")
                    button_moveExe=ttk.Button(subFrame_makeExe, style="Config.DK.TButton", width=10, text="MoveExe")
                    #--------------------------------------------
                    # Element Configuration
                    # - - - - - - - - - - - - - - - - - - - - - -
                    button_makeExe.configure(
                        command=lambda:GUI_call_makeExe(GUIObj)
                    )
                    button_moveExe.configure(
                        command=lambda:GUI_call_moveExe(GUIObj)
                    )
                    #--------------------------------------------
                    # Packing & Grid Config
                    # - - - - - - - - - - - - - - - - - - - - - -
                    button_makeExe.pack(side=tk.TOP, padx=5, pady=(0,5))
                    button_moveExe.pack(side=tk.TOP, padx=5, pady=(0,5))
                    return subFrame_makeExe
                subFrame_makeExe=create_subFrame_makeExe()
                #
                subFrame_clear.grid(row=0,column=0,sticky=tk.NE)
                subFrame_makeExe.grid(row=1,column=0,sticky=tk.NE)
                #
                return subFrame_fileButtons
            subFrame_fileButtons=create_subFrame_fileButtons()
            #
            themeSelection=create_themeSelect_frame(GUIObj,tab_devTools)
            #--------------------------------------------
            # Packing & Grid Config (Tab Cfg-Basic)
            # - - - - - - - - - - - - - - - - - - - - - -
            tab_devTools.columnconfigure(0, weight=1)
            tab_devTools.columnconfigure(1, weight=1)
            row=0
            col=0
            themeSelection.grid(row=row, column=col, padx=(5,0), pady=(10,0))
            col+=1
            subFrame_fileButtons.grid(row=row, column=col, padx=(5,5), pady=(5,0), sticky=tk.NE)
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
        cfgTabs.add(cfgTab_muscle, text='Muscles')
        cfgTabs.add(cfgTab_exercise, text='Exercises')
        cfgTabs.add(cfgTab_DevTools, text='Dev')
        cfgTabs.select(0)
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













