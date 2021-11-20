import os
import os.path
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
from PIL import Image, ImageTk
from pandastable import Table, TableModel
import sqlite3
import pandas as pd

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

    '''for future if we want to delete tabs, works if no previousUploads() set.
    for tab in tabControl.notebookTab.tabs():
       tabControl.forget(tab)
    '''
    #for each file in ordered uploads
    for name in orderedUploads:
        #if txt file
        if name.lower().endswith(('.txt', '.png', '.jpg', 'jpeg', '.db')):
            if name not in previousUploads:
                #add name to used list
                previousUploads.add(name)
                tab = ttk.Frame(tabControl)
                #give tab the current file name
                tabControl.add(tab, text = name)
                #organize the tabs
                tabControl.pack(expand = True, fill ="both")

                #txt
                if name.lower().endswith('.txt'):
                    #put a scrolled text box onto the tab and have it fill the area
                    content = st.ScrolledText(tab, wrap = tk.WORD)
                    content.pack(expand = True, fill = "both")
                    #open the file and read it
                    with open(name, 'r') as f:
                        #reads the data
                        data = f.read()
                        #inserts data into the content window
                        content.insert(tk.END, data)

                #databases
                elif name.lower().endswith('.db'):
                    #convert db to csv
                    filepath = db_to_csv(name)

                    #display the csv
                    csvDisplay(filepath, tab)

                #image
                else: 
                    #open the picture to resize
                    img = Image.open(name)
                    #resize the image
                    imgrs = img.resize((img.width // 3, img.height // 3),Image.ANTIALIAS)
                    #set the picture
                    pic = ImageTk.PhotoImage(imgrs)
                    #set the label to display the picture
                    content = tkinter.Label(tab, image=pic)
                    #keep a reference to the tkinter object so that the picture shows: "Why do my Tkinter images not appear?"
                    content.image = pic
                    #place the image
                    content.pack(expand = True, fill = "both")

#convert db to csv, tableName needs to be hardcoded
def db_to_csv(name, tableName = "notes"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT * FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#display the csv
def csvDisplay(filepath, tab):
    #sets the table
    table = Table(tab, showstatusbar=True, showtoolbar=True)

    #open the csv file
    table.importCSV(filepath)

    #show the csv file on the table
    table.show()

#set for uploadedFiles
uploadedFiles = set()
#set for previous uploads to compare to
previousUploads = set()

#scans the current directory for 
def fileUpdate():
    #set path as current directory
    path = os.getcwd()

    #iterate through each file in the directory
    for entry in os.scandir(path): 
        #if the file is a .txt or .png, dont need to check for repeats since its a set
        if entry.path.lower().endswith(('.txt', '.png', '.jpg', 'jpeg', '.db')):
            #sleep timer for databases to load and convert
            time.sleep(.001)
            #adds the file to the set
            uploadedFiles.add(entry.name)

#what fileWatch calls to update the tabs
class Event(LoggingEventHandler):
    def dispatch(self, event):
        fileUpdate()
        tabLayout()

#automatically update the tabs
def fileWatch():
    #set the format for logging info
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    #set format for displaying path
    path = os.getcwd()

    #initialize logging event 
    event_handler = Event()
    #initialize logging even handler to print actions
    event_log = LoggingEventHandler()
  
    #initialize Observer
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.schedule(event_log, path, recursive=True)

    #start the observer
    observer.start()
    try:
        while True:
            #set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#initial start button
btn0 = tk.Button(text = 'Start', width = 10, command = lambda:[fileUpdate(), tabLayout()])
btn0.place(relx=0.5,rely=0.5,anchor='center')

#start another thread for fileWatch, set to daemon so that it stops when the window closes
fileWatchThread = threading.Thread(target = fileWatch, daemon = True)
fileWatchThread.start()

#spawns the window
root.mainloop()