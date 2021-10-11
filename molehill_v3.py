#Sean's Version
import os
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from tkinter import StringVar, filedialog
from typing import Text

#defines the window
win = tk.Tk()
win.title('Molehill V2')
win.geometry('500x500')

#defines the notebook widget
tabControl = ttk.Notebook(win)
tab = ttk.Frame(tabControl)

#start screen layout
def layout0():
    #destroy the start button
    btn0.destroy()

    #makes uploaded files a list
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

        #put scrolled text boxes onto the tab and center it
        content = st.ScrolledText(tab, wrap = tk.WORD, width = 50, height = 25)
        content.place(relx=0.5,rely=0.5,anchor='center')

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
content.place(relx=0.5,rely=0.5,anchor='center')

#initial start button
btn0 = tk.Button(text = 'Start', width = 10, command = layout0)
btn0.place(relx=0.5,rely=0.5,anchor='center')

#path = current directory
path = os.getcwd()
#new set for uploadedFiles
uploadedFiles = set()

#while True:
#iterate through the files in the current directory
for entry in os.scandir(path): 
    #if the file is a txt file and its not the uploadedFiles set
    if entry.path.lower().endswith('.txt') and entry not in uploadedFiles:
        #adds the file to the set
        print(entry)
        uploadedFiles.add(entry)
win.mainloop()