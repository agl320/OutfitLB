class User():
    def __init__(self, firstName, lastName, userName):
        self.firstName = firstName 
        self.lastName = lastName 
        self.userName = userName 
        self.closet_lst = {}

    def new_closet(self, name, ID, desc=""):
        self.closet_lst[ID]=Closet(name, desc)

    def delete_closet(self, ID):
        self.closet_lst.pop(ID, None)

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
    
    def get_all_closet_comb(self):
        name_lst = list(self.closet_lst.values())
        id_list = list(self.closet_lst.keys())

        for i in range(len(name_lst)):
            name_lst[i] = str(name_lst[i]) + f" {id_list[i]}"

        return name_lst

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
        self.filepath = filepath

    def get_name(self):
        return self.name
    
    def get_info(self):
        info_str = f"Name: {self.name}\nDescription: {self.desc}"
        return info_str
    
    def get_desc(self):
        return self.desc
    
    def is_clean(self):
        return self.clean 
    
    def print_info(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.desc}")

    def set_name(self, new_name):
        self.name = new_name

    def set_desc(self, new_desc):
        self.desc = new_desc 
    
    def set_clean(self, new_clean):
        self.clean = new_clean

    def save(self, new_name, new_desc, new_clean):
        self.set_name(new_name)
        self.set_desc(new_desc) 
        self.set_clean(new_clean)

    
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
