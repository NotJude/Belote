from tkinter import *
import random
from PIL import Image, ImageTk
from const import *

def resize_card(card):
    card_image = Image.open(card)
    resized = card_image.resize(CARD_DIM)
    global tk_card
    tk_card = ImageTk.PhotoImage(resized)
    return tk_card

l = []

root = Tk()
root.title("Belote")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.configure(background=BG)

imagee = resize_card("cards/2_of_clubs.png")
l.append(imagee)
imagen = resize_card("cards/12_of_hearts.png")
l.append(imagen)



main_frame = Frame(root, bg=BG)
main_frame.place(x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT)

n_frame = Label(main_frame, bg=BG, fg="black", text="Nous", bd=-2)
n_frame.place(x=12, y=12, width=CARD_WIDTH, height=CARD_HEIGHT)
n_frame.config(image=l[0])

z_frame = Label(main_frame, bg=BG, fg="black", text="Nous", bd=-2)
z_frame.place(x=312, y=12, width=CARD_WIDTH, height=CARD_HEIGHT)
z_frame.config(image=l[0])

root.mainloop()
