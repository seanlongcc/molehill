#Sean's Version
import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.messagebox
import tkinter.filedialog
from tkinter import StringVar, filedialog

#defines the window
win = tk.Tk()
win.title('Molehill V2')
win.geometry('500x500')

#picture for testing
picture = tkinter.PhotoImage(file=r'constitution.png').subsample(5,5) #Defines the image

#file browser
def browseFiles():
    #look for a file from your directory and read it
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text Files", "*.txt"), ("All Files", "*.*")))
    filename = open(filename, 'r')
    data = filename.read()
    #insert the data into the content window
    content.insert(tk.END, data)

    filename.close()   

#start screen layout
def layout0():
    #destry the start button and initialize global variable for later
    btn0.destroy()
    global content
    #defines  the window to place content
    content = tk.Label(win)

    #create action buttons
    btn1 = tk.Button(text = 'Text', width = 10,command = layout1)
    btn2 = tk.Button(text = 'Picture', width = 10, command = layout2)
    upbtn = tk.Button(win, text = 'Browse Files', command = browseFiles)

    #place action buttons
    btn1.grid(row = 1, column = 1)
    btn2.grid(row = 1, column = 2)
    upbtn.grid(row = 1, column = 3)

#layout 1 - text view
def layout1():
    global content
    content.destroy()
    
    #creates area for scrolled text and places it
    content = st.ScrolledText(win, wrap = tk.WORD, width = 50, height = 25)
    content.place(relx=0.5,rely=0.5,anchor='center')

#layour 2 - picture view
def layout2():
    global content
    content.destroy()

    #creates area for picture and places it
    content = tkinter.Label(win, image=picture, width=400, height=400)
    content.place(relx=0.5,rely=0.5,anchor='center')

#initial start button
btn0 = tk.Button(text = 'Start', width = 10, command = layout0)
btn0.place(relx=0.5,rely=0.5,anchor='center')

#spawns window
win.mainloop()