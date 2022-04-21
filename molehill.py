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
tabControl = ScrollableNotebook(root, wheelscroll=True, tabmenu=True)

#hardcoded list of databases with no extensions
noExtension = ('viber_data', 'viber_messages', 'search_cache_db', 'threads_db2', 'database.sqlite')
excluded = ('requirements.txt')

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
        if (name not in excluded) and (name.lower().endswith(('.txt', '.png', '.jpg', 'jpeg', '.db')) or name in noExtension):
            if name not in previousUploads:
                #add name to used list
                previousUploads.add(name)
                tab = ttk.Frame(tabControl)

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
                    tab_name = name

                #databases. each database file is tried until a match is found.
                elif name.lower().endswith('.db') or name in noExtension:
                    #convert db to csv
                    try: #whatsapp
                        filepath = db_to_csv_MSG(name)
                        tab_name = "WhatsApp Messages"
                    except:
                        try:
                            filepath = db_to_csv_WA(name)
                            tab_name = "WhatsApp Contacts"
                        except:
                            try: #contacts
                                filepath = db_to_csv_CON(name)
                                tab_name = "Phone Contacts"
                            except:
                                try: #fb messenger
                                    filepath = db_to_csv_FBS(name)
                                    tab_name = "Messenger Contacts"
                                except:
                                    try:
                                        filepath = db_to_csv_FBT(name)
                                        tab_name = "Messenger Messages"
                                    except:
                                        try: #viber
                                            filepath = db_to_csv_VD(name)
                                            tab_name = "Viber Contacts"
                                        except:
                                            try:
                                                filepath = db_to_csv_VM(name)
                                                tab_name = "Viber Messages"
                                            except:
                                                try: #telegram
                                                    filepath = db_to_csv_TEL(name)
                                                    tab_name = "Telegram"
                                                except:
                                                    try: # signal
                                                        time.sleep(3) #extra sleep timer for the signal database to load
                                                        filepath = db_to_csv_SIG(name)
                                                        tab_name = "Signal"
                                                    except:
                                                        print("database function does not exist")
                    #display the csv
                    csvDisplay(filepath, tab)

                #image
                else: 
                    #open the picture to resize
                    img = Image.open(name)
                    #resize the image
                    imgrs = img.resize((img.width, img.height),Image.ANTIALIAS)
                    #set the picture
                    pic = ImageTk.PhotoImage(imgrs) 
                    #set the label to display the picture
                    content = tkinter.Label(tab, image=pic)
                    #keep a reference to the tkinter object so that the picture shows: "Why do my Tkinter images not appear?"
                    content.image = pic
                    #place the image
                    content.pack(expand = True, fill = "both")
                    tab_name = name
                    
                #give tab the current file name
                tabControl.add(tab, text = tab_name)
                #organize the tabs
                tabControl.pack(expand = True, fill ="both")

#convert db to csv, tableName needs to be hardcoded
#whatsapp
def db_to_csv_MSG(name, tableName = "messages"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT _id, key_remote_jid, key_from_me, data, timestamp, media_url, media_mime_type, media_size, received_timestamp, receipt_server_timestamp FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#whatsapp
def db_to_csv_WA(name, tableName = "wa_contacts"):
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

#contacts
def db_to_csv_CON(name, tableName = "accounts"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT _id, account_name, account_type FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#viber
def db_to_csv_VD(name, tableName = "phonebookcontact"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT _id, native_id, phone_label, low_display_name, viber, contact_lookup_key, contact_hash, joined_date  FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#viber
def db_to_csv_VM(name, tableName = "messages"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT _id, conversation_id, msg_date, unread, extra_bucket_name, body, msg_info, timebomb FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#telegram
def db_to_csv_TEL(name, tableName = "messages_v2"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT mid, uid, read_state, send_state, date, data, out, media FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#facebook messenger contacts
def db_to_csv_FBS(name, tableName = "search_items"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT fbid, display_name, first_name, last_name, picture_url, thread_type FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#facebook messenger messages
def db_to_csv_FBT(name, tableName = "thread_participants"):
    #set the directory of the file to our current directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)

    #connect with the database
    con = sqlite3.connect(db_path)

    #read the database file
    df = pd.read_sql_query("SELECT _id, thread_key, user_key, type, last_read_receipt_time, last_delivered_receipt_time, is_admin, admin_type FROM {}".format(tableName), con)

    #convert db to csv, is not a string
    df.to_csv(r'{}.csv'.format(name[:-3]), index = False)

    #set filepath name
    filepath = name[:-3] + ".csv"
    return filepath

#signal
def db_to_csv_SIG(name, tableName = "mms"):
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
    #os.chdir('./ScriptFiles')

    #iterate through each file in the directory
    for entry in os.scandir(path): 
        if entry.path.lower().endswith(('.txt', '.png', '.jpg', 'jpeg', '.db') + noExtension):
            #sleep timer for databases to load and convert
            time.sleep(.1)
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
            time.sleep(.1)
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
