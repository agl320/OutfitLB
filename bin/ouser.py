class User():
    def __init__(self, firstName, lastName, userName):
        self.firstName = firstName 
        self.lastName = lastName 
        self.userName = userName 
        self.closet_lst = {}
        self.outfit_lst = []

    def new_outfit(self, name, top, bottom, shoes):
        self.outfit_lst.append(Outfit(name,top,bottom,shoes))

    def new_closet(self, name, ID, desc=""):
        self.closet_lst[ID]=Closet(name, desc)

    def delete_closet(self, ID):
        self.closet_lst.pop(ID, None)

    def get_closet(self, ID):
        return self.closet_lst[ID]
    
    def get_outfits(self):
        return self.outfit_lst

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

    def save_outfits(self,outfits_new):
        self.outfit_lst = outfits_new
        print(f"UPDATED OUTFITS: {self.outfit_lst}")

class Outfit():
    def __init__(self, name, top, bottom, shoes):
        self.name = name
        self.top = top
        self.bottom = bottom
        self.shoes = shoes 
    
    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name 
    
    def set_comb(self, top_new, bottom_new, shoes_new):
        self.top = top_new
        self.bottom = bottom_new
        self.shoes = shoes_new
    
    def set_top(self, top_new):
        self.top = top_new
    
    def set_bottom(self, bottom_new):
        self.bottom = bottom_new
    
    def set_shoes(self, shoes_new):
        self.shoes = shoes_new
    
    def isClean(self):
        print(f"OUTFIT CLEAN CHECK: {self.top}, {self.bottom}, {self.shoes}")
        if (self.top==None or self.top.is_clean()) and (self.bottom==None or self.bottom.is_clean()) and (self.shoes==None or self.shoes.is_clean()):
            return True
        else:
            return False

    def __repr__(self):
        return self.name
        
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
    def __init__(self, name, desc="", colour="#ffffff", type=0, filepath="image.jpg", clean=False, ckmean=None):
        self.name = name
        self.desc = desc
        self.colour = colour
        self.clean = clean
        self.type = type
        self.filepath = filepath
        self.ckmean = ckmean # pyplot figure

    """
    GETTERS
    """

    def get_name(self):
        return self.name
    
    def get_info(self):
        info_str = f"Name: {self.name}\nDescription: {self.desc}\nType: {self.type}"
        return info_str
    
    def get_desc(self):
        return self.desc
    
    def get_type(self):
        return self.type

    def get_image(self):
        return self.filepath
    
    def get_ckmean(self):
        return self.ckmean
    
    def is_clean(self):
        return self.clean 
    
    def print_info(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.desc}")

    """
    SETTERS
    """

    def set_name(self, new_name):
        self.name = new_name

    def set_desc(self, new_desc):
        self.desc = new_desc 
    
    def set_clean(self, new_clean):
        self.clean = new_clean

    def set_type(self, new_type):
        self.type = new_type

    def set_ckmean(self, new_ckmean):
        self.ckmean = new_ckmean

    def save(self, name, desc, clean, type):
        self.set_name(name)
        self.set_desc(desc) 
        self.set_clean(clean)
        self.set_type(type)
    
    # sets image file path for clothing
    def set_image(self, filepath):
        self.filepath = filepath
    

    def __repr__(self):
        return f"{self.name} of type {self.__class__.__name__}"

class Top(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", type=0, sleeves=True, filepath="image.jpg", clean=False):
        super().__init__(name, desc, colour, type, filepath, clean)
        self.sleeves = sleeves

class Bottom(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", type=1, filepath="image.jpg", clean=False):
        super().__init__(name, desc, colour, type, filepath, clean)

class Shoes(Clothing):
    def __init__(self, name, desc="", colour="#ffffff", type=2, filepath="image.jpg", clean=False):
        super().__init__(name, desc, colour, type, filepath, clean)
