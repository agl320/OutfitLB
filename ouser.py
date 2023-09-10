import json


class Manage:
    def __init__(self):
        self.user_lst = {}

    def userLogOut(self, u_file):
        with open(u_file, "r") as read_file:
            d_import = json.load(read_file)
            read_file.close()

        d_import["loggedIn"] = 0

        with open(u_file, "w") as json_file:
            json.dump(d_import, json_file, indent=4)
            json_file.close()

    def import_from_file(self, u_file):
        print("[!] IMPORTING [!]")

        # with open(f"users/{u_file}.json", "r") as read_file:
        #     d_import = json.load(read_file)

        with open(u_file, "r") as read_file:
            d_import = json.load(read_file)

        # CHANGE TO LOGGED IN
        d_import["loggedIn"] = 1

        # Save the updated data back to the file
        # with open(f"users/{u_file}.json", "w") as json_file:
        #     json.dump(d_import, json_file, indent=4)

        with open(u_file, "w") as json_file:
            json.dump(d_import, json_file, indent=4)

        # return username of imported user
        # check if user exists; if so, delete
        u_name = d_import["userName"]
        try:
            if self.user_lst[u_name]:
                print("[!] User exists, overwritting...")
                del self.user_lst[u_name]
        except:
            print("[!] User does not exist yet, creating new...")

        # creation of empty new user
        self.user_lst[u_name] = User(
            d_import["firstName"], d_import["lastName"], u_name
        )

        for i, closet in enumerate(d_import["closets"]):
            ID = d_import["closets"][i]["ID"]
            self.user_lst[u_name].new_closet(d_import["closets"][i]["name"], ID)
            for clothing in closet["clothing"]:
                # multiple if statements in case each type of clothing has different attributes

                if clothing["type"] == 0:
                    self.user_lst[u_name].get_closet(ID).add_Top(
                        clothing["name"],
                        clothing["ID"],
                        clothing["desc"],
                        clothing["colour"],
                        clothing["type"],
                        clothing["filepath"],
                        clothing["clean"],
                    )
                elif clothing["type"] == 1:
                    self.user_lst[u_name].get_closet(ID).add_Bottom(
                        clothing["name"],
                        clothing["ID"],
                        clothing["desc"],
                        clothing["colour"],
                        clothing["type"],
                        clothing["filepath"],
                        clothing["clean"],
                    )
                elif clothing["type"] == 2:
                    self.user_lst[u_name].get_closet(ID).add_Shoes(
                        clothing["name"],
                        clothing["ID"],
                        clothing["desc"],
                        clothing["colour"],
                        clothing["type"],
                        clothing["filepath"],
                        clothing["clean"],
                    )
                else:
                    print("[X] Error in type import.")

        for i, outfit in enumerate(d_import["outfits"]):
            self.user_lst[u_name].new_outfit(
                outfit["name"],
                Top(
                    outfit["top"]["name"],
                    outfit["top"]["ID"],
                    outfit["top"]["desc"],
                    outfit["top"]["colour"],
                    outfit["top"]["type"],
                    outfit["top"]["filepath"],
                    outfit["top"]["clean"],
                ),
                Bottom(
                    outfit["bottom"]["name"],
                    outfit["bottom"]["ID"],
                    outfit["bottom"]["desc"],
                    outfit["bottom"]["colour"],
                    outfit["bottom"]["type"],
                    outfit["bottom"]["filepath"],
                    outfit["bottom"]["clean"],
                ),
                Shoes(
                    outfit["shoes"]["name"],
                    outfit["shoes"]["ID"],
                    outfit["shoes"]["desc"],
                    outfit["shoes"]["colour"],
                    outfit["shoes"]["type"],
                    outfit["shoes"]["filepath"],
                    outfit["shoes"]["clean"],
                ),
            )

        print(f"+++ USER LIST: {self.user_lst} +++")

    def return_user(self, u_name):
        return self.user_lst[u_name]


