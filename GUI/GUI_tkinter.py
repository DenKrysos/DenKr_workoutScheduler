#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-14

@author: Dennis Krummacker
'''

import os


##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV


import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

# from DenKr_essentials_py.struct_handling import dict_get_first_key

##DenKr Packages
from DenKr_essentials_py.GUI.GUI_tkinter_basic import GUI_tkinter_Basic, GUI_IOStream, GUI_state, GUI_widgets, GUI_variables
from DenKr_essentials_py.GUI.GUI_tkinter_elements import create_text_container
from commonFeatures.bits_and_pieces import print_introduction



##Other Files for Project
##Workout-Scheduler Packages
from workoutScheduler.workout import workout
#import settings.config_handler as cfghandle
from GUI.GUI_elements import create_cfg_area
from GUI.GUI_operative_functions import GUI_Operative_Functions as guif
from settings.path_and_file import ico_path, ico_fName



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# REFERENCES for TK/TCL/TKinter
#
# https://www.tcl.tk/man/tcl/TkCmd/ttk_button.html
# Colors:
#    http://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO
#
# - In the Tab for "Dev-Tools"
#    - "Temporary Switch to Terminal". Restarts App in Terminal-Mode
#- Exercise Tutorial: Button that pops up a window in which Explanations for the Exercises are displayed about how they are performed. I.e. "What means this Exercise Name?"
#- Have multiple "Muscle-Profiles". Like one for "Default", "appropriate volume", "slightly-reduced volume".
#    This can serve to display different configuration to the customer, show that the shipped profile is a little too low in volume and what the optimum would be.
#    Then one profile can be marked as "active". The pre-shipped can't be changed in value via GUI, but the "custom" one can for sure.
#



class DKWoSched_GUI(GUI_tkinter_Basic):
    #--------------------------------------------------------------------------
    class GUI_state(GUI_state):
        def __init__(self,
            stdOut_wordWrap=tk.NONE#WORD
        ):
            super().__init__()
            self.stdOut_wordWrap=stdOut_wordWrap
    def __init__(self):
        super().__init__("DenKr-Workout-Scheduler")
    #--------------------------------------------------------------------------
    def ttkStyle_setStyle(self):
        self.ttkStyle.configure("UserQuery.DK.TFrame", background=self.color_userQuerry_bg)
        self.ttkStyle.configure("UserQuery.DK.TLabel", background=self.color_userQuerry_bg, foreground=self.color_userQuerry_fg, font=(self.fontDefault, 12, tkfont.BOLD), justify=tk.CENTER)
        self.ttkStyle.configure("BG.UserQuery.DK.TFrame", background=self.color_userQuerry_bg)
    def set_colorPalette(self):
        self.color_userQuerry_bg='LightGoldenrod1'
        self.color_userQuerry_fg='black'
    #--------------------------------------------------------------------------
    def main_steps(self):
        globV.HCI.set_out(self.IOstream_std)
        globV.HCI.set_err(self.IOstream_err)
        print_introduction()
        self.startup()
    def startup(self):
        self.new_computation()
    def gui_settings(self):
        self.root.iconbitmap(os.path.join(globV.inherentDataFilePath,ico_path,ico_fName))
    #--------------------------------------------------------------------------
    def new_computation(self):
        self.workout=workout()
        self.workout.set()
        self.workout.history_read()
        err=self.workout.compute_workoutSchedule()
        if 0==err:
            self.IOstream_past.clear()
            guif.print_previous_schedule(self)
            guif.rewrite_computed_schedule(self)
            guif.history_write_userPrompt(self)
            return 0
        else:
            return 1
    #--------------------------------------------------------------------------
    def set_outStream_result(self,trgtwidget):
        self.IOstream_result=GUI_IOStream(self,trgtwidget)
    def set_outStream_past(self,trgtwidget):
        self.IOstream_past=GUI_IOStream(self,trgtwidget)
    def set_outStream_std(self,trgtwidget):
        self.IOstream_std=GUI_IOStream(self,trgtwidget)
    def set_outStream_err(self,trgtwidget):
        self.IOstream_err=GUI_IOStream(self,trgtwidget,StreamType='err')
    def set_outStream_query(self,trgtwidget):
        self.IOstream_query=GUI_IOStream(self,trgtwidget)
    def create_gui(self):
        #==========================================================================
        #--------------------------------------------------------------------------
        # Basic Set-Up
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # GUI-State-Variables
        self.state=self.GUI_state()
        self.widgets=GUI_widgets()
        self.variables=GUI_variables()
        #
        guif.set_exercise_names(self)
        #
        # Some Values to have common across multiple widgets
        textArea_padx=(5,0)
        textArea_pady=(5,0)
        textContainer_pad=0  #aka Width of Fancy-Canvas-Frame
        
        #==========================================================================
        #--------------------------------------------------------------------------
        # Configuration Area
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        frame_config=create_cfg_area(self)

        #--------------------------------------------
        # Operation
        # - - - - - - - - - - - - - - - - - - - - - -


        
        # Call the Combobox-Trigger function with the initial value
        #on_entry_select(None)




        #==========================================================================
        #--------------------------------------------------------------------------
        # Text-Areas Common Stuff
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def draw_Frame_generic(trgtcanvas):
            # Clear the canvas
            trgtcanvas.delete("all")
            # Get the canvas dimensions
            canvas_width=trgtcanvas.winfo_width()
            canvas_height=trgtcanvas.winfo_height()
            # Calculate the coordinates for the trapezium
            x1 = 0
            y1 = 0
            x2 = canvas_width
            y2 = 0
            x3 = 3*canvas_width // 4
            y3 = canvas_height // 4
            x4 = canvas_width // 4
            y4 = canvas_height // 4
            # Draw the trapezium on the canvas
            trgtcanvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill="gray", outline="black", width=2)
        #==========================================================================
        #--------------------------------------------------------------------------
        # Output-Text-Area (Middle - Tabs: stdout, Past Schedule)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def create_stdout_area():
            #--------------------------------------------
            # Element definition
            # - - - - - - - - - - - - - - - - - - - - - -
            frame_stdout=ttk.Frame(self.root, style="DK.TFrame")
            # Top-Row: Label and Copy-Button into frame
            def create_topFrame_middleArea():
                TopFrameBottomSep=ttk.Frame(frame_stdout, style="BottomSep.Top.DK.TFrame")
                TopFrameBorder=ttk.Frame(TopFrameBottomSep, style="Border.Top.DK.TFrame")
                TopFrameBorder.pack(fill=tk.BOTH,expand=tk.YES,padx=0,pady=(0,3))
                TopFrame=ttk.Frame(TopFrameBorder, style="Top.DK.TFrame")
                TopFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=(0,5), pady=0)
                toplabel=ttk.Label(
                    TopFrame,
                    style="Heading1.DK.TLabel",
                    text="Std-Out & Past Schedule"
                )
                ### Sub-Frame Packing
                TopFrame.columnconfigure(0, weight=1)
                toplabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NW)
                return TopFrameBottomSep
            topFrame_stdout=create_topFrame_middleArea()
            # - - - - - - - - - - - -
            #
            # Notebook to have two Text-Areas in Tabs
            def create_outTabs():
                outTabs=ttk.Notebook(frame_stdout, style='DK.TNotebook')
                # - - - - - - - - - - - -
                ## Text Area 1
                def create_TextArea1():
                    # Create a canvas to display text on-top
                    canvas_stdout=tk.Canvas(outTabs,borderwidth=2,relief=tk.FLAT)
                    canvas_stdout.pack(fill=tk.BOTH, expand=tk.YES)
                    ## Inside Canvas: Create Text Area with Scrollbars
                    _, self.widgets.text_stdout=create_text_container(self,canvas_stdout,
                        (textContainer_pad,textContainer_pad),
                        (textArea_padx,textArea_pady)
                    )
                    self.widgets.text_stdout.configure(wrap=self.state.stdOut_wordWrap)
                    #--------------------------------------------
                    # Element Configuration
                    # - - - - - - - - - - - - - - - - - - - - - -
                    canvas_stdout.configure(background="purple4")
                    self.widgets.text_stdout.configure(
                        font=(self.fontDefault, 10)
                    )
                    return canvas_stdout
                textArea_stdout=create_TextArea1()
                # - - - - - - - - - - - -
                ## Text Area 2
                def create_TextArea2():
                    # Canvas
                    canvas_out2=tk.Canvas(outTabs,borderwidth=2,relief=tk.SUNKEN)
                    canvas_out2.pack(fill=tk.BOTH, expand=tk.YES)
                    ## Text Area
                    _, self.widgets.text_out2=create_text_container(self,canvas_out2,
                        (textContainer_pad,textContainer_pad),
                        (textArea_padx,textArea_pady)
                    )
                    return canvas_out2
                textArea_previous=create_TextArea2()
                # - - - - - - - - - - - - - - - - - - - - - -
                # Add Tabs to the Notebook
                outTabs.add(textArea_stdout, text='StdOut')
                outTabs.add(textArea_previous, text='PreviousWorkouts')
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                def scrollDown_stdout(*args):
                    try:
                        if True==self.state.scrollStdout:
                            self.widgets.text_stdout.yview_moveto(1.0)
                        del self.state.scrollStdout
                    except:
                        pass
                self.widgets.text_stdout.bind("<Configure>", scrollDown_stdout)
                #
                outTabsStickyness=tk.NW+tk.SE
                def regrid_outTabs():
                    selectedTab=outTabs.index(outTabs.select())
                    activeText=self.widgets.text_stdout
                    if 1==selectedTab:
                        activeText=self.widgets.text_out2
                    # Check if the text widget is scrollable
                    visibleFraction=activeText.yview()
                    # Re-grid the text widget with or without padding depending on whether it is scrollable
                    if 0.0==visibleFraction[0] and 1.0==visibleFraction[1]:
                        outTabs.grid(row=1, column=0, padx=(0,3), pady=0, sticky=outTabsStickyness)
                    else:
                        outTabs.grid(row=1, column=0, padx=0, pady=0, sticky=outTabsStickyness)
                # Bind the <Configure> event of the window to the regrid_text function
                self.root.bind('<Configure>', lambda e: regrid_outTabs())
                return outTabs
            self.widgets.outTabs=create_outTabs()
            # - - - - - - - - - - - -
            #
            # Dynamic Area for User-Query/Input
            def create_userQuery_area():
                userQueryBorder=ttk.Frame(frame_stdout, style="DK.TFrame")
                userQuery_area=ttk.Frame(userQueryBorder, style="UserQuery.DK.TFrame", borderwidth=3, relief=tk.RIDGE)# RAISED, RIDGE, GROOVE, SUNKEN, FLAT
                textBG=ttk.Frame(userQuery_area, style="BG.UserQuery.DK.TFrame", width=30,height=5, borderwidth=0)
                textLabel=ttk.Label(textBG, style="UserQuery.DK.TLabel")
                button_yes=ttk.Button(userQuery_area, style="Config.DK.TButton", width=7, text="Yes")
                # button_yes.configure(command=reset_config)
                button_no=ttk.Button(userQuery_area, style="Config.DK.TButton", width=7, text="No")
                # button_no.configure(command=save_config_persistent)
                #--------------------------------------------
                # Element Configuration
                #   Maybe reconfigured after Function-Call
                # - - - - - - - - - - - - - - - - - - - - - -
                # textLabel.configure(
                #     state=tk.DISABLED
                # )
                def userQuery_yes():
                    self.widgets.userQuery_area.grid_forget()
                    self.workout.push_schedule_toHistory()
                    self.workout.history_write()
                button_yes.configure(command=userQuery_yes)
                def userQuery_no():
                    self.widgets.userQuery_area.grid_forget()
                button_no.configure(command=userQuery_no)
                #--------------------------------------------
                # Packing & Grid Config
                # - - - - - - - - - - - - - - - - - - - - - -
                textLabel.place(anchor=tk.CENTER, relx=0.5, rely=0.5)
                #
                userQuery_area.rowconfigure(0, weight=1)
                userQuery_area.rowconfigure(1, weight=1)
                userQuery_area.columnconfigure(0, weight=1)
                userQuery_area.columnconfigure(1, weight=0)
                textBG.grid(row=0, column=0, rowspan=2, padx=0, pady=0, sticky=tk.NW+tk.SE)
                button_yes.grid(row=0, column=1, padx=0, pady=0, sticky=tk.E)
                button_no.grid(row=1, column=1, padx=0, pady=0, sticky=tk.E)
                #
                userQuery_area.pack(fill=tk.BOTH, expand=tk.YES, padx=(0,0), pady=(0,0))
                #--------------------------------------------
                # Operation
                # - - - - - - - - - - - - - - - - - - - - - -
                self.set_outStream_query(textLabel)
                return userQueryBorder
            self.widgets.userQuery_area=create_userQuery_area()
            #--------------------------------------------
            # Packing & Grid Config
            # - - - - - - - - - - - - - - - - - - - - - -
            # Main-Frame
            row=0
            col=0
            frame_stdout.columnconfigure(col, weight=1)
            topFrame_stdout.grid(row=row, column=col, padx=0, pady=0, sticky=tk.NW+tk.NE)
            frame_stdout.rowconfigure(row, weight=0)
            row=1
            col=0
            #self.widgets.outTabs.grid(row=row, column=col, padx=(0,3), pady=0, sticky=outTabsStickyness)
            frame_stdout.rowconfigure(row, weight=1)
            row+=1
            self.widgets.userQuery_area_pack=lambda:self.widgets.userQuery_area.grid(row=row, column=col, padx=0, pady=0, sticky=tk.NW+tk.NE)# Not packed-from-the-outset. Dynamically packed/unpacked by trigger
            frame_stdout.rowconfigure(row, weight=0)
            row+=1
            #--------------------------------------------
            # Operation
            # - - - - - - - - - - - - - - - - - - - - - -
            self.set_outStream_std(self.widgets.text_stdout)
            self.set_outStream_err(self.widgets.text_stdout)
            self.set_outStream_past(self.widgets.text_out2)
            #
            return frame_stdout
        frame_stdout=create_stdout_area()


        #==========================================================================
        #--------------------------------------------------------------------------
        # Output-Text-Area (Right - Computed upcoming Schedule)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def create_result_area():
            #--------------------------------------------
            # Element definition
            # - - - - - - - - - - - - - - - - - - - - - -
            frame_wo_upcoming=ttk.Frame(self.root, style="DK.TFrame")
            # Top-Row: Label and Copy-Button into frame
            def create_textArea_result():
                # Create a canvas to display text on-top
                canvas_wo_upcoming=tk.Canvas(frame_wo_upcoming,
                    #width=500, height=150,
                    borderwidth=2,
                    relief=tk.RAISED
                )
                ## Inside Canvas: Create Text Area with Scrollbars
                _, self.widgets.text_wo_upcoming=create_text_container(self,canvas_wo_upcoming,
                    (textContainer_pad,textContainer_pad),
                    (textArea_padx,textArea_pady)
                )
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                canvas_wo_upcoming.configure(background="purple4")
                # Draw fancy frame in canvas
                # TODO
                # For resizing also interessting: https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
                # def on_canvas_resize(event):
                #     draw_Frame_generic(canvas_wo_upcoming)
                # canvas_wo_upcoming.bind("<Configure>", on_canvas_resize)
                return canvas_wo_upcoming
            textArea_result=create_textArea_result()
            # - - - - - - - - - - - -
            def create_topFrame_rightArea():
                TopFrameBottomSep=ttk.Frame(frame_wo_upcoming, style="BottomSep.Top.DK.TFrame")
                topFrame=ttk.Frame(TopFrameBottomSep, style="Top.DK.TFrame")
                topFrame.pack(fill=tk.BOTH,expand=tk.YES,padx=0,pady=(0,3))
                label_frame_wo_upcoming=ttk.Label(
                    topFrame,
                    style="Heading1.DK.TLabel",
                    text="Computed Schedule"
                )
                ## Create the button to copy text to clipboard
                clipboardButton_wo_upcoming=ttk.Button(topFrame, style="Top.DK.TButton", text='Copy to Clipboard')
                #--------------------------------------------
                # Element Configuration
                # - - - - - - - - - - - - - - - - - - - - - -
                clipboardButton_wo_upcoming.configure(command=lambda trgtwidget=self.widgets.text_wo_upcoming:self.copy_to_clipboard(trgtwidget))
                ### Sub-Frame Packing
                topFrame.columnconfigure(0, weight=1)
                topFrame.columnconfigure(1, weight=1)
                label_frame_wo_upcoming.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NW)
                clipboardButton_wo_upcoming.grid(row=0,column=1,pady=0,sticky=tk.SE)
                return TopFrameBottomSep
            topFrame_wo_upcoming=create_topFrame_rightArea()
            #--------------------------------------------
            # Packing & Grid Config
            # - - - - - - - - - - - - - - - - - - - - - -
            row=0
            col=0
            frame_wo_upcoming.columnconfigure(col, weight=1)
            topFrame_wo_upcoming.grid(row=row, column=col, padx=0, pady=0, sticky=tk.NW+tk.NE)
            frame_wo_upcoming.rowconfigure(row, weight=0)
            row+=1
            textArea_result.grid(row=row, column=col, padx=0, pady=0, sticky=tk.NW+tk.SE)
            frame_wo_upcoming.rowconfigure(row, weight=1)
            row+=1
            frame_wo_upcoming.rowconfigure(row, weight=0)
            #--------------------------------------------
            # Operation
            # - - - - - - - - - - - - - - - - - - - - - -
            # Bind focus in and focus out events to select and deselect entire text, respectively
            # Function to add text selection on focus in event
            # def on_focus_in(event):
            #     text.tag_add(tk.SEL, "1.0", tk.END)
            # # Function to remove text selection on focus out event
            # def on_focus_out(event):
            #     text.tag_remove(tk.SEL, "1.0", tk.END)
            # text.bind("<FocusIn>", on_focus_in)
            # text.bind("<FocusOut>", on_focus_out)
            self.set_outStream_result(self.widgets.text_wo_upcoming)
            #insertTxt="Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum \nLorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum "
            #text_wo_upcoming.insert(tk.END,insertTxt)
            #self.insert_to_text_widget(text_wo_upcoming, insertTxt)
            #globV.HCI.printStd(insertTxt)
            #globV.HCI.printStd("test")
            #
            return frame_wo_upcoming
        frame_wo_upcoming=create_result_area()


        #==========================================================================
        #--------------------------------------------------------------------------
        # Level-1 Packing
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # & Configure the grid rows and columns to resize with the window
        row=0
        self.root.rowconfigure(row, weight=1)
        col=0
        frame_config.grid(row=row,column=col,sticky=tk.NW+tk.SE)
        self.root.columnconfigure(col, weight=0)
        col+=1
        frame_stdout.grid(row=row,column=col,sticky=tk.NW+tk.SE)
        self.root.columnconfigure(col, weight=6)
        col+=1
        frame_wo_upcoming.grid(row=row,column=col,sticky=tk.NW+tk.SE)
        self.root.columnconfigure(col, weight=4)
        col+=1










# Define your main function
def main():
    # Create and run the app
    app = DKWoSched_GUI()

# To test the GUI isolated
if __name__ == "__main__":
    main()