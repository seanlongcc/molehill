import os
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from tkinter import StringVar, filedialog
from typing import Text
import time

#defines the window
win = tk.Tk()
win.title('Molehill V2')
win.geometry('500x500')

#defines the notebook widget
tabControl = ttk.Notebook(win)
tab = ttk.Frame(tabControl)

#screen layout
def tabLayout():
    #destroy the start button
    btn0.destroy()
    
    #makes uploadedFiles a list
    orderedUploads = list(uploadedFiles)

    #extracts the name from elements in orderedUploads
    orderedUploads = [x.name for x in orderedUploads]
    #sort by alphabetical order
    orderedUploads.sort()
    #for each file in ordered uploads
    for name in orderedUploads:
        #create a new tab
        tab = ttk.Frame(tabControl)
        #give tab the current file name
        tabControl.add(tab, text = name)
        #organize the tabs
        tabControl.pack(expand = True, fill ="both")

        #put a scrolled text box onto the tab and center it
        content = st.ScrolledText(tab, wrap = tk.WORD, width = 100, height = 30)
        content.pack(expand = True, fill = "both")

        #open the file and read it
        with open(name, 'r') as f:
            #reads the data
            data = f.read()
            #inserts data into the content window
            content.insert(tk.END, data)

#lazy picture tab
#Defines the image
picture = tkinter.PhotoImage(file=r'constitution.png').subsample(5,5) 
tabControl.add(tab, text = 'Picture')
content = tkinter.Label(tab, image=picture, width=400, height=400)
content.pack(expand = True, fill = "both")

#initial start button
btn0 = tk.Button(text = 'Start', width = 10, command = tabLayout)
btn0.place(relx=0.5,rely=0.5,anchor='center')

#set path as current directory
path = os.getcwd()
#set for uploadedFiles
uploadedFiles = set()

#while True:
#iterate through the files in the current directory
for entry in os.scandir(path): 
    #if the file is a txt file and its not the uploadedFiles set
    if entry.path.lower().endswith('.txt') and entry not in uploadedFiles:
        #adds the file to the set
        uploadedFiles.add(entry)
        print(entry)
win.mainloop()