# Cleaning code from main
# removing use of global variables

import os
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

# No need for NavigationToolbar2Tk since colour plot for now; no need for zoom
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# removal of prefix
from ouser import *
from ckmean import *

"""
class ClosetPopUp(tk.Frame):
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.l = tk.Label(self.top, text="Closet Name")
"""


class SwitchFrame(tk.Frame):
    def __init__(self, parent, all_frames, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.all_frames = all_frames

        # switch to closet/outfit
        self.switch_c_b = tk.Button(
            self.parent, text="Closets", command=lambda: self.showFrame("CFRAME")
        )
        # switch to closet/outfit
        self.switch_o_b = tk.Button(
            self.parent, text="Outfits", command=lambda: self.showFrame("OFRAME")
        )

        self.switch_c_b.grid(row=0, column=0, sticky="n")
        self.switch_o_b.grid(row=1, column=0, sticky="n")

    def showFrame(self, page_name):
        current_frame = self.all_frames[page_name]
        current_frame.tkraise()


class OutfitFrame(tk.Frame):
    def __init__(self, parent, user, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.user = user
        self.all_outfits = self.user.get_outfits()

        self.updateNetClothing()

        self.o_lb_frame = tk.Frame(self)
        self.o_option_fr = tk.Frame(self)
        self.o_view_fr = tk.Frame(self)

        # Scrollbar and Listbox
        self.sb = tk.Scrollbar(self.o_lb_frame, orient=tk.VERTICAL)
        # display current list box of closet
        self.outfit_lb = tk.Listbox(
            self.o_lb_frame,
            yscrollcommand=self.sb.set,
            height=10,
            width=30,
            activestyle="dotbox",
            font=("Helvetica", 10),
            fg="black",
        )
        self.sb["command"] = self.outfit_lb.yview

        self.addOutfit_b = tk.Button(
            self.o_option_fr, text="New", command=lambda: self.addOutfitPopup()
        )
        self.editOutfit_b = tk.Button(
            self.o_option_fr, text="Edit", command=lambda: self.editOutfitPopup()
        )
        self.viewOutfit_b = tk.Button(
            self.o_option_fr, text="View", command=lambda: self.viewOutfit()
        )
        self.delOutfit_b = tk.Button(
            self.o_option_fr, text="Delete", command=lambda: self.delOutfitPopup()
        )

        # Make all clean
        self.makeClean_b = tk.Button(
            self.o_option_fr, text="Clean", command=lambda: self.changeOutfitList(1)
        )

        # Make all dirty
        self.makeDirty_b = tk.Button(
            self.o_option_fr, text="Dirty", command=lambda: self.changeOutfitList(0)
        )

        # Find clean outfits
        self.findCleanO_b = tk.Button(
            self.o_option_fr,
            text="Refresh",
            command=lambda: self.updateOutfitList(),
        )

        # LB FRAME
        self.o_lb_frame.grid(row=0, column=0, sticky="NW")

        # lb_frame
        self.outfit_lb.grid(row=0, column=0, sticky="NW")
        self.o_view_fr.grid(row=0, column=1, sticky="NW")

        self.addOutfit_b.grid(row=0, column=0, sticky="NW")
        self.editOutfit_b.grid(row=0, column=1, sticky="NW")
        self.viewOutfit_b.grid(row=0, column=2, sticky="NW")
        self.delOutfit_b.grid(row=0, column=3, sticky="NW")

        self.makeClean_b.grid(row=1, column=0, columnspan=1, sticky="NW")
        self.makeDirty_b.grid(row=1, column=1, columnspan=1, sticky="NW")
        self.findCleanO_b.grid(row=2, column=0, columnspan=1, sticky="NW")

        self.o_option_fr.grid(row=2, column=0, sticky="NW")

        self.updateOutfitList()

    def delOutfitPopup(self):
        self.del_outfit_confirm = tk.messagebox.askyesno(
            title="Confirm Delete",
            message=f"Are you sure you want to delete outfit: {self.outfit_lb.get(self.outfit_lb.curselection()[0])}",
        )

        if self.del_outfit_confirm:
            self.all_outfits.pop(self.outfit_lb.curselection()[0])
            self.outfit_lb.delete(self.outfit_lb.curselection()[0])
            self.updateOutfitList()

    def saveOutfitList(self):
        self.all_outfits[self.outfit_select[0]].set_name(self.edit_n_en.get())
        self.all_outfits[self.outfit_select[0]].set_comb(
            self.checkIfRange(self.outfit_sep_top_lb, self.top_lst),
            self.checkIfRange(self.outfit_sep_bottom_lb, self.bottom_lst),
            self.checkIfRange(self.outfit_sep_shoes_lb, self.shoes_lst),
        )

        print(self.all_outfits[self.outfit_lb.curselection()[0]])

        print(f"[>] SAVED: {self.all_outfits}")

        self.updateOutfitList()

        self.edit_outfit_window.destroy()

    def editOutfitPopup(self):
        self.outfit_select = self.outfit_lb.curselection()

        self.updateNetClothing()
        self.sepNetClothing()

        if self.outfit_lb.curselection():
            self.edit_outfit_window = tk.Toplevel(self)
            # grab_set() to isolate actions to window
            self.edit_outfit_window.grab_set()

            # CREATE name var
            self.edit_n_var = tk.StringVar()
            self.edit_n_var.set("")
            # Edit name frame
            self.edit_n_en = tk.Entry(
                self.edit_outfit_window, textvariable=self.edit_n_var.get(), width=20
            )

            # FOR FINDING COMB. OF OUTFIT
            top_val = 0
            bot_val = 0
            shoe_val = 0

            self.edit_n_var.set(self.all_outfits[self.outfit_select[0]].get_name())
            self.edit_n_en.config(textvariable=self.edit_n_var)
            # when updated, self.edit_n_var.get()

            # EDIT DEBUG
            print("[EDIT]")
            print(f"TOPLIST: {self.top_lst}")
            print(f"BOTLIST: {self.bottom_lst}")
            print(f"SHOELIST: {self.shoes_lst}")

            # # FIND INDEX OF MATCHING IN LISTBOX

            for i, top in enumerate(self.top_lst):
                print("[=] FINDING MATCHING")
                print(
                    f"\t{top.get_ID()} ~ {self.all_outfits[self.outfit_select[0]].top.get_ID()}"
                )
                # AFTER ID FIX, USE THIS
                # if (
                #     top.get_ID()
                #     == self.all_outfits[self.outfit_lb.curselection()[0]].top.get_ID()
                # ):
                if (
                    top.get_name()
                    == self.all_outfits[self.outfit_select[0]].top.get_name()
                ):
                    top_val = i
                else:
                    print(f"{top} != {self.all_outfits[self.outfit_select[0]].top}")

            for i, bot in enumerate(self.bottom_lst):
                if bot == self.all_outfits[self.outfit_select[0]].bottom:
                    bot_val = i

            for i, shoe in enumerate(self.shoes_lst):
                if shoe == self.all_outfits[self.outfit_select[0]].shoes:
                    shoe_val = i

            print(f"COMB: {top_val},{bot_val},{shoe_val}")

            self.addOutfitLB(self.edit_outfit_window, top_val, bot_val, shoe_val)

            # save button
            self.edit_save_b = tk.Button(
                self.edit_outfit_window,
                text="Save",
                command=lambda: self.saveOutfitList(),
            )

            # cancel button
            self.edit_cancel_b = tk.Button(
                self.edit_outfit_window,
                text="Cancel",
                command=lambda: self.edit_outfit_window.destroy(),
            )

            # widget placement
            self.edit_n_en.grid(row=0, column=0, columnspan=2, sticky="NW")

            self.edit_save_b.grid(row=2, column=0, sticky="NW")
            self.edit_cancel_b.grid(row=2, column=1, sticky="NW")
        else:
            tk.messagebox.showwarning(title="Error", message="No outfit selected!")

            print("[!] No outfit selected.")

    def updateNetClothing(self):
        self.net_clothing = []
        tmp_net = []
        for id in self.user.get_all_closet_id():
            tmp_net.append(self.user.get_closet(id).get_all())

        for sublist in tmp_net:
            self.net_clothing.extend(sublist)
        print(self.net_clothing)

    def sepNetClothing(self):
        self.top_lst = []
        self.bottom_lst = []
        self.shoes_lst = []

        for clothing in self.net_clothing:
            if clothing.get_type() == 0:
                self.top_lst.append(clothing)
            elif clothing.get_type() == 1:
                self.bottom_lst.append(clothing)
            elif clothing.get_type() == 2:
                self.shoes_lst.append(clothing)
            else:
                print("[!] WARNING: Clothing of unknown type")

        print(f"NET CLOTHING: {self.net_clothing}")

    def viewOutfit(self):
        self.o_view_name_var = tk.StringVar()
        self.o_view_name = tk.Label(self.o_view_fr, textvariable=self.o_view_name_var)

        if self.outfit_lb.curselection():
            self.o_view_name_var.set(self.outfit_lb.get(self.outfit_lb.curselection()))
            self.o_view_name.config(textvariable=self.o_view_name_var)

            self.o_view_name.grid(row=0, column=0, sticky="NW")

            print("[+]] Outfit selected")
            print(f"\t{self.o_view_name_var}")
        else:
            print("[+] No outfit selected")

    def addOutfitPopup(self):
        self.add_outfit_window = tk.Toplevel(self)
        # grab_set() to isolate actions to window
        self.add_outfit_window.grab_set()

        self.add_o_name = tk.StringVar()
        self.add_o_name.set("Outfit-Name")
        self.add_outfit_name = tk.Entry(
            self.add_outfit_window, textvariable=self.add_o_name, width=20
        )

        self.add_outfit_b = tk.Button(
            self.add_outfit_window, text="Add", command=lambda: self.addOutfit()
        )

        self.back_outfit_b = tk.Button(
            self.add_outfit_window,
            text="Cancel",
            command=lambda: self.add_outfit_window.destroy,
        )

        self.add_outfit_name.grid(row=0, column=0, columnspan=2, sticky="NW")
        self.add_outfit_b.grid(row=2, column=0, sticky="NW")
        self.back_outfit_b.grid(row=2, column=1, sticky="NW")

        self.addOutfitLB(self.add_outfit_window)

    def addOutfitLB(self, window, top_sel=0, bot_sel=0, shoe_sel=0):
        self.updateNetClothing()
        self.sepNetClothing()

        """
        TOP
        """
        # Scrollbar and Listbox
        self.sb_sep_top = tk.Scrollbar(window, orient=tk.VERTICAL)
        # display current list box of closet
        self.outfit_sep_top_lb = tk.Listbox(
            window,
            exportselection=False,
            yscrollcommand=self.sb_sep_top.set,
            height=10,
            width=10,
            activestyle="dotbox",
            font=("Helvetica", 10),
            fg="black",
        )
        self.sb_sep_top["command"] = self.outfit_sep_top_lb.yview

        self.updateSepTop(top_sel)

        """
        BOTTOM
        """
        # Scrollbar and Listbox
        self.sb_sep_bottom = tk.Scrollbar(window, orient=tk.VERTICAL)
        # display current list box of closet
        self.outfit_sep_bottom_lb = tk.Listbox(
            window,
            exportselection=False,
            yscrollcommand=self.sb_sep_bottom.set,
            height=10,
            width=10,
            activestyle="dotbox",
            font=("Helvetica", 10),
            fg="black",
        )
        self.sb_sep_bottom["command"] = self.outfit_sep_bottom_lb.yview

        self.updateSepBottom(bot_sel)
        """
        SHOES
        """
        # Scrollbar and Listbox
        self.sb_sep_shoes = tk.Scrollbar(window, orient=tk.VERTICAL)
        # display current list box of closet
        self.outfit_sep_shoes_lb = tk.Listbox(
            window,
            exportselection=False,
            yscrollcommand=self.sb_sep_shoes.set,
            height=10,
            width=10,
            activestyle="dotbox",
            font=("Helvetica", 10),
            fg="black",
        )
        self.sb_sep_shoes["command"] = self.outfit_sep_shoes_lb.yview

        self.updateSepShoes(shoe_sel)

        self.outfit_sep_top_lb.grid(row=1, column=0, sticky="NW")
        self.outfit_sep_bottom_lb.grid(row=1, column=1, sticky="NW")
        self.outfit_sep_shoes_lb.grid(row=1, column=2, sticky="NW")

    def updateSepTop(self, top_sel=0):
        self.outfit_sep_top_lb.delete(0, tk.END)
        for i, clothing in enumerate(self.top_lst):
            self.outfit_sep_top_lb.insert(i, clothing.get_name())
            self.outfit_sep_top_lb.itemconfig(i, {"bg": "Black"})

        # PRE SELECT
        self.outfit_sep_top_lb.selection_clear(0, tk.END)
        self.outfit_sep_top_lb.selection_set(top_sel)

    def updateSepBottom(self, bot_sel):
        self.outfit_sep_bottom_lb.delete(0, tk.END)
        for i, clothing in enumerate(self.bottom_lst):
            self.outfit_sep_bottom_lb.insert(i, clothing.get_name())
            self.outfit_sep_bottom_lb.itemconfig(i, {"bg": "Blue"})

        # PRE SELECT
        self.outfit_sep_bottom_lb.selection_clear(0, tk.END)
        self.outfit_sep_bottom_lb.selection_set(bot_sel)

    def updateSepShoes(self, shoe_sel):
        self.outfit_sep_shoes_lb.delete(0, tk.END)
        for i, clothing in enumerate(self.shoes_lst):
            self.outfit_sep_shoes_lb.insert(i, clothing.get_name())
            self.outfit_sep_shoes_lb.itemconfig(i, {"bg": "Red"})

        # PRE SELECT
        self.outfit_sep_shoes_lb.selection_clear(0, tk.END)
        self.outfit_sep_shoes_lb.selection_set(shoe_sel)

    def addOutfit(self):
        self.add_o_name_var = self.add_o_name.get()

        self.all_outfits.append(
            Outfit(
                self.add_o_name_var,
                self.checkIfRange(self.outfit_sep_top_lb, self.top_lst),
                self.checkIfRange(self.outfit_sep_bottom_lb, self.bottom_lst),
                self.checkIfRange(self.outfit_sep_shoes_lb, self.shoes_lst),
            )
        )

        print(f"ADDED OUTFIT: {self.add_o_name_var}")
        print(
            f"{self.outfit_sep_top_lb.curselection()}, {self.outfit_sep_bottom_lb.curselection()}, {self.outfit_sep_shoes_lb.curselection()}"
        )
        self.add_outfit_window.destroy()

        self.updateOutfitList()

    def updateOutfitList(self):
        # UPDATES LOCAL LIST
        # UPDATES USER OUTFIT LIST
        self.user.save_outfits(self.all_outfits)

        # UPDATE LISTBOX
        self.outfit_lb.delete(0, tk.END)
        for i, outfit in enumerate(self.all_outfits):
            self.outfit_lb.insert(i, outfit.get_name())
            if outfit.isClean():
                self.outfit_lb.itemconfig(i, {"bg": "#E4E4E4"})
                print(f"{self.outfit_lb.get(i)} is clean")
            else:
                self.outfit_lb.itemconfig(i, {"bg": "red"})
                print(f"{self.outfit_lb.get(i)} is not clean")

    def changeOutfitList(self, state):
        print(f"Turning to {state}")
        # state in case make all dirty/clean
        # UPDATES LOCAL LIST
        # UPDATES USER OUTFIT LIST

        outfit_select = self.outfit_lb.curselection()[0]

        print("[!] Selected")
        # strvar.set(clothing_lb.get(c_selection))

        print(f"[=>]: Name: {self.all_outfits[outfit_select].get_name()}")
        print(f"[=>]: Clean: {self.all_outfits[outfit_select].isClean()}")

        try:
            print(self.all_outfits[outfit_select].get_top().get_name())

            self.all_outfits[outfit_select].get_top().set_clean(state)
        except:
            print("[!] No top in outfit.")

        try:
            print(self.all_outfits[outfit_select].get_bottom().get_name())

            self.all_outfits[outfit_select].get_bottom().set_clean(state)
        except:
            print("[!] No bottom in outfit.")

        try:
            print(self.all_outfits[outfit_select].get_shoes().get_name())

            self.all_outfits[outfit_select].get_shoes().set_clean(state)
        except:
            print("[!] No shoes in outfit.")

        self.updateOutfitList()

    def checkIfRange(self, clothing_lb, lst):
        # returns index of selected item in respective listbox
        try:
            return lst[clothing_lb.curselection()[0]]
        except:
            print("Missing some piece; cannot make outfit")
            self.add_outfit_window.destroy()


class ClosetFrame(tk.Frame):
    def __init__(self, parent, user, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user = user

        # <> NAV BAR
        self.navbar_frame = tk.Frame(self)

        # <> LEFT LIST AND RIGHT PREVIEW
        self.lb_frame = tk.Frame(self)
        self.lb_preview = tk.Frame(self)

        self.lb_button_frame = tk.Frame(self.lb_preview)

        self.navBar()
        self.prevSetup()

        # Scrollbar and Listbox
        self.sb = tk.Scrollbar(self.lb_frame, orient=tk.VERTICAL)
        # display current list box of closet
        self.clothing_lb = tk.Listbox(
            self.lb_frame,
            yscrollcommand=self.sb.set,
            height=10,
            width=30,
            activestyle="dotbox",
            font=("Helvetica", 10),
            fg="white",
        )
        self.sb["command"] = self.clothing_lb.yview

        # <> PREVIEW BUTTON
        self.prev_b = tk.Button(
            self.lb_frame, text="View", command=lambda: self.getPreview()
        )
        self.edit_current_b = tk.Button(
            self.lb_frame, text="Edit", command=lambda: self.editCurrent()
        )
        self.del_current_b = tk.Button(
            self.lb_frame, text="Delete", command=lambda: self.delCurrent()
        )

        # REFRESH
        self.refresh_b = tk.Button(
            self.lb_frame,
            text="Refresh",
            command=lambda: self.updateClothingList(),
        )

        # + EXAMPLE DATA
        # self.all_clothing = self.user.get_closet("0").get_all()
        # self.example_data()
        try:
            self.dropdown.current(0)
            self.dropdown_callback(None)
        except:
            print("Dropdown items empty")

        # init no image filepath
        self.filepath_add = ""

        # + ADD DATA
        self.add_b = tk.Button(
            self.lb_frame, text="Add clothing", command=lambda: self.addNewPopup()
        )

        # <> WIDGET DISPLAY
        self.widgetDisplay()

    def prevSetup(self):
        self.filepath_current = "image.jpg"
        self.image_current = Image.open(self.filepath_current).resize((50, 50))
        self.image_current = ImageTk.PhotoImage(self.image_current)

        # default no image
        # self.prev_image = tk.Label(self.lb_preview, image=self.image_current)
        self.prev_image = tk.Label(self.lb_preview)

        # <> CLOTHING PANEL PREVIEW
        self.prev_label_var = tk.StringVar()
        self.prev_label = tk.Label(
            self.lb_preview,
            textvariable=self.prev_label_var,
            font=("Helvetica", 10),
            justify=tk.LEFT,
        )

    def ckmeanDisplay(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.lb_preview)
        canvas.get_tk_widget().grid(row=3, column=4, sticky="NW")

    def ckmeanGenerate(self, imagepath):
        # Reading image into array
        img = cv2.imread(imagepath)
        # Conversion from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Reshaping into flat array [R G B] of MxN size
        img = img.reshape((img.shape[1] * img.shape[0], 3))

        # Kmeans algorithm
        kmeans = KMeans(n_clusters=4)
        s = kmeans.fit(img)

        # Each point assigned a label (cluster)
        labels = kmeans.labels_
        labels = list(labels)

        # Average position
        centroid = kmeans.cluster_centers_

        # For each centroid size, take proportion
        percent = []
        for i in range(len(centroid)):
            # Number of points within pertaining to a cluster
            j = labels.count(i)
            # Dividing by total number of points
            j = j / (len(labels))
            # Average out of 100
            percent.append(j)

        fig = plt.Figure(figsize=(2, 2), dpi=50)
        ax = fig.add_subplot(111)
        ax.pie(
            percent, colors=np.array(centroid / 255), labels=np.arange(len(centroid))
        )
        self.ckmeanDisplay(fig)

        self.all_clothing[self.prev_select[0]].set_ckmean(fig)

    def getPreview(self):
        # gets selected item in listbox
        self.prev_select = self.clothing_lb.curselection()

        if not self.prev_select:
            tk.messagebox.showwarning(title="Error", message="No clothing selected!")

            print("[!] None selected.")
        else:
            # gets value of selected
            # gets index of selected
            print(f"Index: {self.prev_select[0]}")
            print(self.all_clothing[self.prev_select[0]].print_info())
            # check if no listbox item selected

            if not self.prev_select:
                print("[!] None selected.")
                self.prev_label_var.set("None selected.")
                self.prev_label.config(textvariable=self.prev_label_var)

                # self.prev_label = tk.Label(self.parent, textvariable=self.prev_label_var, font=("Helvetica", 10),justify= tk.LEFT)
                self.prev_image = tk.Label(self.lb_preview, text="No image.")

            else:
                print("[!] Selected")
                # strvar.set(clothing_lb.get(c_selection))
                self.prev_label_var.set(
                    self.all_clothing[self.prev_select[0]].get_info()
                )
                self.prev_label.config(textvariable=self.prev_label_var)
                # self.prev_label = tk.Label(self.parent, textvariable=self.prev_label_var, font=("Helvetica", 10),justify= tk.LEFT)
                # getting and displaying current clothing image

                self.filepath_current = self.all_clothing[
                    self.prev_select[0]
                ].get_image()
                if not self.filepath_current or self.filepath_current.isspace():
                    self.filepath_current = "image.jpg"
                    print("[!] No image for current")

                self.image_current = Image.open(self.filepath_current).resize(
                    (100, 100)
                )
                self.image_current = ImageTk.PhotoImage(self.image_current)

                self.prev_image.configure(image=self.image_current)
                # prevent garbage collection
                self.prev_image.image = self.image_current

                # DISPLAY CKMEAN
                if self.all_clothing[self.prev_select[0]].get_ckmean() == None:
                    print("[!] NO PIE CHART")

                    self.ckmeanGenerate(self.filepath_current)

                    # plt.savefig('clothing_pie', bbox_inches='tight')

                else:
                    self.ckmeanDisplay(
                        self.all_clothing[self.prev_select[0]].get_ckmean()
                    )

    def navBar(self):
        # <> CLOSET DISPLAY
        # Dropdown menu
        self.dropdown_var = tk.StringVar()
        self.dropdown = ttk.Combobox(
            self.navbar_frame,
            textvariable=self.dropdown_var,
            values=self.user.get_all_closet_comb(),
        )

        try:
            self.dropdown.current(0)
        except:
            print("Dropdown items empty")

        self.dropdown.bind("<<ComboboxSelected>>", self.dropdown_callback)

        # Add closet
        self.add_closet_b = tk.Button(
            self.navbar_frame, text="New closet", command=lambda: self.addClosetPopup()
        )
        self.add_closet_b.grid(row=0, column=1, sticky="NW")

        # Delete closet
        self.delete_closet_b = tk.Button(
            self.navbar_frame, text="Delete", command=lambda: self.deleteCloset()
        )
        self.delete_closet_b.grid(row=0, column=5, sticky="NW")

    def addClosetPopup(self):
        self.add_closet_window = tk.Toplevel(self)
        self.add_closet_window.geometry("200x200")
        # grab_set() to isolate actions to window
        self.add_closet_window.grab_set()

        add_c_name = tk.StringVar()
        add_c_name.set("Closet-Name")
        add_c_id = tk.IntVar()
        add_c_id.set("ID")
        self.add_closet_name = tk.Entry(
            self.add_closet_window, textvariable=add_c_name, width=20
        )
        self.add_closet_id = tk.Entry(
            self.add_closet_window, textvariable=add_c_id, width=10
        )
        self.add_closet_b2 = tk.Button(
            self.add_closet_window, text="Add", command=lambda: self.addCloset()
        )

        self.back_closet_b = tk.Button(
            self.add_closet_window,
            text="Cancel",
            command=self.add_closet_window.destroy,
        )

        self.add_closet_name.grid(row=0, column=0, columnspan=2, sticky="NW")
        self.add_closet_id.grid(row=1, column=0, columnspan=2, sticky="NW")
        self.add_closet_b2.grid(row=2, column=0, sticky="NW")
        self.back_closet_b.grid(row=2, column=1, sticky="NW")

    # def addCloset_expand(self):
    #     self.addClosetPopup()
    #     self.add_closet_b.destroy()

    #     add_c_name = tk.StringVar()
    #     add_c_name.set("Closet-Name")
    #     add_c_id = tk.IntVar()
    #     add_c_id.set("ID")
    #     self.add_closet_name = tk.Entry(self.navbar_frame, textvariable=add_c_name, width=20)
    #     self.add_closet_id = tk.Entry(self.navbar_frame, textvariable=add_c_id, width=10)
    #     self.add_closet_b2 = tk.Button(self.navbar_frame, text="Add", command=lambda: self.addCloset())

    #     self.back_closet_b = tk.Button(self.navbar_frame, text="Back", command=lambda: self.addCloset())

    #     self.add_closet_name.grid(row=0,column=1,sticky="NW")
    #     self.add_closet_id.grid(row=0,column=2,sticky="NW")
    #     self.add_closet_b2.grid(row=0,column=3,sticky="NW")
    #     self.back_closet_b.grid(row=0,column=4,sticky="NW")

    def addCloset(self):
        print(
            f"[+] Added new closet: {self.add_closet_name.get()}, {self.add_closet_id.get()}"
        )
        self.user.new_closet(
            self.add_closet_name.get().replace(" ", "-"),
            self.add_closet_id.get().replace(" ", "-"),
        )

        # # DELETE AND REVERT TO INITIAL NAVBAR
        # self.add_closet_name.destroy()
        # self.add_closet_id.destroy()
        # self.add_closet_b2.destroy()
        # self.back_closet_b.destroy()

        # Add closet
        self.add_closet_b = tk.Button(
            self.navbar_frame,
            text="New closet",
            command=lambda: self.addCloset_expand(),
        )
        self.add_closet_b.grid(row=0, column=1, sticky="NW")

        # Update dropdown menu
        self.dropdown["values"] = self.user.get_all_closet_comb()

        print(f"[=] All closet name: {self.user.get_all_closet_name()}")
        print(f"[=] All closet id: {self.user.get_all_closet_id()}")
        # print(f"First closet: {self.user.get_closet('0')}")

        self.add_closet_window.destroy()

    def deleteCloset(self):
        self.mb_confirm = tk.messagebox.askyesno(
            title="Confirm Delete",
            message=f"Are you sure you want to delete closet: {self.dropdown.get()}",
        )

        if self.mb_confirm:
            print(f"[X] Deleted closet: {self.dropdown.get().split()[1]}")
            self.user.delete_closet(self.dropdown.get().split()[1])
            # Update dropdown menu
            self.dropdown["values"] = self.user.get_all_closet_comb()
            # CLEAR
            self.clothing_lb.delete(0, tk.END)
            self.dropdown.set("")

    # DEBUG
    def dropdown_callback(self, *args):
        # UPDATE
        print("[>] Closet selected: ", self.dropdown.get())

        # CLEAR
        self.clothing_lb.delete(0, tk.END)
        self.all_clothing = []

        # Get closet by splitting dropdown value and taking the id part since first element of
        # dropdown.get() since "name + id"
        self.all_clothing = self.user.get_closet(
            self.dropdown.get().split()[1]
        ).get_all()

        self.updateClothingList()

    def save_to_user(self):
        self.user.save_closet(self.all_clothing, self.dropdown.get().split()[1])

    def delCurrent(self):
        confirm = tk.messagebox.askyesno(
            "Confirm Delete",
            message=f"Are you sure you want to clothing {self.clothing_lb.curselection()}?",
        )

        print(f"BEFORE DELETE: {self.all_clothing}")
        if confirm:
            # gets selected item in listbox
            del_select = self.clothing_lb.curselection()
            index = del_select[0]
            self.clothing_lb.delete(index)
            self.all_clothing.pop(index)
        print(f"AFTER DELETE: {self.all_clothing}")

        # Update clothing list box
        self.updateClothingList()
        # Update user clothing list
        self.save_to_user()

    # def saveCurrent(self):
    #     self.all_clothing[self.edit_select[0]].save(name=self.edit_n_var.get(), desc=self.edit_d_txt.get("1.0",tk.END).replace('\n',' '), clean=self.edit_clean_var.get(), type=self.edit_type_var.get())
    #     print(f"[SAVED] {self.all_clothing[self.edit_select[0]].get_info()}")

    #     self.updateClothingList()

    def editCurrent(self):
        # gets selected item in listbox
        self.edit_select = self.clothing_lb.curselection()

        if not self.edit_select:
            tk.messagebox.showwarning(title="Error", message="No clothing selected!")

            print("[!] None selected.")
        else:
            self.edit_window = tk.Toplevel(self.lb_preview)
            # grab_set() to isolate actions to window
            self.edit_window.grab_set()

            # Edit name frame
            self.edit_n_l = tk.Label(self.edit_window, text="Name", justify=tk.LEFT)

            # CREATE name var
            self.edit_n_var = tk.StringVar()
            self.edit_n_var.set("")
            self.edit_n_en = tk.Entry(
                self.edit_window, textvariable=self.edit_n_var.get(), width=40
            )

            # Edit description frame
            self.edit_d_l = tk.Label(
                self.edit_window, text="Description", justify=tk.LEFT
            )

            # Text has no textvariable attribute, thus must use regular strings
            self.edit_d_var = ""
            self.edit_d_txt = tk.Text(self.edit_window, width=30, height=10)
            self.edit_d_txt.insert(tk.INSERT, self.edit_d_var)

            self.edit_image_b = tk.Button(
                self.edit_window, text="Image", command=lambda: self.imageUpload()
            )

            # Clean? checklist w/ Description frame
            self.edit_clean_var = tk.IntVar()
            self.edit_clean_b = tk.Checkbutton(
                self.edit_window, text="Clean", variable=self.edit_clean_var
            )

            # TYPE
            self.edit_type_var = tk.IntVar(self.edit_window, 0)  # default value is top
            self.edit_rb_t = tk.Radiobutton(
                self.edit_window, text="Top", variable=self.edit_type_var, value=0
            )
            self.edit_rb_b = tk.Radiobutton(
                self.edit_window, text="Bottom", variable=self.edit_type_var, value=1
            )
            self.edit_rb_s = tk.Radiobutton(
                self.edit_window, text="Shoes", variable=self.edit_type_var, value=2
            )

            print("[!] Selected")
            # strvar.set(clothing_lb.get(c_selection))

            print(f"[=>]: Name: {self.all_clothing[self.edit_select[0]].get_name()}")
            print(f"[=>]: ID: {self.all_clothing[self.edit_select[0]].get_ID()}")
            print(f"[=>]: Desc: {self.all_clothing[self.edit_select[0]].get_desc()}")
            print(f"[=>]: Type: {self.all_clothing[self.edit_select[0]].get_type()}")

            self.edit_n_var.set(self.all_clothing[self.edit_select[0]].get_name())
            self.edit_n_en.config(textvariable=self.edit_n_var)

            self.edit_d_var = self.all_clothing[self.edit_select[0]].get_desc()
            self.edit_d_txt.insert(tk.INSERT, self.edit_d_var)

            self.edit_clean_var.set(self.all_clothing[self.edit_select[0]].is_clean())

            # default value is top
            self.edit_type_var.set(self.all_clothing[self.edit_select[0]].get_type())

            # getting and displaying current clothing image
            # self.filepath_current = self.all_clothing[self.prev_select[0]].get_image()
            # if not self.filepath_current or self.filepath_current.isspace():
            #    self.filepath_current = "image.jpg"
            #    print("[!] No image for current")

            # SAVE BUTTON -> UPDATE ALL_CLOTHING

            self.edit_save = tk.Button(
                self.edit_window, text="Save", command=lambda: self.saveCurrent()
            )

            self.edit_n_l.grid(row=0, column=0, sticky="NW")
            self.edit_n_en.grid(row=1, column=0, sticky="NW")

            # description
            self.edit_d_l.grid(row=2, column=0, sticky="NW")
            self.edit_d_txt.grid(row=3, column=0, rowspan=1, sticky="NW")

            # clean button
            self.edit_clean_b.grid(row=4, column=0, rowspan=1, sticky="NW")

            # save button
            self.edit_save.grid(row=5, column=0, sticky="NW")

            # TYPE
            self.edit_rb_t.grid(row=0, column=1, sticky="NW")
            self.edit_rb_b.grid(row=1, column=1, sticky="NW")
            self.edit_rb_s.grid(row=2, column=1, sticky="NW")
            # edit image (under clothing type)
            self.edit_image_b.grid(row=3, column=1, rowspan=1, sticky="NW")

    # SAVE CURRENT EDIT
    def saveCurrent(self):
        self.all_clothing[self.edit_select[0]].save(
            name=self.edit_n_var.get(),
            desc=self.edit_d_txt.get("1.0", tk.END).replace("\n", " "),
            clean=self.edit_clean_var.get(),
            type=self.edit_type_var.get(),
        )
        print(f"[SAVED] {self.all_clothing[self.edit_select[0]].get_info()}")

        self.updateClothingList()
        self.edit_window.destroy()

    def updateClothingList(self):
        self.updateFromOutfit()
        self.clothing_lb.delete(0, tk.END)
        for i, clothing in enumerate(self.all_clothing):
            self.clothing_lb.insert(i, clothing.get_name())

            # debug print
            print(
                f"[+ type:{clothing.get_type()}] {clothing.get_name()}\n\t{clothing.get_desc()}\n\t{clothing.is_clean()}"
            )

            if clothing.is_clean():
                self.clothing_lb.itemconfig(i, {"bg": "Green"})
            else:
                self.clothing_lb.itemconfig(i, {"bg": "Red"})

    def addNewPopup(self):
        self.add_window = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        self.add_window.grab_set()

        self.addframe = tk.Frame(self.add_window)
        self.addframe.grid(row=2, column=0, rowspan=6, columnspan=6, sticky="NW")

        """
        INFO ADD FRAME 
        """
        # <> ADD SECTION
        # Left type + image frame
        # Right info frame
        self.type_frame = tk.Frame(self.addframe)
        self.info_frame = tk.Frame(self.addframe)
        self.addType()
        self.addInfo()
        self.type_frame.grid(row=2, column=0, sticky="NW")
        self.info_frame.grid(row=2, column=2, sticky="NW")
        self.add_n_l.grid(row=0, column=0, sticky="NW")
        self.add_n_en.grid(row=1, column=0, sticky="NW")

        # description
        self.add_d_l.grid(row=2, column=0, sticky="NW")
        self.add_d_txt.grid(row=3, column=0, rowspan=1, sticky="NW")
        self.add_clean_b.grid(row=4, column=0, rowspan=1, sticky="NW")

        # button submit
        self.add_sm_b.grid(row=5, column=0, sticky="NW")

        """
        TYPE FRAME 
        """
        self.add_rb_t.grid(row=0, column=0, sticky="NW")
        self.add_rb_b.grid(row=1, column=0, sticky="NW")
        self.add_rb_s.grid(row=2, column=0, sticky="NW")
        # add image (under clothing type)
        self.add_image_b.grid(row=3, column=0, rowspan=1, sticky="NW")

        # self.closet_save_b.grid(row=6,column=0,sticky="NW")

    def addInfo(self):
        # Name frame
        self.add_n_l = tk.Label(self.info_frame, text="Name", justify=tk.LEFT)
        self.add_n_en = tk.Entry(self.info_frame, width=20)

        # Description frame
        self.add_d_l = tk.Label(self.info_frame, text="Description", justify=tk.LEFT)
        self.add_d_txt = tk.Text(self.info_frame, width=15, height=2)

        # Clean? checklist w/ Description frame
        self.clean_var = tk.IntVar()
        self.add_clean_b = tk.Checkbutton(
            self.info_frame, text="Clean?", variable=self.clean_var
        )

        # Button submit
        self.add_sm_b = tk.Button(
            self.info_frame,
            text="ADD",
            padx=10,
            pady=5,
            command=lambda: self.addClothing(),
        )

    def addType(self):
        self.type_var = tk.IntVar(self.parent, 0)  # default value is top
        self.add_rb_t = tk.Radiobutton(
            self.type_frame, text="Top", variable=self.type_var, value=0
        )
        self.add_rb_b = tk.Radiobutton(
            self.type_frame, text="Bottom", variable=self.type_var, value=1
        )
        self.add_rb_s = tk.Radiobutton(
            self.type_frame, text="Shoes", variable=self.type_var, value=2
        )

        self.add_image_b = tk.Button(
            self.type_frame, text="Image", command=lambda: self.imageUpload()
        )

        # SAVE
        # self.closet_save_b = tk.Button(self.type_frame, text='Save closet', command=lambda: self.save_to_user())

    def imageUpload(self):
        # clear current filepath
        self.filepath_add = ""
        # uploading file (image)
        self.filepath_add = filedialog.askopenfilename(
            filetypes=(
                ("jpeg files", "*.jpg"),
                ("png files", "*.png"),
                ("all files", "*.*"),
            )
        )

        # DEBUG
        print(f">> Updated filepath to: {self.filepath_add}")

    # Add clothing to clothing list function
    def addClothing(self):
        # check if valid closet
        try:
            if self.user.get_closet(self.dropdown.get().split()[1]):
                print("[!] Closet exists")
            # get name and description
            self.add_n_var = self.add_n_en.get()
            self.add_d_var = self.add_d_txt.get("1.0", tk.END).replace("\n", " ")
            # new_c_name = str(input())

            # If empty string, use no name
            if not self.add_n_var or self.add_n_var.isspace():
                self.add_n_var = "No name"

            # debug print
            print(
                f"[+ NEW]\n\tNAME: {self.add_n_var}\n\tDESC: {self.add_d_var}\n\tCLEAN: {self.clean_var.get()}\n\tTYPE: {self.type_var.get()}"
            )

            # Adding to clothing list -> type check
            match self.type_var.get():
                case 0:
                    self.all_clothing.append(
                        Top(
                            name=self.add_n_var,
                            ID="0000",
                            desc=self.add_d_var,
                            type=self.type_var.get(),
                            filepath=self.filepath_add,
                            clean=self.clean_var.get(),
                        )
                    )
                case 1:
                    self.all_clothing.append(
                        Bottom(
                            name=self.add_n_var,
                            ID="0000",
                            desc=self.add_d_var,
                            type=self.type_var.get(),
                            filepath=self.filepath_add,
                            clean=self.clean_var.get(),
                        )
                    )
                case 2:
                    self.all_clothing.append(
                        Shoes(
                            name=self.add_n_var,
                            ID="0000",
                            desc=self.add_d_var,
                            type=self.type_var.get(),
                            filepath=self.filepath_add,
                            clean=self.clean_var.get(),
                        )
                    )

            # RESET filepath
            self.filepath_add = ""

            # Check if clean
            if self.clean_var.get():  # [].is_clean():
                self.clothing_lb.insert(tk.END, self.add_n_var)
                self.clothing_lb.itemconfig(tk.END, {"bg": "Green"})
            else:
                self.clothing_lb.insert(tk.END, self.add_n_var)
                self.clothing_lb.itemconfig(tk.END, {"bg": "Red"})

            self.save_to_user()

        except:
            tk.messagebox.showwarning(
                title="Closet error", message="Closet does not exist!"
            )
            print("[!] Closet does not exist")

        self.add_window.destroy()

    def updateFromOutfit(self):
        print("> Updating cleansiness from outfit list")
        for outfit in self.user.get_outfits():
            top = outfit.get_top()
            bot = outfit.get_bottom()
            shoes = outfit.get_shoes()

            print(
                f"\t> Checking {top.get_name()},ID={top.get_ID()} : {top.is_clean()} from outfit"
            )

            for i, clothing in enumerate(self.all_clothing):
                print(
                    f"\t> Comparing to {self.all_clothing[i].get_name()},ID={self.all_clothing[i].get_ID()} : {self.all_clothing[i].is_clean()} from clothing list"
                )

                if clothing.get_type() == 0 and top.get_ID() == clothing.get_ID():
                    print(
                        f"\t\t> {self.all_clothing[i].get_name()} is turning into {top.is_clean()}"
                    )
                    self.all_clothing[i].set_clean(top.is_clean())
                    # make self.all_clothing[] = same cleansiness
                elif clothing.get_type() == 1 and bot.get_ID() == clothing.get_ID():
                    self.all_clothing[i].set_clean(bot.is_clean())
                    # make self.all_clothing[] = same cleansiness
                elif clothing.get_type() == 2 and shoes.get_ID() == clothing.get_ID():
                    self.all_clothing[i].set_clean(shoes.is_clean())
                    # make self.all_clothing[] = same cleansiness

    # WIDGET DISPLAYING
    # GRID FORMAT
    def widgetDisplay(self):
        """
        MAIN FRAME
        """
        self.navbar_frame.grid(row=0, column=0, columnspan=6, sticky="NW")
        self.lb_frame.grid(row=1, column=0, columnspan=3, sticky="NW")

        self.lb_button_frame.grid(row=0, column=0, sticky="NW")
        # addClothing_en.grid(row=1,column=1,rowspan=1,sticky="N")
        # name
        self.lb_preview.grid(row=1, column=3, rowspan=3, sticky="NW")

        """
        LISTBOX FRAME
        """
        # ALL CLOTHING FRAME
        self.dropdown.grid(row=0, column=0, sticky="NW")

        # CHANGED TO FIX BUTTON SPACING
        # lb_frame
        self.clothing_lb.grid(row=0, column=0, columnspan=4, sticky="NW")
        self.sb.grid(row=0, column=2, sticky="NSE")

        # lb_preview
        self.prev_b.grid(row=4, column=2, sticky="NW")

        """
        EDIT
        """
        self.edit_current_b.grid(row=4, column=1, sticky="NW")

        """
        DELETE
        """
        self.del_current_b.grid(row=4, column=3, sticky="NW")

        """
        ADD
        """
        self.add_b.grid(row=4, column=0, sticky="NW")

        """
        PREVIEW
        """
        # clothing preview (right of all clothing list)
        self.prev_label.grid(row=1, column=4, sticky="NW")
        self.prev_image.grid(row=0, column=4, sticky="NW")

        """
        REFRESH
        """
        self.refresh_b.grid(row=5, column=0, sticky="NW")

    def example_data(self):
        shirt_1 = Top("Blue Shirt", "0000", "Blue shirt I bought at Wendy's")
        shirt_2 = Top("Black Shirt", "0000", "Black shirt I bought at McDonald's")
        shirt_3 = Top("Red Shirt", "0000", "Red shirt I bought at Arby's", clean=True)
        pants_1 = Bottom("Normal Jeans", "0000", "Taco", clean=True)

        self.all_clothing.append(shirt_1)
        self.all_clothing.append(shirt_2)
        self.all_clothing.append(shirt_3)
        self.all_clothing.append(pants_1)

        print("ADDING CLOTHING...")

        self.updateClothingList()
        self.save_to_user()

        print("FINISHED ADDING CLOTHING")

    # When user first imports data
    def user_start(self):
        self.dropdown_callback()
        self.updateClothingList()
        self.save_to_user()
        pass


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
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
        switch_button = tk.Button(
            optionsFrame, text="Switch", command=lambda: self.switchAccount()
        )

        new_button = tk.Button(
            optionsFrame, text="New", command=lambda: self.newAccountPopup()
        )

        optionsFrame.grid(row=0, column=0, sticky="NW")
        switch_button.grid(row=0, column=0)
        new_button.grid(row=1, column=0)

    def newAccountPopup(self):
        self.newWindow = tk.Toplevel(self)
        # self.add_window.geometry("200x200")
        # grab_set() to isolate actions to window
        self.newWindow.grab_set()

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

    def createAndClose(self, firstNameVar, lastNameVar, usernameVar, loggedIn=0):
        self.createAccount(firstNameVar, lastNameVar, usernameVar, loggedIn)
        self.newWindow.destroy()

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
            self.topframe, text="Account", command=lambda: self.optionsPopup()
        )
        account_button.grid(row=0, column=0)

        save_button = tk.Button(
            self.topframe,
            text="Save",
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


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
