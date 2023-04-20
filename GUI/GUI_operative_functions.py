#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created: 2020-11-18
Last Update: 2023-04-16

@author: Dennis Krummacker
'''


import tkinter as tk



##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV




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