class User:
    def __init__(self, firstName, lastName, userName):
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.closet_lst = {}
        self.outfit_lst = []

    def new_outfit(self, name, top, bottom, shoes):
        self.outfit_lst.append(Outfit(name, top, bottom, shoes))

    def new_closet(self, name, ID):
        self.closet_lst[ID] = Closet(name, ID)

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

    def save_closet(self, closet_new, ID):
        self.closet_lst[ID].set_closet(closet_new)
        print(f"UPDATED CLOSET [{ID}]: {self.closet_lst}")

    def save_outfits(self, outfits_new):
        self.outfit_lst = outfits_new
        print(f"UPDATED OUTFITS: {self.outfit_lst}")

    def export_json(self, filepath):
        print("[!] EXPORTING [!]")
        print(self.closet_lst)
        print(self.outfit_lst)
        print([y.to_dict() for y in self.outfit_lst])

        # Serializing json
        d_export = {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "userName": self.userName,
            "loggedIn": 1,
            "closets": [self.get_closet(x).to_dict() for x in self.closet_lst],
            "outfits": [y.to_dict() for y in self.outfit_lst],
        }
        json_object = json.dumps(d_export, indent=4)

        # Writing to sample.json
        with open(filepath, "w") as outfile:
            outfile.write(json_object)

        # # Writing to sample.json if FILE NAME
        # with open(f"users/{filename}.json", "w") as outfile:
        #     outfile.write(json_object)


class Outfit:
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

    def get_top(self):
        return self.top

    def get_bottom(self):
        return self.bottom

    def get_shoes(self):
        return self.shoes

    def isClean(self):
        print(f"OUTFIT CLEAN CHECK: {self.top}, {self.bottom}, {self.shoes}")
        if (
            (self.top == None or self.top.is_clean())
            and (self.bottom == None or self.bottom.is_clean())
            and (self.shoes == None or self.shoes.is_clean())
        ):
            return True
        else:
            return False

    def to_dict(self):
        return {
            "name": self.name,
            "top": self.top.to_dict(),
            "bottom": self.bottom.to_dict(),
            "shoes": self.shoes.to_dict(),
        }

    def __repr__(self):
        return self.name


# Closet class
# - Closet contains dict of Clothing (Top, Bottom, Shoes)
# - Methods to add clothing
class Closet:
    def __init__(self, name, ID):
        self.clothing_lst = []
        self.name = name
        self.ID = ID

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

    def to_dict(self):
        return {
            "name": self.name,
            "ID": self.ID,
            "clothing": [clothing.to_dict() for clothing in self.clothing_lst],
        }

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
class Clothing:
    def __init__(
        self,
        name,
        ID="0000",
        desc="",
        colour="#ffffff",
        type=0,
        filepath="image.jpg",
        clean=False,
        ckmean=None,
    ):
        self.name = name
        self.ID = ID
        self.desc = desc
        self.colour = colour
        self.clean = clean
        self.type = type
        self.filepath = filepath
        self.ckmean = ckmean  # pyplot figure

    """
    GETTERS
    """

    def get_name(self):
        return self.name

    def get_info(self):
        info_str = f"Name: {self.name}\n\ID: {self.ID}\nDescription: {self.desc}\nType: {self.type}"
        return info_str

    def get_ID(self):
        return self.ID

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

    def to_dict(self):
        return {
            "name": self.name,
            "ID": self.ID,
            "desc": self.desc,
            "colour": self.colour,
            "clean": self.clean,
            "type": self.type,
            "filepath": self.filepath,
            "ckmean": self.ckmean,
        }

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
    def __init__(
        self,
        name,
        ID="0000",
        desc="",
        colour="#ffffff",
        type=0,
        # sleeves=True,
        filepath="image.jpg",
        clean=False,
    ):
        super().__init__(name, ID, desc, colour, type, filepath, clean)
        # self.sleeves = sleeves


class Bottom(Clothing):
    def __init__(
        self,
        name,
        ID="0000",
        desc="",
        colour="#ffffff",
        type=1,
        filepath="image.jpg",
        clean=False,
    ):
        super().__init__(name, ID, desc, colour, type, filepath, clean)


class Shoes(Clothing):
    def __init__(
        self,
        name,
        ID="0000",
        desc="",
        colour="#ffffff",
        type=2,
        filepath="image.jpg",
        clean=False,
    ):
        super().__init__(name, ID, desc, colour, type, filepath, clean)
