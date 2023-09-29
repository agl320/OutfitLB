import tkinter as tk


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
        # init as blue
        self.switch_c_b.config(bg="#257AFD", fg="white")
        self.switch_o_b.config(bg="#c4dbff", fg="black")

        self.switch_c_b.grid(row=0, column=0, sticky="n")
        self.switch_o_b.grid(row=1, column=0, sticky="n")

    def showFrame(self, page_name):
        if page_name == "OFRAME":
            self.switch_o_b.config(bg="#257AFD", fg="white")
            self.switch_c_b.config(bg="#c4dbff", fg="black")
        elif page_name == "CFRAME":
            self.switch_c_b.config(bg="#257AFD", fg="white")
            self.switch_o_b.config(bg="#c4dbff", fg="black")
        else:
            print("[>] Frame does not exist")

        current_frame = self.all_frames[page_name]
        current_frame.tkraise()
