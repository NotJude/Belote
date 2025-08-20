from tkinter import *
from PIL import Image, ImageTk
from const import *
from deck import Deck


root = Tk()
root.title("Belote")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.configure(background=BG)

main_frame = Frame(root, bg=BG)
main_frame.place(x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT)

n_frame = Label(main_frame, bg=BG, fg="black", text="Nous", bd=-2)
n_frame.place(x=MID_0_X, y=MID_0_Y, width=CARD_WIDTH, height=CARD_HEIGHT)


n_label = Label(n_frame, bg=BG, text='')
n_label.pack()

labs = []
u_labs = []
l_imgs = ["" for _ in range(8)]
for i in range(8):
    lab = Label(main_frame, bg="white", fg="black", text="Nous", bd=-2)
    u_lab = Label(lab, bg=BG, text='')
    labs.append(lab)
    u_lab.pack()
    u_labs.append(u_lab)
    



deck = Deck()

def resize_card(card):
    card_image = Image.open(card)
    resized = card_image.resize(CARD_DIM)
    global tk_card
    tk_card = ImageTk.PhotoImage(resized)
    return tk_card

def butt():

    cdn = '2_of_clubs'
    global imagen
    imagen = resize_card(f'cards/{cdn}.png')
    
    n_frame.config(image=imagen)

def display_cartes_m(mes_cartes):
    n = len(mes_cartes)
    taille = n*CARD_WIDTH + (n-1)*PAD_CARTES_M
    x_min = WIN_WIDTH/2 - taille/2
    y = round(2/3*WIN_HEIGHT)
    for i, cdn in enumerate(mes_cartes):
        x = x_min + i*(CARD_WIDTH+PAD_CARTES_M)
        lab = labs[i]
        lab.place(x=x, y=y, width=CARD_WIDTH, height=CARD_HEIGHT)
        u_lab = u_labs[i]

        imagen = resize_card(f'cards/{cdn}.png')
        l_imgs[i] = imagen
        u_lab.config(image=imagen)
        

# lambda: display_cartes_m(['2_of_clubs', '3_of_clubs', '12_of_hearts'])


shuffle_button = Button(root, text=" button", command=butt)
shuffle_button.pack()





root.mainloop()

