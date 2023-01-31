import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk


# User class
# - User will have set of closets
# - Each closet contains dict of Clothing
# - - Each closet can be accessed by ID
class User():
    def __init__(self, firstName, lastName, userName):
        self.firstName = firstName 
        self.lastName = lastName 
        self.userName = userName 
        self.closet_lst = {}

    def new_closet(self, name, ID, desc=""):
        self.closet_lst[ID]=Closet(name, desc)

    def get_closet(self, ID):
        return self.closet_lst[ID]

    # returns dict of all closets
    def get_all(self):
        return self.closet_lst.copy()

    def get_all_closet_name(self):
        # get closet list values in dict 
        # wrap and convert to list since values() returns view
        name_lst = list(self.closet_lst.values())
            
        return name_lst.copy()

    def get_all_closet_id(self):
        id_list = list(self.closet_lst.keys())
        return id_list.copy()

    def view_all_closets(self):
        print(self.closet_lst)

    def save_closet(self,closet_new,ID):
        self.closet_lst[ID].set_closet(closet_new)
        print(f"UPDATED CLOSET [{ID}]: {self.closet_lst}")
        
# Closet class
# - Closet contains dict of Clothing (Top, Bottom, Shoes)
# - Methods to add clothing
class Closet():
    def __init__(self, name, desc=""):
        self.clothing_lst = []
        self.name = name

    def add_Top(self, *args):
        self.clothing_lst.append(Top(*args))

    def add_Bottom(self, *args):
        self.clothing_lst.append(Bottom(*args))

    def add_Shoes(self, *args):
        self.clothing_lst.append(Shoes(*args))
    
    # Return all clothing in list form
    def get_all(self):
        return self.clothing_lst.copy()
    
    def set_closet(self, clothing_lst_new):
        self.clothing_lst = clothing_lst_new
    
    

    def __repr__(self):
        return self.name

# Clothing class
# Getters:
# - Get name
# - Is clean?
# - Print info
# - Get info
# - Get image filepath
# Setters:
# - Set image filepath
class Clothing():
    def __init__(self, name, desc="", colour="#ffffff", clean=1, filepath="image.jpg"):
        self.name = name
        self.desc = desc
        self.colour = colour
        self.clean = clean
        self.filepath=filepath

    def get_name(self):
        return self.name
    
    def is_clean(self):
        return self.clean 
    
    def print_info(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.desc}")

    def get_info(self):
        info_str = f"Name: {self.name}\nDescription: {self.desc}"
        return info_str
    
    # sets image file path for clothing
    def set_image(self, filepath):
        self.filepath = filepath
    
    def get_image(self):
        return self.filepath

    def __repr__(self):
        return f"{self.name} of type {self.__class__.__name__}"

