# Cleaning code from main
# removing use of global variables

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

# removal of prefix
from ouser import *

class AddFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

class PreviewFrame(tk.Frame):
    def __init__(self, parent, all_clothing, clothing_lb, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.all_clothing = all_clothing
        self.clothing_lb = clothing_lb

        self.filepath_add=""
        self.filepath_current = "image.jpg"
        self.image_current = Image.open(self.filepath_current).resize((50, 50))        
        self.image_current = ImageTk.PhotoImage(self.image_current)

        # default no image
        self.prev_image = tk.Label(self, image=self.image_current)

        # <> CLOTHING PANEL PREVIEW
        self.prev_label_var = tk.StringVar()
        self.prev_label = tk.Label(self, textvariable=self.prev_label_var, font=("Helvetica", 10),justify= tk.LEFT) 
        
        # <> PRINTING PREVIEW DATA
        self.getPreview()

        # <> WIDGET DISPLAY
        self.widgetDisplay()

    def getPreview(self):
        
        # gets selected item in listbox
        self.prev_select = self.clothing_lb.curselection()
        # gets value of selected
        # gets index of selected
        print(f"Index: {self.prev_select[0]}")
        print(self.all_clothing[self.prev_select[0]].print_info())
        # check if no listbox item selected
        if not self.prev_select:
            print(">> None selected.")
            self.prev_label_var.set("None selected.")
            self.prev_label = tk.Label(self.parent, textvariable=self.prev_label_var, font=("Helvetica", 10),justify= tk.LEFT) 

            self.prev_image = tk.Label(self.parent, text="No image.")
        else:
            print(">> Selected")
            #strvar.set(clothing_lb.get(c_selection))
            self.prev_label_var.set(self.all_clothing[self.prev_select[0]].get_info())
            self.prev_label = tk.Label(self.parent, textvariable=self.prev_label_var, font=("Helvetica", 10),justify= tk.LEFT) 

            # getting and displaying current clothing image
            self.filepath_current = self.all_clothing[self.prev_select[0]].get_image()
            if not self.filepath_current or self.filepath_current.isspace():
                self.filepath_current = "image.jpg"
                print(">> No image for current")

            self.image_current = Image.open(self.filepath_current).resize((50, 50))
            self.image_current = ImageTk.PhotoImage(self.image_current)
            self.prev_image.configure(image=self.image_current)
            # prevent garbage collection
            self.prev_image.image = self.image_current

    def widgetDisplay(self):
        # clothing preview (right of all clothing list)
        self.prev_label.grid(row=0,column=4,sticky="W")
        self.prev_image.grid(row=0,column=5,sticky="W")

class ClosetFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # <> LEFT LIST AND RIGHT PREVIEW
        self.lb_frame = tk.Frame(parent)
        self.lb_preview = tk.Frame(parent)

        # <> CLOSET DISPLAY
        # Scrollbar and Listbox
        self.sb = tk.Scrollbar(self.lb_frame, orient=tk.VERTICAL) 
        # display current list box of closet
        self.clothing_lb = tk.Listbox(self.lb_frame, yscrollcommand = self.sb.set, height = 10, width = 25,bg = "grey",activestyle = 'dotbox',font = "Helvetica",fg = "yellow")
        self.sb['command'] = self.clothing_lb.yview
        
        # <> PREVIEW BUTTON
        self.prev_b = tk.Button(self.lb_preview, text='Preview', command=self.callPreview)
        
        # + EXAMPLE DATA
        self.all_clothing = []
        self.example_data()

        # <> WIDGET DISPLAY
        self.widgetDisplay()

    def callPreview(self):
        """
        Creates a preview frame and changes the contents of such preview frame.
        Then places the preview frame using grid. 
        """
        self.previewframe = PreviewFrame(self.lb_preview, self.all_clothing, self.clothing_lb) # maybe self.lb_preview?
        self.previewframe.grid(row=0,column=2,sticky="W")
    
    # WIDGET DISPLAYING
    # GRID FORMAT
    def widgetDisplay(self):
        # lb_frame
        self.clothing_lb.grid(row=0,column=0,columnspan=3)
        self.sb.grid(row=0,column=2, sticky='NSE')

        # lb_preview
        self.prev_b.grid(row=0,column=1,sticky="W")

        # MAIN FRAME DISPLAY
        self.lb_frame.grid(row=0,column=0)
        self.lb_preview.grid(row=0,column=1)
        

    def example_data(self):
        shirt_1 = Top("Blue Shirt", "Blue shirt I bought at Wendy's")
        shirt_2 = Top("Black Shirt", "Black shirt I bought at McDonald's")
        shirt_3 = Top("Red Shirt", "Red shirt I bought at Arby's", clean=False)

        self.all_clothing.append(shirt_1)
        self.all_clothing.append(shirt_2)
        self.all_clothing.append(shirt_3)

        print("ADDING CLOTHING...")

        for i, clothing in enumerate(self.all_clothing):
            self.clothing_lb.insert(i, clothing.get_name())
            print(f"[+] {clothing.get_name()}")

            if clothing.is_clean():
                self.clothing_lb.itemconfig(i,{'bg':'Green'})
            else:
                self.clothing_lb.itemconfig(i,{'bg':'Red'})

        print("FINISHED ADDING CLOTHING")

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.cframe = ClosetFrame(self)
        

        parent.geometry('650x500')
        parent.title("Outfit Manager")

        # widget placement
        self.grid(padx=5, pady=5)
        self.cframe.grid(row=0,column=0,columnspan=3,sticky="W")
        
        

def main(): 
    agl13 = User("GH", "Andrew", "agl13")
    agl13.new_closet("AC",'0')
    agl13.new_closet("DC",'1')

    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == '__main__':
    main()