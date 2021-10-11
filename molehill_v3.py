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


#defines the window
root = tk.Tk()
root.title('Molehill V2')
root.geometry('500x500')

#defines the notebook widget
tabControl=ScrollableNotebook(root,wheelscroll=True,tabmenu=True)
tab = ttk.Frame(tabControl)

#screen layout
def tabLayout():
    #destroy the start button
    btn0.destroy()

    #makes uploadedFiles a list
    orderedUploads = list(uploadedFiles)
    #sort by alphabetical order
    orderedUploads.sort()

    #for each file in ordered uploads
    for name in orderedUploads:
        #SOME KINDA IF STATEMENT HERE TO CHECK IF THE TAB ALREADY EXISTS
        if name not in previousUploads:
            previousUploads.add(name)
            #create a new tab
            tab = ttk.Frame(tabControl)
            #give tab the current file name
            tabControl.add(tab, text = name)
            #organize the tabs
            tabControl.pack(expand = True, fill ="both")

            #put a scrolled text box onto the tab and center it
            content = st.ScrolledText(tab, wrap = tk.WORD)
            content.pack(expand = True, fill = "both")

            #open the file and read it
            with open(name, 'r') as f:
                #reads the data
                data = f.read()
                #inserts data into the content window
                content.insert(tk.END, data)

#refresh button
def refreshButton():
    btnRefresh = tk.Button(text = 'Refresh', command = lambda:[filescan(), tabLayout()])
    btnRefresh.pack()

#lazy picture tab
#Defines the image
picture = tkinter.PhotoImage(file=r'constitution.png').subsample(5,5) 
tabControl.add(tab, text = 'Picture')
content = tkinter.Label(tab, image=picture)
content.pack(expand = True, fill = "both")

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
        #if the file is a txt file and its not the uploadedFiles set
        if entry.path.lower().endswith('.txt') and entry not in uploadedFiles:
            #adds the file to the set
            uploadedFiles.add(entry.name)

#initial start button
btn0 = tk.Button(text = 'Start', width = 10, command = lambda:[filescan(), refreshButton(), tabLayout()])
btn0.place(relx=0.5,rely=0.5,anchor='center')

#spawns the window
root.mainloop()