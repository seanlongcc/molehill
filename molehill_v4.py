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
root.title('Molehill V4')
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

                #text files
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
                    try:
                        filepath = db_to_csv(name)
                    except:
                        try:
                            filepath = db_to_csv2(name)
                        except:
                            try:
                                filepath = display_idName(name)
                            except:
                                print("database function does not exist")

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
def db_to_csv(name, tableName = "messages"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)
    con_wa = sqlite3.connect(os.path.join(BASE_DIR, "wa.db"))

    #read the database file
    df = pd.read_sql_query("SELECT _id, key_remote_jid, key_from_me, data, timestamp, media_url, media_mime_type, media_size, received_timestamp, receipt_server_timestamp FROM {}".format(tableName), con)

    #read database file of wa to get contacts
    df_wa = pd.read_sql_query("SELECT jid, number, display_name FROM wa_contacts", con_wa)

    wa_dict = {}
    #dictionary of contacts in wa, maps jid to display name
    for i in range(len(df_wa)):
       wa_dict[df_wa.iloc[i]["jid"]] = df_wa.iloc[i]["display_name"]

    match = []
    #corresponds mgstore and wa, maps phone number, and display name
    for i in range(1, len(df)):
        if df.iloc[i]["key_from_me"] == 0:
            match.append([wa_dict[df.iloc[i]["key_remote_jid"]], df.iloc[i]["data"]])
        else:
            match.append(["FROM ME", df.iloc[i]["data"]])
    print(match)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

def db_to_csv2(name, tableName = "wa_contacts"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT _id, jid, status, number, display_name, given_name, sort_name, nickname FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

def idName(name, tableName = "id_and_name"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)
    con_wa = sqlite3.connect(os.path.join(BASE_DIR, "wa.db"))
    conID = sqlite3.connect('id_and_name.db')

    #read the database file
    df = pd.read_sql_query("SELECT * FROM {}".format(tableName), con)

    #read database file of wa to get contacts
    df_wa = pd.read_sql_query("SELECT jid, display_name FROM wa_contacts", con_wa)

    #make cursors for each database
    cur = conID.cursor()
    curWA = con_wa.cursor()

    #get the data from wa_contacts and puts into rows
    curWA.execute("SELECT jid, display_name FROM wa_contacts")
    rows = curWA.fetchall()

    #put data from rows into id_and_name
    sql_statement = 'INSERT INTO id_and_name VALUES (?, ?)'
    cur.executemany(sql_statement, rows)
    
    #commit and close the db
    conID.commit()
    conID.close()

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

def display_idName(name, tableName = "id_and_name"):
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

#create new database for ID and Name
con = sqlite3.connect('id_and_name.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS id_and_name (ID, Name)''')
idName('id_and_name.db')
#cur.execute("INSERT INTO id_and_name VALUES (100,100)")
con.commit()
con.close()

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
            time.sleep(.01)
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