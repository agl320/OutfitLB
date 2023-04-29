#Import Tkinter library
from tkinter import *
#Create an instance of Tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x350")
#Create ListBoxes
listboxA=Listbox(win, exportselection=False) #Create listboxA
listboxA.pack(padx=10,pady=10,fill=BOTH,expand=True)
listboxB=Listbox(win,exportselection=False) #Create ListboxB
listboxB.pack(padx=10,pady=10,fill=BOTH,expand=True)
listboxA.insert(1, "1.Python")
listboxA.insert(2, "2.Java")
listboxA.insert(3, "3.C++")
listboxA.insert(4, "4.Rust")
listboxA.insert(5, "5.GoLang")
listboxB.insert(1, "a.C#")
listboxB.insert(2, "b.JavaScript")
listboxB.insert(3, "c.R")
listboxB.insert(4, "d.Php")
listboxB.insert(5, "e.CoffeeScript")
listboxB.insert(6, "f.Curl")
win.mainloop()