class Top(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", sleeves=True, clean=1, filepath=""):
        super().__init__(name, desc, colour, clean, filepath)
        self.sleeves = sleeves

class Bottom(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", clean=1, filepath=""):
        super().__init__(name, desc, colour, clean, filepath)

class Shoes(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", clean=1, filepath=""):
        super().__init__(name, desc, colour, clean, filepath)


# Add clothing to clothing list function
def add_c(en, txt):
    global all_clothing, v, clean_var, filepath_add

    # get name and description 
    add_c_name = en.get()
    add_c_txt = txt.get("1.0",tk.END).replace('\n',' ')
    #new_c_name = str(input())

    # If empty string, use no name
    if not add_c_name or add_c_name.isspace():
        add_c_name = "No name"

    # debug print
    print(f"[+ type:{v.get()}] {add_c_name}")

    # Adding to clothing list -> type check
    match v.get():
        case 0:
            all_clothing.append(Top(add_c_name, add_c_txt, "Custom", clean=clean_var.get(), filepath=filepath_add))
        case 1:
            all_clothing.append(Bottom(add_c_name, add_c_txt, "Custom", clean=clean_var.get(), filepath=filepath_add))
        case 2:
            all_clothing.append(Shoes(add_c_name, add_c_txt, "Custom", clean=clean_var.get(), filepath=filepath_add))
    
    # RESET filepath
    filepath_add=""

    # Check if clean
    if clean_var.get():#[].is_clean():
        clothing_lb.insert(tk.END, add_c_name)
        clothing_lb.itemconfig(tk.END,{'bg':'Green'})
    else:
        clothing_lb.insert(tk.END, add_c_name)
        clothing_lb.itemconfig(tk.END,{'bg':'Red'})
    
# 
def print_debug(var, index, mode):
    global v
    print(f"Add switched to {v.get()}")

def get_preview():
    global c_prev_label, clothing_lb, strvar, c_prev_image
    #c_prev_label = tk.Label(text="Convert to German Cognate", font=("Arial", 15, 'bold'))
    #c_selected = clothing_lb.get(clothing_lb.curselection()[0])
    
    # gets selected
    c_selection = clothing_lb.curselection()
    # gets value of selected
    # print(clothing_lb.get(c_selection))
    # gets index of selected
    print(c_selection[0])
    print(all_clothing[c_selection[0]].print_info())

    # check if no listbox item selected
    if not c_selection:
        print(">> None selected.")
        strvar.set("None selected.")
        c_prev_label = tk.Label(window, textvariable=strvar, font=("Helvetica", 15)) 
        c_prev_image = tk.Label(window, text="No image.")
    else:
        print(">> Selected")
        #strvar.set(clothing_lb.get(c_selection))
        strvar.set(all_clothing[c_selection[0]].get_info())
        c_prev_label = tk.Label(window, textvariable=strvar, font=("Helvetica", 15)) 

        # getting and displaying current clothing image
        filepath_current = all_clothing[c_selection[0]].get_image()
        if not filepath_current or filepath_current.isspace():
            filepath_current = "image.jpg"
            print("> No image for current")

        image_current = Image.open(filepath_current).resize((50, 50))
        image_current = ImageTk.PhotoImage(image_current)
        c_prev_image.configure(image=image_current)
        # prevent garbage collection
        c_prev_image.image = image_current
    
def upload():
    global filepath_add
    filepath_add = ""
    # uploading file (image)
    filepath_add = filedialog.askopenfilename(filetypes = (("jpeg files", "*.jpg"),("png files", "*.png"),("all files","*.*")))
    print(filepath_add)

# DEBUG
def dropdown_callback(*args):
    global all_clothing, clothing_lb, agl13, dropdown
    
    # UPDATE
    print("Closet selected: ", dropdown.get())

    # CLEAR
    clothing_lb.delete(0,tk.END)
    all_clothing = []

    all_clothing = agl13.get_closet(dropdown.get()).get_all()
    
    for i, clothing in enumerate(all_clothing):
        clothing_lb.insert(i, clothing.get_name())

        print(f"[+] {clothing.get_name()}")
        print(f"\t[>] CLEAN:{clothing.is_clean()}")
        
        if clothing.is_clean():
            clothing_lb.itemconfig(i,{'bg':'Green'})
        else:
            clothing_lb.itemconfig(i,{'bg':'Red'})
            


def save_to_user():
    global all_clothing, dropdown, agl13
    agl13.save_closet(all_clothing,dropdown.get())


#def update_lb():
 #       global window, clothing_lb
  #      window.after(100, update_lb)

# MAIN
# GET Closet
# UPDATE Closet
# SAVE Closet

# current closet init
all_clothing = []

# outfit combinations init
outfits = []

# EXAMPLE closet =================================
# NEW USER
    
agl13 = User("GH", "Andrew", "agl13")
agl13.new_closet("AC",'0')
agl13.new_closet("DC",'1')

shirt_1 = Top("Blue Shirt", "Blue shirt I bought at Wendy's")
shirt_2 = Top("Black Shirt", "Blue shirt I bought at McDonald's")
shirt_3 = Top("Red Shirt", "Blue shirt I bought at Arby's", clean=False)

all_clothing = agl13.get_closet('0').get_all()

all_clothing.append(shirt_1)
all_clothing.append(shirt_2)
all_clothing.append(shirt_3)

# END EXAMPLE ====================================

# Empty filepath init
filepath_add=""

# TK RENDERING

window = tk.Tk()
window.geometry('650x500')
w_title = window.title("Outfit Manager")

# All clothing column
all_c_frame = tk.Frame(window)


# Drop down menu

dropdown_var = tk.StringVar()
dropdown = ttk.Combobox(all_c_frame, textvariable=dropdown_var, values=agl13.get_all_closet_id())
dropdown.current(0)
dropdown.bind("<<ComboboxSelected>>", dropdown_callback)


# vertical scrollbar for all clothing

#all_c_label = tk.Label(all_c_frame, text="ALL CLOTHING",justify= tk.LEFT)
w_sb = tk.Scrollbar(window, orient=tk.VERTICAL) 
#w_sb.config(command = clothing_lb.yview)

# DISPLAY current list box of closet
clothing_lb = tk.Listbox(all_c_frame, yscrollcommand=w_sb.set, height = 10, width = 25,bg = "grey",activestyle = 'dotbox',font = "Helvetica",fg = "yellow")
w_sb['command'] = clothing_lb.yview

# DEBUG
print("ADDING CLOTHING...")

for i, clothing in enumerate(all_clothing):
    clothing_lb.insert(i, clothing.get_name())
    print(f"[+] {clothing.get_name()}")

    if clothing.is_clean():
        clothing_lb.itemconfig(i,{'bg':'Green'})
    else:
        clothing_lb.itemconfig(i,{'bg':'Red'})

print("FINISHED ADDING CLOTHING")

# Clean clothing column
#clean_c_frame = tk.Frame(window)

#clean_c_label = tk.Label(clean_c_frame, text="CLEAN CLOTHING",justify= tk.LEFT)
#clean_c_lb = tk.Listbox(clean_c_frame, height = 10, width = 25,bg = "grey",activestyle = 'dotbox',font = "Helvetica",fg = "yellow")

# CLOTHING PANEL PREVIEW
strvar = tk.StringVar()
c_prev_label = tk.Label(window, textvariable=strvar, font=("Helvetica", 10, 'bold'),justify= tk.LEFT) 
c_preview_b = tk.Button(window, text='Preview', command=get_preview)

filepath_current = "image.jpg"
image_current = Image.open(filepath_current).resize((50, 50))        
image_current = ImageTk.PhotoImage(image_current)

c_prev_image = tk.Label(window, text="No image.", image=image_current)


# Add clothing
# framing for packing together below
add_c_frame = tk.Frame(window)
add_c_frame_2 = tk.Frame(window)

# Name frame
add_c_en_label = tk.Label(add_c_frame_2, text="Name",justify= tk.LEFT)
add_c_en = tk.Entry(add_c_frame_2,width=20)

# Description frame
add_c_en_label_2 = tk.Label(add_c_frame_2, text="Description",justify= tk.LEFT)
add_c_txt = tk.Text(add_c_frame_2, width=15,height=2)

# Clean? checklist w/ Description frame
clean_var =  tk.IntVar()
clean_cb = tk.Checkbutton(add_c_frame_2, text = "Clean?", variable=clean_var)




# Button submit
add_c_b = tk.Button(
    window,
    text="ADD", 
    padx=10, 
    pady=5,
    command=lambda: add_c(add_c_en, add_c_txt)
    )

# Add clothing TYPE
# Clothing type frame
add_c_frame_type = tk.Frame(window)

v = tk.IntVar(window, 0) # default value is top

# debugging
v.trace('w',print_debug)

add_c_rb_top = tk.Radiobutton(add_c_frame_type, text="Top", variable=v, value=0)
add_c_rb_bot = tk.Radiobutton(add_c_frame_type, text="Bottom", variable=v, value=1)
add_c_rb_sh = tk.Radiobutton(add_c_frame_type, text="Shoes", variable=v, value=2)

img_b = tk.Button(add_c_frame_type, text="Image", command=upload)

# SAVE 
closet_save_b = tk.Button(window, text='Save closet', command=save_to_user)


# Widget placement
window.config(pady=10,padx=10)


# ALL CLOTHING FRAME
dropdown.grid(row=0,column=0, sticky="NW")
# all clothing list
all_c_frame.grid(row=0,column=0,columnspan=3,sticky="W")
#all_c_label.grid(row=0,column=0,columnspan=3,sticky="W")
clothing_lb.grid(row=1,column=0,columnspan=3)

w_sb.grid(row=0,column=2, sticky='NSE')

# clean clothing list
#clean_c_frame.grid(row=0,column=5,columnspan=3,sticky="W")
#clean_c_label.grid(row=0,column=0,columnspan=3,sticky="W")
#clean_c_lb.grid(row=1,column=0,columnspan=3)


# clothing preview (right of all clothing list)
c_preview_b.grid(row=0,column=3,sticky="W")
c_prev_label.grid(row=0,column=4,sticky="W")
c_prev_image.grid(row=0,column=5,sticky="W")

# add clothing type widgets
add_c_frame_type.grid(row=1,column=0,rowspan=3)
add_c_rb_top.grid(row=0,column=0,sticky="W")
add_c_rb_bot.grid(row=1,column=0,sticky="W")
add_c_rb_sh.grid(row=2,column=0,sticky="W")
# add image (under clothing type)
img_b.grid(row=3,column=0,rowspan=1,sticky="N")

# clothing add widgets
add_c_frame.grid(row=1,column=1)
add_c_frame_2.grid(row=2, column=1)

#add_c_en.grid(row=1,column=1,rowspan=1,sticky="N")
# name 
add_c_en_label.grid(row=0,column=0,sticky="W")
add_c_en.grid(row=1,column=0,sticky="N")

# description
add_c_en_label_2.grid(row=2,column=0,sticky="W")
add_c_txt.grid(row=3,column=0,rowspan=1,sticky="N")
clean_cb.grid(row=4,column=0,rowspan=1,sticky="N")


# button subimt
add_c_b.grid(row=1,column=2,rowspan=3, sticky="S")

closet_save_b.grid(row=6,column=0)

window.mainloop()
