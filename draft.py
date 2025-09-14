import tkinter as tk
from const import *

root = tk.Tk()

root.geometry("800x600")
f= tk.Frame(root, bg=BG)
f.place(x=0, y=0, width=800, height=600)

l = tk.Label(f, bg="white", highlightthickness=25)
l.place(x=50, y=50, width=50, height=50)
l.config(highlightbackground="black", highlightcolor="black")

root.mainloop()