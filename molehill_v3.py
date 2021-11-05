import os
import time
import sys
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from tkinter import StringVar, filedialog
from typing import Text
from ScrollableNotebook import *
import threading
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

#defines the window
root = tk.Tk()
root.title('Molehill V3')
root.geometry('1280x720')

#defines the notebook widget
tabControl=ScrollableNotebook(root, wheelscroll=True, tabmenu=True)

#screen layout
def tabLayout():
    #destroy the start button
    btn0.destroy()
    #makes uploadedFiles a list
    orderedUploads = list(uploadedFiles)
    #sort by alphabetical order
    orderedUploads.sort(key = lambda x: x.lower())

    #for each file in ordered uploads
    for name in orderedUploads:
        #if text file
        if name.lower().endswith('.txt'):
            #if tab doesnt exist, compares with previousUploads
            if name not in previousUploads:
                #add name to used list
                previousUploads.add(name)
                #create a new tab
                tab = ttk.Frame(tabControl)
                #give tab the current file name
                tabControl.add(tab, text = name)
                #organize the tabs
                tabControl.pack(expand = True, fill ="both")

                #put a scrolled text box onto the tab and have it fill the area
                content = st.ScrolledText(tab, wrap = tk.WORD)
                content.pack(expand = True, fill = "both")

                #open the file and read it
                with open(name, 'r') as f:
                    #reads the data
                    data = f.read()
                    #inserts data into the content window
                    content.insert(tk.END, data)

        #if picture
        elif name.lower().endswith(('.png')):
            #if tab doesnt exist, compares with previousUploads
            if name not in previousUploads:
                #add name to used list
                previousUploads.add(name)
                #create a new tab
                tab = ttk.Frame(tabControl)
                #give tab current file name
                tabControl.add(tab, text = name)
                #organize the tabs
                tabControl.pack(expand = True, fill ="both")
                
                #set the picture
                pic = tkinter.PhotoImage(file=name).subsample(3,3)
                #set the label to display the picture
                content = tkinter.Label(tab, image=pic)
                #keep a reference to the tkinter object so that the picture shows: "Why do my Tkinter images not appear?"
                content.image = pic
                #place the image
                content.pack(expand = True, fill = "both")                

#refresh button
def refreshButton():
    btnRefresh = tk.Button(text = 'Refresh', command = lambda:[filescan(), tabLayout()])
    btnRefresh.pack()

#set for uploadedFiles
uploadedFiles = set()
#set for previous uploads to compare to
previousUploads = set()

#scans the current directory
def filescan():
    #set path as current directory
    path = os.getcwd()
    #iterate through each file in the directory
    for entry in os.scandir(path): 
        #if the file is a .txt or .png
        if entry.path.lower().endswith(('.txt', '.png')):
            #adds the file to the set
            uploadedFiles.add(entry.name)

#initial start button
btn0 = tk.Button(text = 'Start', width = 10, command = lambda:[filescan(), refreshButton(), tabLayout()])
btn0.place(relx=0.5,rely=0.5,anchor='center')

#spawns the window
root.mainloop()