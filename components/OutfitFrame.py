import tkinter as tk
import random
from ouser import *


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
            text="Update from Closet",
            bg="#c4dbff",
            command=lambda: self.updateOutfitAndClothing(),
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
        self.findCleanO_b.grid(row=2, column=0, columnspan=2, sticky="NW")

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
                self.genOutfitID(),
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

    def genOutfitID(self):
        print("> Generating new ID")
        used = []
        for outfit in self.all_outfits:
            used.append(outfit.get_ID())
        print(f"\t> Used IDs: {used}")
        while True:
            new_ID = f"{random.randint(0,9999):04d}"
            if new_ID not in used:
                break

        return new_ID

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

    def updateFromClothing(self):
        print("> Updating cleansiness from clothing list")

        # must update self.all_outfits
        for i, closet_id in enumerate(self.user.get_all_closet_id()):
            print(f"> Checking closet w/ ID: {closet_id}")

            # print(f"> User get all closets: {self.user.get_all_closet()}")
            # print(f"> User get all: {self.user.get_all()}")

            for j, clothing in enumerate(
                self.user.get_closet(closet_id).get_all_clothing()
            ):
                print(
                    f"\t> Checking {clothing.get_name()},ID={clothing.get_ID()} : {clothing.is_clean()}"
                )

                for k, outfit in enumerate(self.all_outfits):
                    top = outfit.get_top()
                    bot = outfit.get_bottom()
                    shoes = outfit.get_shoes()

                    if clothing.get_type() == 0 and top.get_ID() == clothing.get_ID():
                        # outfit clothing -> clothing list clothing
                        print(
                            f"\t\t> {top.get_name()} is turning into {self.user.get_closet(closet_id).get_all_clothing()[j].is_clean()}"
                        )

                        self.all_outfits[k].get_top().set_clean(
                            self.user.get_closet(closet_id)
                            .get_all_clothing()[j]
                            .is_clean()
                        )
                        # make self.all_clothing[] = same cleansiness
                    elif clothing.get_type() == 1 and bot.get_ID() == clothing.get_ID():
                        print(
                            f"\t\t> {bot.get_name()} is turning into {self.user.get_closet(closet_id).get_all_clothing()[j].is_clean()}"
                        )

                        self.all_outfits[k].get_bottom().set_clean(
                            self.user.get_closet(closet_id)
                            .get_all_clothing()[j]
                            .is_clean()
                        )
                        # make self.all_clothing[] = same cleansiness
                    elif (
                        clothing.get_type() == 2 and shoes.get_ID() == clothing.get_ID()
                    ):
                        print(
                            f"\t\t> {shoes.get_name()} is turning into {self.user.get_closet(closet_id).get_all_clothing()[j].is_clean()}"
                        )

                        self.all_outfits[k].get_shoes().set_clean(
                            self.user.get_closet(closet_id)
                            .get_all_clothing()[j]
                            .is_clean()
                        )
                        # make self.all_clothing[] = same cleansiness

    def updateToMatch(self, outfitMatch):
        print("> Updating cleansiness from own outfit list")

        # updating all other outfits to match this one if same clothing
        topMatch = outfitMatch.get_top()
        bottomMatch = outfitMatch.get_bottom()
        shoesMatch = outfitMatch.get_shoes()

        for k, outfit in enumerate(self.all_outfits):
            if self.all_outfits[k].get_ID() != outfitMatch.get_ID():
                print("\t> Not same outfit")

                top = outfit.get_top()
                bot = outfit.get_bottom()
                shoes = outfit.get_shoes()

                if topMatch.get_ID() == top.get_ID():
                    print(
                        f"\t> {top.get_name()} being matched to {topMatch.get_name()}"
                    )
                    print(
                        f"\t\t> {top.get_name()} from another outfit is turning into {topMatch.is_clean()}"
                    )

                    self.all_outfits[k].get_top().set_clean(topMatch.is_clean())
                    # make self.all_clothing[] = same cleansiness
                else:
                    print("\t> Top is not the same")

                if bottomMatch.get_ID() == bot.get_ID():
                    print(
                        f"\t> {bot.get_name()} being matched to {bottomMatch.get_name()}"
                    )
                    print(
                        f"\t\t> {bot.get_name()} from another outfit is turning into {bottomMatch.is_clean()}"
                    )

                    self.all_outfits[k].get_bottom().set_clean(bottomMatch.is_clean())
                    # make self.all_clothing[] = same cleansiness
                else:
                    print("\t> Bottom is not the same")

                if shoesMatch.get_ID() == shoes.get_ID():
                    print(
                        f"\t> {shoes.get_name()} being matched to {shoesMatch.get_name()}"
                    )
                    print(
                        f"\t\t> {shoes.get_name()} from another outfit is turning into {shoesMatch.is_clean()}"
                    )

                    self.all_outfits[k].get_shoes().set_clean(shoesMatch.is_clean())
                    # make self.all_clothing[] = same cleansiness
                else:
                    print("\t> Shoes are not the same")
            else:
                print("\t> Same outfit")

    def updateOutfitAndClothing(self):
        self.updateFromClothing()
        self.updateOutfitList()

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

        self.updateToMatch(self.all_outfits[outfit_select])
        self.updateOutfitList()

    def checkIfRange(self, clothing_lb, lst):
        # returns index of selected item in respective listbox
        try:
            return lst[clothing_lb.curselection()[0]]
        except:
            print("Missing some piece; cannot make outfit")
            self.add_outfit_window.destroy()
