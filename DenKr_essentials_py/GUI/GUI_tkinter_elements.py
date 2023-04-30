#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-18

@author: Dennis Krummacker
'''

import tkinter as tk
from tkinter import ttk



class AutoHidingScrollbar(ttk.Scrollbar):
    # Defining set method with all its parameter
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            # Using grid_remove
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        ttk.Scrollbar.set(self, low, high)
    # Defining pack method
    def pack(self, **kw):
        # If pack is used it throws an error
        raise (tk.TclError,"pack cannot be used with this widget")
    # Defining place method
    def place(self, **kw):
        # If place is used it throws an error
        raise (tk.TclError, "place cannot be used  with this widget")


def create_text_container(GUIObj,parent,paddingContainer=((0,0),(0,0)),paddingText=((0,0),(0,0))):
    #--------------------------------------------
    # Element definition & Packing
    # - - - - - - - - - - - - - - - - - - - - - -
    text_container=ttk.Frame(parent, style="TextContainer.DK.TFrame",
        # relief=tk.FLAT,
        borderwidth=0
    )
    text_container.grid_rowconfigure(0, weight=1)
    text_container.grid_columnconfigure(0, weight=1)
    text=tk.Text(text_container, wrap=tk.NONE, width=50,height=10, borderwidth=0)
    text_container_textVsb=AutoHidingScrollbar(text_container, style="DK.Vertical.TScrollbar", orient=tk.VERTICAL, command=text.yview)
    text_container_textHsb=AutoHidingScrollbar(text_container, style="DK.Horizontal.TScrollbar", orient=tk.HORIZONTAL, command=text.xview)
    text.configure(yscrollcommand=text_container_textVsb.set, xscrollcommand=text_container_textHsb.set)
    text.grid(row=0, column=0, padx=paddingText[0], pady=paddingText[1], sticky=tk.NSEW)# Packed into Text-Container
    text_container_textVsb.grid(row=0, column=1, sticky=tk.NS)
    text_container_textHsb.grid(row=1, column=0, sticky=tk.EW)
    text_container.pack(fill=tk.BOTH, expand=tk.YES, padx=paddingContainer[0], pady=paddingContainer[1])# Packed into parent
    #--------------------------------------------
    # Element Configuration
    #   Maybe reconfigured after Function-Call
    # - - - - - - - - - - - - - - - - - - - - - -
    text.configure(
        font=(GUIObj.fontDefault, 9),
        background=GUIObj.color_txtArea_bg,
        foreground=GUIObj.color_txtArea_fg,
        selectbackground=GUIObj.color_txtArea_selectbg,
        selectforeground=GUIObj.color_txtArea_selectfg,
        state=tk.DISABLED
    )
    return text_container, text




class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.scrollWrapper=tk.Canvas(self)
        self.scrollWrapper.configure(borderwidth=0,relief=tk.FLAT,highlightthickness=0)
        vScrollbar=AutoHidingScrollbar(self, style="DK.Vertical.TScrollbar", orient=tk.VERTICAL, command=self.scrollWrapper.yview)
        self.scrollableFrame=ttk.Frame(self.scrollWrapper)
        self.scrollWrapper.create_window((0, 0), window=self.scrollableFrame, anchor=tk.NW, tags="resizeFrame")
        def on_resize(event):
            self.scrollWrapper.configure(
                scrollregion=self.scrollWrapper.bbox("all")
                ,width=event.width
            )
        def on_CanvasConfigure(event):
            self.scrollWrapper.itemconfig('resizeFrame', width=self.scrollWrapper.winfo_width())
        self.scrollableFrame.bind("<Configure>",on_resize)
        #self.scrollWrapper.bind("<Configure>",on_CanvasConfigure)
        self.scrollWrapper.configure(yscrollcommand=vScrollbar.set)
        self.scrollWrapper.grid(row=0,column=0,sticky=tk.NW+tk.SE)
        vScrollbar.grid(row=0,column=1,sticky=tk.NE+tk.S)

#Unfinished, doesn't work very well. Rather use the Class
def create_scrollable_frame(parent):
    scrollContainer=ttk.Frame(parent, style="Config.DK.TFrame")
    scrollContainer.columnconfigure(0, weight=1)
    scrollContainer.rowconfigure(0, weight=1)
    scrollWrapper=tk.Canvas(scrollContainer,width=1,height=100)
    scrollWrapper.grid(row=0,column=0,sticky=tk.NW+tk.SE)
    scrollableFrame=ttk.Frame(scrollWrapper, style="Config.DK.TFrame")
    scrollableFrame.bind("<Configure>", lambda e: scrollWrapper.configure(scrollregion=scrollWrapper.bbox("all")))
    vScrollbar=AutoHidingScrollbar(scrollContainer, style="DK.Vertical.TScrollbar", orient=tk.VERTICAL, command=scrollWrapper.yview)
    vScrollbar.grid(row=0,column=1,sticky=tk.NE+tk.S)
    scrollWrapper.configure(yscrollcommand=vScrollbar.set)
    # Pack the frame inside the canvas
    scrollWrapper.create_window((0, 0), window=scrollableFrame, anchor=tk.NW)
    return scrollContainer, scrollableFrame




def create_themeSelect_frame(GUIObj,parent):
    """This uses a tk.StringVar(). It is assumed that this is already instantiated as with the \"class GUI_tkinter_Basic()\" in \"GUI_tkinter_basic.py\""""
    def change_theme(*args):
        GUIObj.ttkStyle.theme_use(GUIObj.theme_selected.get())
    theme_frame=ttk.LabelFrame(parent, style="Config.DK.TLabelframe", text='Themes')
    for theme_name in GUIObj.ttkStyle.theme_names():
        rb=ttk.Radiobutton(
            theme_frame,
            text=theme_name,
            value=theme_name,
            variable=GUIObj.theme_selected,
            command=change_theme)
        rb.pack(expand=True, fill='both')
    #theme_frame.grid(padx=10, pady=10, ipadx=20, ipady=20, sticky='w')
    return theme_frame

    










