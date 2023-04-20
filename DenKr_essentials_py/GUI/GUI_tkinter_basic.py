#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-14

@author: Dennis Krummacker
'''


import sys
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
# import tkinter.messagebox as tkmsgbox



##Global Variables & HCI-struct of Output-Handling
from settings import global_variables as globV

# try:
#     from ttkthemes import ThemedTk
# except ImportError:
#     globV.HCI.printErr("============================================")
#     globV.HCI.printErr("==  ERROR: Dependency missing: \"ttkthemes\".")
#     globV.HCI.printErr("============================================")
#     globV.HCI.printErr("--> This won't work without installing requirements...")

try:
    from PIL import Image, ImageTk, ImageDraw# Pillow (PIL fork)
except ImportError:
    globV.HCI.printErr("============================================")
    globV.HCI.printErr("==  ERROR: Dependency missing: \"Pillow\".")
    globV.HCI.printErr("============================================")
    globV.HCI.printErr("--> This won't work without installing requirements...")


##DenKr Packages
from auxiliary.filesystem import _assure_Dir_exists


class GUI_tkinter_Basic(object):
    """A child of this shall define \"create_gui(self)\" to build the GUI with its elements."""
    """A child of this may optionally define \"set_colorPalette(self)\" to overwrite the used Colors, which are set by default."""
    """Same for \"ttkStyle_setStyle()\"."""
    """A child may optionally define \"main_steps()\" to perform additional actions before GUI's mainloop is started."""
    def __init__(self,title):
        # Create tkinter window
        self.root=tk.Tk()
        #self.root=ThemedTk()
        self.root.title(title)
        # Init some more stuff
        #self._create_transparent_image()
        self.set_colorPalette_default()
        #if hasattr(self, "set_colorPalette") and callable(self.set_colorPalette):
        try:
            self.set_colorPalette()
        except AttributeError:
            pass
        # Set some values
        self._set_fonts()
        # ttk Style
        self.ttkStyle=ttk.Style()
        self._theme_set()
        # Some Settings
        self._set_window_PosAndSize()
        # Call function to create GUI widgets
        self.create_gui()
        try:
            self.root.after(0, self.main_steps())
        except AttributeError:
            pass
        #--------------------------
        # Run tkinter event loop
        self.root.mainloop()
    def _set_fonts(self):
        self.root.configure(background=self.color_bg)
        self.fontSystemsDefault=tkfont.nametofont("TkDefaultFont")# Get default font value into Font object
        # print(self.systemsDefaultFont)
        # print(self.systemsDefaultFont.actual())
        self.fontDefault=tkfont.nametofont("TkDefaultFont")# 'Helvetica', 'Courier', 'Segoe UI', 'Arial'
        self.fontHeading1='helvetica'
        self.fontHeading1_size=12
        self.fontHeading2='Courier'
        self.fontHeading2_size=10
    def _set_window_PosAndSize(self):
        self.screenX=self.root.winfo_screenwidth()
        self.screenY=self.root.winfo_screenheight()
        taskbarheight=75
        windowX=1700
        windowY=1020
        windowX=min(windowX,self.screenX)
        windowY=min(windowY,self.screenY-taskbarheight)
        windowPosX=self.screenX//2-windowX//2
        windowPosY=(self.screenY-taskbarheight)//2-windowY//2
        windowPosX=max(windowPosX,0)
        windowPosY=max(windowPosY,0)
        self.root.geometry(f"{windowX}x{windowY}+{windowPosX}+{windowPosY}")
    def _theme_set(self):
        self.theme_default=self.ttkStyle.theme_use()
        self.theme_selected=tk.StringVar()# This same Var is used by the created Theme-Select-Frame from the "GUI_tkinter_elements.py -> create_themeSelect_frame()"
        available_themes=self.ttkStyle.theme_names()
        for theme_name in available_themes:
            self.ttkStyle.theme_use(theme_name)
            self._ttkStyle_setStyle_Default()
            try:
                self.ttkStyle_setStyle()
            except AttributeError:
                pass
        if 'alt' in available_themes:
            self.theme_selected.set('alt')
        elif 'scidblue' in available_themes:
            self.theme_selected.set('scidblue')
        elif 'default' in available_themes:
            self.theme_selected.set('default')
        elif 'clam' in available_themes:
            self.theme_selected.set('clam')
        else:
            self.theme_selected.set(self.theme_default)
        self.ttkStyle.theme_use(self.theme_selected.get())
    def _ttkStyle_setStyle_Default(self):
        self.ttkStyle.configure("DK.TFrame", background=self.color_bg)
        self.ttkStyle.configure("DK.TLabelframe", background=self.color_bg)
        self.ttkStyle.configure("DK.TLabelframe.Label", background=self.color_bg)
        self.ttkStyle.configure("DK.TLabel", foreground='black', background=self.color_bg)
        self.ttkStyle.configure("DK.TButton", foreground='black', background=self.color_bg, width=0)#, relief='raised')
        self.ttkStyle.configure("DK.Vertical.TScrollbar", background='MediumPurple3', bordercolor="MediumPurple4", arrowcolor="blue")
        self.ttkStyle.map('DK.Vertical.TScrollbar',
            background=[('!active', 'MediumPurple3'), ('active', 'MediumPurple1')],
            bordercolor=[('!active', 'MediumPurple4'), ('active', 'MediumPurple2')],
        )
        self.ttkStyle.configure("DK.Horizontal.TScrollbar", background='MediumPurple3', bordercolor="MediumPurple4", arrowcolor="blue")
        self.ttkStyle.map('DK.Horizontal.TScrollbar',
            background=[('!active', 'MediumPurple3'), ('active', 'MediumPurple1')],
            bordercolor=[('!active', 'MediumPurple4'), ('active', 'MediumPurple2')],
        )
        self.ttkStyle.configure("DK.TCheckbutton", background=self.color_bg)#, foreground='red', indicatorbackground='green', indicatorcolor='yellow', indicatorrelief='blue')
        self.ttkStyle.configure("DK.TNotebook", background=self.color_bg)
        self.ttkStyle.configure("DK.TNotebook.Tabs", background=self.color_bg, bordercolor='yellow')
        self.ttkStyle.map('DK.TNotebook.Tab',
            background=[('selected', '!active', 'DarkOrchid4'), ('selected', 'active', 'DarkOrchid3'), ('!selected', '!active', 'dark slate blue'), ('!selected', 'active', 'slate blue')],
            foreground=[('selected', '!active', 'white'), ('selected', 'active', 'white'), ('!selected', '!active', 'white'), ('!selected', 'active', 'white')],
            focuscolor=[('disabled', 'black'), ('!disabled', 'black')],
        )
        self.ttkStyle.configure("DK.TEntry", background=self.color_bg)
        self.ttkStyle.configure("DK.TRadiobutton", background=self.color_bg)
        self.ttkStyle.configure("Top.DK.TFrame", background=self.color_heading_bg)
        self.ttkStyle.configure("Top.DK.TButton", foreground='white', background='royal blue')
        self.ttkStyle.map('Top.DK.TButton',
            background=[('!active', 'royal blue'), ('active', 'cornflower blue')],
            foreground=[('!active', 'white'), ('active', 'black')],
            focuscolor=[('disabled', 'black'), ('!disabled', 'black')],
            highlightcolor=[('focus', 'white'), ('!focus', 'white')],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')],
        )
        self.ttkStyle.configure("Border.Top.DK.TFrame", background='dark violet')
        self.ttkStyle.configure("BottomSep.Top.DK.TFrame", background='gold', borderwidth=4, relief=tk.FLAT)
        self.ttkStyle.configure("Config.DK.TFrame", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.configure("Config.DK.TLabelframe", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.configure("Config.DK.TLabelframe.Label", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.configure("Config.DK.TNotebook", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light, bordercolor='light gray')
        self.ttkStyle.configure("Config.DK.TNotebook.Tab", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.map('Config.DK.TNotebook.Tab',
            background=[('selected', '!active', self.color_cfg_bg), ('selected', 'active', self.color_cfg_light), ('!selected', '!active', 'LightSkyBlue4'), ('!selected', 'active', 'SkyBlue3')],
            foreground=[('!active', 'black'), ('active', 'black')],
            focuscolor=[('disabled', 'black'), ('!disabled', 'black')],
        )
        self.ttkStyle.configure("Config.DK.TCheckbutton", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.map('Config.DK.TCheckbutton',
            background=[('!active', self.color_cfg_bg), ('active', self.color_cfg_light)],
        )
        self.ttkStyle.configure("Config.DK.TLabel", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.configure("Config.DK.TEntry", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.configure("Config.DK.TButton", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.map('Config.DK.TButton',
            background=[('!active', self.color_cfg_light), ('active', 'LightSkyBlue1')],
            foreground=[('!active', 'black'), ('active', 'black')],
            focuscolor=[('disabled', 'black'), ('!disabled', 'black')],
            highlightcolor=[('focus', 'white'), ('!focus', 'white')],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')],
        )
        self.ttkStyle.configure("Config.DK.TRadiobutton", background=self.color_cfg_bg, foreground=self.color_cfg_foreground_light)
        self.ttkStyle.map('Config.DK.TRadiobutton',
            background=[('!active', self.color_cfg_bg), ('active', self.color_cfg_light)],
        )
        self.ttkStyle.configure("TextContainer.DK.TFrame", background=self.color_txtArea_bg)
        self.ttkStyle.configure("Heading1.DK.TLabel", background=self.color_heading_bg, foreground='white', font=(self.fontHeading1, self.fontHeading1_size))
        self.ttkStyle.configure("Heading2.DK.TLabel", font=(self.fontHeading2, self.fontHeading2_size))
    # - - - - - - - - - - - - - - - - - - - - - - -
    #TODO: Transparent Image stuff for use as background not finished
    # For use as transparent background, Render an Image as temporary file
    def _create_rectangle(self, trgtcanvas, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha=int(kwargs.pop('alpha') * 255)
            fill=kwargs.pop('fill')
            fill=self.root.winfo_rgb(fill) + (alpha,)
            image=Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            trgtcanvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        trgtcanvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    def _create_transparent_image(self):
        self._create_rectangle(80, 80, 150, 120, fill='#800000', alpha=.8)
    def _create_transparent_image_persistent(self):
        image_path=globV.progPath
        image_path=os.path.join(image_path,"tmp")
        image_file=os.path.join(image_path,"transparent.png")
        if not os.path.exists(image_file):
            _assure_Dir_exists(image_path)
            # Create an RGBA image with a transparent region
            width=200
            height=150
            image=Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw=ImageDraw.Draw(image)
            draw.rectangle((50, 50, 150, 100), fill=(255, 0, 0, 0))
            # Don't Save the image to a file if it shall be temporary
            image.save(image_file)
        # Create a PhotoImage object from the transparent image file
        self.transPhoto=tk.PhotoImage(file=image_file)
    def set_colorPalette_default(self):
        self.color_success='lime green'
        self.color_fail='OrangeRed2'
        self.color_bg='gray25'
        self.color_heading_bg='purple4'
        self.color_cfg_foreground_light='black'
        self.color_cfg_light='LightSkyBlue2'
        self.color_cfg_bg='LightSkyBlue3'
        self.color_txtArea_bg='black',
        self.color_txtArea_fg='white',
        self.color_txtArea_selectbg="lightblue",
        self.color_txtArea_selectfg="black",
    #--------------------------------------------------------------------------
    #System
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def reset_stdout(cls):
        sys.stdout=sys.__stdout__
    @classmethod
    def reset_stdin(cls):
        sys.stdin=sys.__stdin__
    @classmethod
    def redirect_stdout(cls,trgtwidget):
        class StdoutRedirector:
            def __init__(self, trgtwidget):
                self.trgtwidget=trgtwidget
            def write(self, message):
                self.trgtwidget.insert(tk.END, message)
                self.trgtwidget.see(tk.END)  # Scroll to the end of the text
            def flush(self):
                pass
        # Redirect stdout to the Text widget
        sys.stdout=StdoutRedirector(trgtwidget)
    @classmethod
    def redirect_stdin(cls,trgtwidget):
        class StdinRedirector:
            def __init__(self, trgtwidget):
                self.trgtwidget=trgtwidget
            def readline(self):
                line = self.trgtwidget.get('end-1c linestart', 'end')
                self.trgtwidget.delete('end-2l linestart', tk.END)
                return line
        # Redirect stdin to the Entry widget
        sys.stdin=StdinRedirector(trgtwidget)
    #--------------------------------------------------------------------------
    #Handling Text-Widgets
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Output: Text-Widget
    @classmethod
    def insert_to_text_widget(cls,trgtwidget,output):
        #curstate=trgtwidget['state']
        curstate=trgtwidget.cget('state')
        trgtwidget.configure(state=tk.NORMAL)
        # Append output to Text widget
        trgtwidget.insert(tk.END, output)# + "\n"
        trgtwidget.configure(state=curstate)
        # Scroll to the bottom of the Text widget
        trgtwidget.see(tk.END)
    @classmethod
    def clear_text_widget(cls,trgtwidget):
        curstate=trgtwidget.cget('state')
        trgtwidget.configure(state=tk.NORMAL)
        trgtwidget.delete("1.0", tk.END)
        trgtwidget.configure(state=curstate)
    ## Input: Text-Widget
    @classmethod
    def getInput_from_text_widget(cls,trgtwidget):
        user_input=trgtwidget.get('1.0', tk.END)
        #user_input=user_input.strip()
        return user_input
    ## Output: Label
    @classmethod
    def insert_to_label_widget(cls,trgtwidget,output):
        curtxt=trgtwidget.cget("text")
        trgtwidget.configure(text=curtxt+output)
    @classmethod
    def set_txt_label_widget(cls,trgtwidget,output):
        trgtwidget.configure(text=output)
    @classmethod
    def clear_label_widget(cls,trgtwidget):
        trgtwidget.configure(text="")
    #
    ## Function to copy text of widget to clipboard
    def copy_to_clipboard(self,trgtwidget):
        selected_text=trgtwidget.get('1.0', tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
        #tkmsgbox.showinfo('Clipboard', 'Schedule copied to clipboard!')
        self.root.update() # now it stays on the clipboard after the window is closed
        x=trgtwidget.winfo_rootx()+trgtwidget.winfo_width()//2
        y=trgtwidget.winfo_rooty()+trgtwidget.winfo_height()//4
        self.show_popup_simple('Text copied to clipboard!',(x,y))
    #--------------------------------------------------------------------------
    #Effects
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Function to show a custom popup window
    def show_popup_simple(self,displaytxt,geometryXY):
        popup=tk.Toplevel(self.root)
        popup.title('')
        label=tk.Label(popup, text=displaytxt, font=('Helvetica', 14, tkfont.ITALIC), bg='LightSteelBlue1', highlightthickness=0)
        popupwidth=label.winfo_reqwidth()+40
        popupheight=label.winfo_reqheight()+60
        #popup.geometry('200x100+{}+{}'.format(self.root.winfo_screenwidth() // 2 - 100, self.root.winfo_screenheight() // 2 - 50))
        popup.geometry('{}x{}+{}+{}'.format(popupwidth,popupheight,geometryXY[0]-popupwidth//2,geometryXY[1]-popupheight//2))
        popup.config(bg='LightSteelBlue1')
        popup.attributes('-alpha', 0.8)
        popup.overrideredirect(True)  # Remove title bar and window decorations
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)
        label.grid(row=0,column=0, padx=0, pady=0)
        # ok_button = tk.Button(popup, text='OK', command=popup.destroy)
        # ok_button.pack()
        popup.after(2000, popup.destroy)  # Automatically close popup after 2 seconds
    #Todo: Unfinished:
    # For Windows-only solution: https://stackoverflow.com/questions/70149724/tkinter-canvas-without-white-background-make-it-transparent
    def show_popup_fancy(self,displaytxt,geometryXY):
        def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, color):
            """Create a rounded rectangle on a canvas."""
            canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, outline=color, fill=color)
            canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, outline=color, fill=color)
            canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, outline=color, fill=color)
            canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, outline=color, fill=color)
            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, outline=color, fill=color)
            canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, outline=color, fill=color)

        popup=tk.Toplevel(self.root)
        popup.title('')
        label=tk.Label(popup, text=displaytxt, font=('Helvetica', 14, tkfont.ITALIC), bg='LightSteelBlue1', highlightthickness=0)
        popupwidth=label.winfo_reqwidth()
        popupheight=label.winfo_reqheight()
        canvaswidth=popupwidth+40
        canvasheight=popupheight+60
        canvas=tk.Canvas(popup, width=canvaswidth, height=canvasheight, bg="", highlightthickness=0)
        create_rounded_rectangle(canvas, 5, 5, canvaswidth-5, canvasheight-5, 15, color='red')
        #popup.geometry('200x100+{}+{}'.format(self.root.winfo_screenwidth() // 2 - 100, self.root.winfo_screenheight() // 2 - 50))
        popup.geometry('{}x{}+{}+{}'.format(canvaswidth,canvasheight,geometryXY[0]-canvaswidth//2,geometryXY[1]-canvasheight//2))
        popup.config(bg='LightSteelBlue1')
        popup.attributes('-alpha', 0.8)
        popup.overrideredirect(True)  # Remove title bar and window decorations
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)
        canvas.grid(row=0,column=0, padx=0, pady=0)
        # ok_button = tk.Button(popup, text='OK', command=popup.destroy)
        # ok_button.pack()
        popup.after(2000, popup.destroy)  # Automatically close popup after 2 seconds
    #--------------------------------------------------------------------------


class GUI_IOStream:
    def __new__(cls,widget):
        if isinstance(widget,tk.Text):
            return TextWidgetIOStream(widget)
            #return TextWidgetIOStream.__new__(TextWidgetIOStream,widget)
        elif isinstance(widget,ttk.Label):
            return LabelWidgetIOStream(widget)
            #return LabelWidgetIOStream.__new__(LabelWidgetIOStream,widget)
        else:
            return None


class TextWidgetIOStream:
    def __init__(self, text_widget):
        self.widget=text_widget
    def write(self, text):
        GUI_tkinter_Basic.insert_to_text_widget(self.widget, text)
    def writelines(self, text):
        if isinstance(text, str):
            GUI_tkinter_Basic.clear_text_widget(self.widget)
            GUI_tkinter_Basic.insert_to_text_widget(self.widget, text)
        elif isinstance(text, list) or isinstance(text, tuple):
            for line in text:
                GUI_tkinter_Basic.insert_to_text_widget(self.widget, line)
    def flush(self):
        pass# No-op, as flush is not required
    #Todo for both reads: Some kind of clearing the content of the widget.
    def read(self, size=None):
        user_input=self.widget.get('1.0', tk.END)
        return user_input
    def readline(self, size=None):
        #TODO. Some kind of buffering. If buffer empty: Read current content in. Then, split buffer by \n. Return first line, buffer rest. If buffer empty, del buffer-variable
        return self.widget.get('1.0', tk.END).split('\n', 1)[0]
    def clear(self):
        GUI_tkinter_Basic.clear_text_widget(self.widget)

class LabelWidgetIOStream:
    def __init__(self, label_widget):
        self.widget=label_widget
    def write(self, text):
        GUI_tkinter_Basic.insert_to_label_widget(self.widget, text)
    def writelines(self, text):
        if isinstance(text, str):
            GUI_tkinter_Basic.set_txt_label_widget(self.widget, text)
        elif isinstance(text, list) or isinstance(text, tuple):
            GUI_tkinter_Basic.clear_label_widget(self.widget)
            for line in text:
                GUI_tkinter_Basic.insert_to_label_widget(self.widget, line)
    def flush(self):
        pass# No-op, as flush is not required
    def read(self, size=None):
        raise (tk.TclError,"this stream can only be used for output")
    def readline(self, size=None):
        raise (tk.TclError,"this stream can only be used for output")
    def clear(self):
        GUI_tkinter_Basic.clear_label_widget(self.widget)





class GUI_state:
    def __init__(self,
        someStateVar=None
    ):
        self.someStateVar=someStateVar
class GUI_widgets:
    """Some widgets are to be kept, to reference to them on different positions."""
    """ Store them in some instance of this."""
    def __init__(self):
        pass
class GUI_variables:
    """Some Variables are used across several widgets/commands. So they need to be made accessable/visible (at least temporary in some local scope)."""
    """ Store them in some instance of this."""
    def __init__(self):
        pass