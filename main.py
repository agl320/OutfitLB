import os
import tkinter as tk

from components.SwitchFrame import SwitchFrame
from components.OutfitFrame import OutfitFrame
from components.ClosetFrame import ClosetFrame

# removal of prefix
from ouser import *
from ckmean import *

from tkinter import filedialog

import hashlib

from components.DBSetup import DBSetup


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Database init
        self.DBMaster = DBSetup()

        self.parent = parent

        # # ACCOUNT
        # agl13 = User("GH", "Andrew", "agl13")
        # agl13.new_closet("AC", "0")
        # agl13.new_closet("Buster-Wolf", "1")

        # find all files ending in json, see which is logged in
        self.Manager = Manage()
        self.autoAssignLogin()

        self.initialWidgetDisplay()

    def optionsPopup(self):
        optionsWindow = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        optionsWindow.grab_set()

        optionsFrame = tk.Frame(optionsWindow)
        localO_button = tk.Button(
            optionsFrame, text="Local", command=lambda: self.localOptions()
        )

        onlineO_button = tk.Button(
            optionsFrame, text="Online", command=lambda: self.onlineOptions()
        )

        optionsFrame.grid(row=0, column=0)
        localO_button.grid(row=0, column=0)
        onlineO_button.grid(row=1, column=0)

    # retrieves logged in data and displays it for user to download locally
    def getLoggedInData(self):
        pass

    def signupSubmit(self, username, password):
        # define hashing style and hash password

        # check if username exists
        if (
            self.DBMaster.getCollection().count_documents(
                {"account": username}, limit=1
            )
            != 0
        ):
            print("> Username already exists")
            tk.messagebox.showerror(message="Username already exists")
        else:
            h = hashlib.new("SHA256")
            h.update(password.encode())

            print(f"> Trying to sign up with {username} and {h.hexdigest()}")

            # send to mongodb database
            # data is list of users
            dbExport = {
                "account": username,
                "password": h.hexdigest(),
                "data": [],
            }

            self.DBMaster.insert(dbExport)

    def signup(self):
        onlineOWindow = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        onlineOWindow.grab_set()

        onlineOFrame = tk.Frame(onlineOWindow)
        # username, password, password again

        # Username widgets
        usernameLabel = tk.Label(onlineOFrame, text="Username", justify=tk.LEFT)
        usernameEntry = tk.Entry(onlineOFrame, width=20)

        # Password widgets
        passwordLabel = tk.Label(onlineOFrame, text="Password", justify=tk.LEFT)
        passwordEntry = tk.Entry(onlineOFrame, width=20)

        passwordRLabel = tk.Label(onlineOFrame, text="Retype Password", justify=tk.LEFT)
        passwordREntry = tk.Entry(onlineOFrame, width=20)

        # Submit button
        # goes to function that pushes data to database
        # {accountusername: ... ,
        # accountpassword: ...(hashed) ,
        # accountdata: ...(users)}
        submitButton = tk.Button(
            onlineOFrame,
            text="Submit",
            command=lambda: self.signupSubmit(usernameEntry.get(), passwordEntry.get()),
        )

        # hash password, upload to database paired with username
        usernameLabel.grid(row=0, column=0)
        usernameEntry.grid(row=1, column=0)

        passwordLabel.grid(row=2, column=0)
        passwordEntry.grid(row=3, column=0)
        passwordRLabel.grid(row=4, column=0)
        passwordREntry.grid(row=5, column=0)

        submitButton.grid(row=6, column=0)

        onlineOFrame.grid(row=0, column=0)

    def loginSubmit(self, username, password):
        # define hashing style and hash password
        h = hashlib.new("SHA256")
        h.update(password.encode())

        print(f"> Trying to login with {username} and {h.hexdigest()}")

        exampleAcc = {
            "account": "agl13",
            "password": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
            "data": [],
        }

        # find returns Cursor instance which allows you to iterate over all matching documents
        # find_one finds first instance
        account = self.DBMaster.getCollection().find_one({"account": username})

        if account is None:
            print("Account not found.")
            tk.messagebox.showerror(message="Account not found.")
        else:
            print(account["password"])
            print("\t> Found account, checking password")
            # check password
            if exampleAcc["password"] == h.hexdigest():
                tk.messagebox.showinfo(message="Log in successful!")
                print("\t> Password match, logged in")
                self.loginWindow.destroy()
            else:
                tk.messagebox.showerror(message="Incorrect password")
                print("\t> Incorrect password")

    def login(self):
        # get hashed password from database and check with hashed password from user
        # if matches, loggedin is true
        # two options: upload data button, import data to listbox to import
        # run getLoggedInData()

        self.loginWindow = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        self.loginWindow.grab_set()

        loginFrame = tk.Frame(self.loginWindow)
        # username, password, password again

        # Username widgets
        usernameLabel = tk.Label(loginFrame, text="Username", justify=tk.LEFT)
        usernameEntry = tk.Entry(loginFrame, width=20)

        # Password widgets
        passwordLabel = tk.Label(loginFrame, text="Password", justify=tk.LEFT)
        passwordEntry = tk.Entry(loginFrame, width=20)

        # Submit button
        # goes to function that pushes data to database
        # {accountusername: ... ,
        # accountpassword: ...(hashed) ,
        # accountdata: ...(users)}
        submitButton = tk.Button(
            loginFrame,
            text="Submit",
            command=lambda: self.loginSubmit(usernameEntry.get(), passwordEntry.get()),
        )

        # hash password, upload to database paired with username
        usernameLabel.grid(row=0, column=0)
        usernameEntry.grid(row=1, column=0)

        passwordLabel.grid(row=2, column=0)
        passwordEntry.grid(row=3, column=0)

        submitButton.grid(row=6, column=0)

        loginFrame.grid(row=0, column=0)

    def onlineOptions(self):
        onlineOWindow = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        onlineOWindow.grab_set()

        onlineOFrame = tk.Frame(onlineOWindow)

        # checked if already logged in or not
        # if not, allow for signup/login
        if True:
            signup_button = tk.Button(
                onlineOFrame, text="Sign Up", command=lambda: self.signup()
            )
            login_button = tk.Button(
                onlineOFrame, text="Login", command=lambda: self.login()
            )
            onlineOFrame.grid(row=0, column=0)
            signup_button.grid(row=0, column=0)
            login_button.grid(row=1, column=0)
        else:
            # Run getLoggedInData()
            # display all user configs saved on the database
            # allow user to select which config they want
            pass

    def localOptions(self):
        localOWindow = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        localOWindow.grab_set()

        localOFrame = tk.Frame(localOWindow)

        import_button = tk.Button(
            localOFrame, text="Import", command=lambda: self.switchAccount()
        )
        new_button = tk.Button(
            localOFrame, text="New user", command=lambda: self.newAccountPopup()
        )

        localOFrame.grid(row=0, column=0)
        import_button.grid(row=0, column=0)
        new_button.grid(row=1, column=0)

    def newAccountPopup(self):
        self.newWindow = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        self.newWindow.grab_set()

        # WIDGET RENDERING
        newWindowFrame = tk.Frame(self.newWindow)

        firstNameVar = tk.StringVar()
        firstNameLabel = tk.Label(self.newWindow, text="First Name")
        firstName = tk.Entry(self.newWindow, textvariable=firstNameVar)

        lastNameVar = tk.StringVar()
        lastNameLabel = tk.Label(self.newWindow, text="Last Name")
        lastName = tk.Entry(self.newWindow, textvariable=lastNameVar)

        usernameVar = tk.StringVar()
        usernameLabel = tk.Label(self.newWindow, text="Username")
        username = tk.Entry(self.newWindow, textvariable=usernameVar)

        createButton = tk.Button(
            self.newWindow,
            text="Create",
            command=lambda: self.createAndClose(
                firstNameVar.get(), lastNameVar.get(), usernameVar.get()
            ),
        )
        cancelButton = tk.Button(
            self.newWindow, text="Cancel", command=lambda: self.newWindow.destroy()
        )

        # WIDGET PLACEMENT
        newWindowFrame.grid(row=0, column=0)

        firstNameLabel.grid(row=0, column=0, columnspan=2)
        firstName.grid(row=1, column=0, columnspan=2)

        lastNameLabel.grid(row=2, column=0, columnspan=2)
        lastName.grid(row=3, column=0, columnspan=2)

        usernameLabel.grid(row=4, column=0, columnspan=2)
        username.grid(row=5, column=0, columnspan=2)

        createButton.grid(row=6, column=0)
        cancelButton.grid(row=6, column=1)

    # Create User and Close window
    def createAndClose(self, firstNameVar, lastNameVar, usernameVar, loggedIn=0):
        self.createAccount(firstNameVar, lastNameVar, usernameVar, loggedIn)
        self.newWindow.destroy()

    # Create New User function
    def createAccount(self, firstNameVar, lastNameVar, usernameVar, loggedIn=0):
        d_import = {
            "firstName": firstNameVar,
            "lastName": lastNameVar,
            "userName": usernameVar,
            "loggedIn": loggedIn,
            "closets": [],
            "outfits": [],
        }

        userpath = os.path.join(os.getcwd(), "users")
        finalpath = os.path.join(userpath, f"{usernameVar}.json")

        with open(finalpath, "w") as json_file:
            json.dump(d_import, json_file, indent=4)

    def initialWidgetDisplay(self):
        # TOP FRAME
        self.topframe = tk.Frame(self)

        account_button = tk.Button(
            self.topframe,
            text="Account",
            command=lambda: self.optionsPopup(),
            bg="#c4dbff",
            fg="black",
            font="Helvetica 9 bold",
        )
        account_button.grid(row=0, column=0)

        save_button = tk.Button(
            self.topframe,
            text="Save",
            bg="#c4dbff",
            command=lambda: self.user.export_json(self.filepath),
        )
        save_button.grid(row=0, column=1)

        # left option, right action
        self.optionframe = tk.Frame(self)
        self.actionframe = tk.Frame(self)

        # ACTION FRAME
        self.cframe = ClosetFrame(self.actionframe, self.user)
        self.oframe = OutfitFrame(self.actionframe, self.user)

        self.parent.geometry("650x500")
        self.parent.title("Outfit Manager")

        # frame storing and management
        self.all_frames = {}
        self.all_frames["CFRAME"] = self.cframe
        self.all_frames["OFRAME"] = self.oframe

        # OPTION FRAME
        self.switchframe = SwitchFrame(self.optionframe, self.all_frames)

        # widget placement
        self.grid(padx=5, pady=5)
        self.cframe.grid(row=0, column=0, sticky="news")
        self.oframe.grid(row=0, column=0, sticky="news")

        # MAIN
        self.topframe.grid(row=0, column=0, sticky="news")
        self.optionframe.grid(row=1, column=0, sticky="nw")
        self.actionframe.grid(row=1, column=1, sticky="nw")
        self.actionframe.rowconfigure(0, weight=1)
        self.actionframe.columnconfigure(0, weight=1)

        # SHOW FRAME
        self.showFrame("CFRAME")

    def refreshWidget(self):
        self.cframe.destroy()
        self.oframe.destroy()

        self.cframe = ClosetFrame(self.actionframe, self.user)
        self.oframe = OutfitFrame(self.actionframe, self.user)

        # frame storing and management
        self.all_frames = {}
        self.all_frames["CFRAME"] = self.cframe
        self.all_frames["OFRAME"] = self.oframe

        # OPTION FRAME
        self.switchframe = SwitchFrame(self.optionframe, self.all_frames)

        # widget placement
        self.grid(padx=5, pady=5)
        self.cframe.grid(row=0, column=0, sticky="news")
        self.oframe.grid(row=0, column=0, sticky="news")

        # MAIN
        self.topframe.grid(row=0, column=0, sticky="news")
        self.optionframe.grid(row=1, column=0, sticky="nw")
        self.actionframe.grid(row=1, column=1, sticky="nw")
        self.actionframe.rowconfigure(0, weight=1)
        self.actionframe.columnconfigure(0, weight=1)

        # SHOW FRAME
        self.showFrame("CFRAME")

    def showFrame(self, page_name):
        current_frame = self.all_frames[page_name]
        current_frame.tkraise()

    def autoAssignLogin(self):
        json_files = []

        print("USERS FOLDER:")
        print(os.path.join(os.getcwd(), "users"))
        users_add = os.path.join(os.getcwd(), "users")

        # check if users folder exist
        if os.path.exists(users_add):
            print("> Users folder exists")
        else:
            print("> User folder does not exist")
            print("\t> Creating new users folder")
            os.makedirs(users_add)

        print("> Checking if users exist in folder...")
        for files in os.walk(users_add):
            for file in files[2]:
                if file.endswith(".json"):
                    json_files.append(file)

        # check if no users
        # if none, create one that is logged in
        if len(json_files) == 0:
            print("\t> No users in folder")
            self.createAccount("First name", "Last name", "username", 1)
        else:
            print("\t> Users exist in folder")

        userCheck = False

        print("> Iterating through users...")
        for files in os.walk(users_add):
            for file in files[2]:
                if file.endswith(".json"):
                    self.filepath = os.path.join(users_add, file)
                    with open(self.filepath, "r") as read_file:
                        d_import = json.load(read_file)

                        print(f"\t> Checking user: {d_import['userName']}")
                        print(f"\t\t> Filepath: {self.filepath}")

                        if d_import["loggedIn"] and userCheck == False:
                            print("\t\t> Logged in [/] AND is first user [X]")

                            u_name = d_import["userName"]
                            # self.Manager.import_from_file(f"{os.path.splitext(file)[0]}")
                            self.Manager.import_from_file(self.filepath)
                            self.user = self.Manager.return_user(u_name)

                            print(f"+++ {u_name} IS LOGGED IN +++")
                            userCheck = True
                            # not first user to be logged in

                            self.old_filepath = self.filepath

                        elif d_import["loggedIn"] and userCheck == True:
                            print("\t\t> Logged in [/] AND not first user [X]")
                            u_name = d_import["userName"]
                            d_import["loggedIn"] = 0
                            print(
                                f"\t\t> An account already logged in, {u_name} logging out +++"
                            )
                            with open(self.filepath, "w") as update_file:
                                json.dump(d_import, update_file, indent=4)
                                update_file.close()
                        else:
                            print("\t\t> Not logged in")

        # check if any users logged in
        # at this point, a user must exist as a new would have been created if none existed
        # if existed and none logged in, will just use the data from last variables but change loggedin to 1
        print("> Checking if any user already logged in...")
        if userCheck == False:
            print("\t> No user logged in, logging in first user available")
            with open(self.filepath, "r") as read_file:
                d_import = json.load(read_file)

                print(d_import["userName"])

                d_import["loggedIn"] = 1

                # first user ot be logged in
                if d_import["loggedIn"]:
                    u_name = d_import["userName"]
                    # self.Manager.import_from_file(f"{os.path.splitext(file)[0]}")
                    self.Manager.import_from_file(self.filepath)
                    self.user = self.Manager.return_user(u_name)

                    print(f"+++ {u_name} IS LOGGED IN +++")
                    userCheck = True
            self.old_filepath = self.filepath
        else:
            print("\t> User logged in already")

        print(json_files)
        print(f"> Old filepath (LOGGED IN): {self.old_filepath}")

    def switchAccount(self):
        print("> Switching account initiated!")
        print(f"\t> Old filepath: {self.old_filepath}")
        # GET OLD FILE_NAME
        # self.old_filepath = self.filepath

        # uploading file
        users_add = os.path.join(os.getcwd(), "users")

        try:
            self.filepath = filedialog.askopenfilename(
                initialdir=users_add,
                filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
            )

            # if self.filepath:
            #     filename = os.path.basename(self.filepath)

            # LOG OUT USING OLD FILE_NAME
            print(f"+++ {self.old_filepath} IS LOGGED OUT +++")
            self.Manager.userLogOut(self.old_filepath)

            with open(self.filepath, "r") as read_file:
                d_import = json.load(read_file)

                u_name = d_import["userName"]
                # self.Manager.import_from_file(f"{os.path.splitext(filename)[0]}")
                self.Manager.import_from_file(self.filepath)
                self.user = self.Manager.return_user(u_name)

            # Change LoggedIn status
            d_import["loggedIn"] = 1
            with open(self.filepath, "w") as update_file:
                json.dump(d_import, update_file, indent=4)
                update_file.close()

            print(f"+++ {u_name} IS LOGGED IN +++")

            self.refreshWidget()
        except:
            print("> User import cancelled")


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
