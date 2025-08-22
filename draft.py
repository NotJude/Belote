from tkinter import *
import random
from PIL import Image, ImageTk
from const import *

root = Tk()
root.geometry("900x500")

def on_click(event, color):
    print("clicked!", color)

j = Label(root,bg="green")
j.place(x=150, y=50, width=50, height=50)
j.bind("<Button-1>", lambda event: on_click(event, "green"))

l = Label(root,bg="red")
l.place(x=50, y=50, width=50, height=50)
l.bind("<Button-1>", lambda event: on_click(event, "red"))


root.mainloop()