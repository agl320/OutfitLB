import tkinter as tk


class Clothing():
    def __init__(self, name, clothing_type, desc="", colour="#ffffff", clean=True):
        self.name = name
        self.desc = desc
        self.clothing_type = clothing_type.lower()
        self.colour = colour
        

    def print_info(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.desc}")

    def get_name(self):
        return self.name

    def is_clean(self):
        return self.clean 


class Top(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", sleeves=True, clean=True):
        super().__init__(name, "top", desc, colour, clean)
        self.sleeves = sleeves

class Bottom(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", clean=True):
        super().__init__(name, "top", desc, colour, clean)

class Shoes(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", clean=True):
        super().__init__(name, "top", desc, colour, clean)
        
        
def add_c(txt):
    global all_clothing, v

    add_c_name = txt.get("1.0",tk.END).replace('\n',' ')
    #new_c_name = str(input())
    print(f"[+ type:{v.get()}] {add_c_name}")

    match v.get():
        case 0:
            all_clothing.append(Top(add_c_name, "Custom"))
        case 1:
            all_clothing.append(Bottom(add_c_name, "Custom"))
        case 2:
            all_clothing.append(Shoes(add_c_name, "Custom"))
    clothing_lb.insert(tk.END, add_c_name)
    
def print_debug(var, index, mode):
    global v
    print(f"Add switched to {v.get()}")

all_clothing = []

# outfit combinations
outfits = []


shirt_1 = Top("Blue Shirt", "Blue shirt I bought at Wendy's")
shirt_2 = Top("Black Shirt", "Blue shirt I bought at McDonald's")
shirt_3 = Top("Red Shirt", "Blue shirt I bought at Arby's")

all_clothing.append(shirt_1)
all_clothing.append(shirt_2)
all_clothing.append(shirt_3)


# TK RENDERING

window = tk.Tk()
window.geometry('1200x800')
w_title = window.title("Outfit Manager")

clothing_lb = tk.Listbox(window, height = 10, width = 15,bg = "grey",activestyle = 'dotbox',font = "Helvetica",fg = "yellow")

# All clothing column
print("ADDING CLOTHING...")

for i, clothing in enumerate(all_clothing):
    clothing_lb.insert(i, clothing.get_name())
    print(f"[+] {clothing.get_name()}")

print("FINISHED ADDING CLOTHING")

# Add clothing
add_c_txt = tk.Text(window,width=15,height=2)

add_c_b = tk.Button(
    window,
    text="ADD", 
    padx=10, 
    pady=5,
    command=lambda: add_c(add_c_txt)
    )

# Add clothing type
v = tk.IntVar(window, 0) # default value is top

# debugging
v.trace('w',print_debug)

add_c_rb_top = tk.Radiobutton(window, text="Top", variable=v, value=0)
add_c_rb_bot = tk.Radiobutton(window, text="Bottom", variable=v, value=1)
add_c_rb_sh = tk.Radiobutton(window, text="Shoes", variable=v, value=2)

# Widget placement
window.config(pady=10,padx=10)
clothing_lb.grid(row=0,column=0,columnspan=2)
add_c_rb_top.grid(row=1,column=0,sticky="W")
add_c_rb_bot.grid(row=2,column=0,sticky="W")
add_c_rb_sh.grid(row=3,column=0,sticky="W")
add_c_txt.grid(row=1,column=1,rowspan=3)
add_c_b.grid(row=1,column=2,rowspan=3)


window.mainloop()
