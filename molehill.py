#Week 09/19/2021
#Task:
#Create a python script that opens a window that has a start button on it. 
#When you click the start button, a picture and text will pop up. 

#Tkinter is a Python binding to the Tk GUI toolkit. 
#It is the standard Python interface to the Tk GUI toolkit, and is Python's de facto standard GUI. 
#Please install Pillow "pip install Pillow"

import tkinter
import tkinter.scrolledtext
import tkinter.messagebox
import tkinter.filedialog
import os

abspath = os.path.abspath(__file__) # Get current file's directory
os.chdir(os.path.dirname(abspath)) # Change working directory to current file's

program_version = "20210924"

win=tkinter.Tk() # defines window
win.title('Molehill %s' % program_version) # titles window
win.geometry('500x500') # sets window resolution
win.resizable(height = None, width = None)
picture = tkinter.PhotoImage(file=r'constutions.png').subsample(5,5) #Defines the image

def set_layout1():
    """Sets layout to layout 1."""
    # Creating two buttons that will open up text/picture of constitution
    btn1 = tkinter.Button(text="Click to see text of US constitution", command=text_constitution, width=35, height=2)
    btn2 = tkinter.Button(text="Click to see picture of US constitution", command=pic_constitution, width=35, height=2)
    # Defines three global variables, see comments below
    global window_content, text_displaying, pic_displaying
    window_content = tkinter.Label(win) # The content widget
    text_displaying, pic_displaying = False, False # The state of whether a text/pic is displaying
    # Places buttons on grid
    btn1.grid(row=1, column=2)
    btn2.grid(row=1, column=1)
    # Destroys original startup button
    btn0.destroy()

def text_constitution():
    """Changes the text of button to the text of the US constitution after clicking it."""
    text = "US constitution: We the People of the United States, \nin Order to form a more perfect Union, establish Justice, \ninsure domestic Tranquility, provide for the common defence, \npromote the general Welfare, and secure the Blessings of Liberty to \nourselves and our Posterity,do ordain and establish \nthis Constitution for the United States of America."
    global window_content, text_displaying, pic_displaying # Three global variables defined in set_layout1()
    window_content.destroy() # Destroys current content widget
    # Will only proceed if there is no text displaying.
    if text_displaying == False:
		# Creates textbox and inserts content into textbox
	    window_content = tkinter.scrolledtext.ScrolledText(win, width=58, height=27)
	    window_content.insert(tkinter.END, text)
	    
	    window_content.grid(row=2, columnspan=20) # Place widget on grid
	    text_displaying, pic_displaying = True, False # Refreshes state variables
    else:
	    text_displaying, pic_displaying = False, False # refreshes state variables

def pic_constitution():
    """Changes the text of button to the picture of the US constitution after clicking it."""
    global window_content, text_displaying, pic_displaying
    window_content.destroy()
    if pic_displaying == False:
	    window_content = tkinter.Label(win, image=picture, width=450, height=450) # Creates label widget
	    window_content.grid(row=2, columnspan=20) # Place widget on grid
	    text_displaying, pic_displaying = False, True # Refreshes state variables
    else:
	    text_displaying, pic_displaying = False, False # refreshes state variables

def about():
	"""Displays "about" dialog."""
	tkinter.messagebox.showinfo("About","Molehill version %s\nBy Team HillsHaveEyes" % program_version)

def file_dialog():
	"""Hides main window and starts file dialog."""
	win.withdraw()
	file_path = tkinter.filedialog.askopenfilename()
	win.wm_deiconify()
	return file_path

def open_dialog(): # NEEDS IMPLEMENTATION
	"""Opens dialog to open file.
	NOT IMPLEMENTED"""
	tkinter.messagebox.showinfo("ERROR","Not implemented...")
	file_path = file_dialog()

def save_dialog(): # NEEDS IMPLEMENTATION
	"""Opens dialog to save file.
	NOT IMPLEMENTED"""
	tkinter.messagebox.showinfo("ERROR","Not implemented...")
	file_path = file_dialog()

# creates a singular button on screen and places it at given coordinates
btn0=tkinter.Button(win,text="Click Me", width=10,height=5,
					command=set_layout1)
btn0.place(relx=0.5,y=-10,rely=0.5,anchor='center')

# creates menu bar and configures main window to use it
menu_bar = tkinter.Menu(win)
win.config(menu=menu_bar)

# defines file menu
file_menu = tkinter.Menu(menu_bar, tearoff="off")
file_menu.add_command(label='New') 
file_menu.add_command(label='Open...', command=open_dialog) 
file_menu.add_command(label='Save', command=save_dialog)
file_menu.add_separator() 
file_menu.add_command(label='Exit', command=win.quit)

# defines edit menu
edit_menu = tkinter.Menu(menu_bar, tearoff="off")
edit_menu.add_command(label='Cut')
edit_menu.add_command(label='Copy')
edit_menu.add_command(label='Paste')

# defines view menu
#view_menu = tkinter.Menu(menu_bar, tearoff="off")
#view_menu.add_command(label='')
#view_menu.add_command(label='')

# defines help menu
help_menu = tkinter.Menu(menu_bar, tearoff="off")
help_menu.add_command(label='About', command=about)

# adds menus to bar
menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
#menu_bar.add_cascade(label='View', menu=view_menu)
menu_bar.add_cascade(label='Help', menu=help_menu)

# spawns window
win.mainloop()