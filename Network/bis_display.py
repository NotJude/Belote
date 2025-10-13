

import tkinter as tk

from const import *

class BeloteWindow:
    def __init__(self, j):
        self.j = j
        self.root = tk.Tk()
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.root.title("Belote")
        self.root.configure(background=BG)
        
        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.place(x=0, y=0, height=WIN_HEIGHT, width=WIN_WIDTH)




    def affiche(self):
        self.lab = tk.Label(self.main_frame, text="ABC")
        self.lab.place(x=50, y=50, width=30, height=50)