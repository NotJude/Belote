from tkinter import *
import random
from PIL import Image, ImageTk
from const import *


class Deck:
    def __init__(self):
        suits = ["clubs", "diamonds", "spades", "hearts"]
        values = [i for i in range(2,15)]

        self.DECK = []
        for suit in suits:
            for value in values:
                self.DECK.append(f'{value}_of_{suit}')

        self.current_deck = []
        self.free_refill()

    def shuffle(self):
        random.shuffle(self.current_deck)

    def pick(self):
        card = random.choice(self.current_deck)
        self.current_deck.remove(card)
        return card
    
    def pick_and_put_back(self):
        return random.choice(self.current_deck) 

    def empty_deck(self):
        return len(self.current_deck)==0
    
    def free_refill(self):
        self.current_deck = self.DECK.copy()

root = Tk()
root.title("Belote")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.configure(background=BG)

main_frame = Frame(root, bg=BG)
main_frame.place(x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT)

n_frame = Label(main_frame, bg=BG, fg="black", text="Nous", bd=-2)


n_label = Label(n_frame, bg=BG, text='')
n_label.pack()

# lab1 = Label(n_frame, text='')
# lab2 = Label(n_frame, text='')
# lab3 = Label(n_frame, text='')
# lab4 = Label(n_frame, text='')
# lab5 = Label(n_frame, text='')
# lab6 = Label(n_frame, text='')
# lab7 = Label(n_frame, text='')
# lab8 = Label(n_frame, text='')
# labs = [lab1, lab2, lab3, lab4, lab5, lab6, lab7, lab8]
# for lab in labs:
#     lab.pack()
labs = []
u_labs = []
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
    n_frame.place(x=MID_0_W, y=MID_0_H, width=CARD_WIDTH, height=CARD_HEIGHT)
    n_label.config(image=imagen)

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

    global imagen
    imagen = resize_card(f'cards/{cdn}.png')
    u_lab.config(image=imagen)

# lambda: display_cartes_m(['2_of_clubs', '3_of_clubs', '12_of_hearts'])


shuffle_button = Button(root, text=" button", command=lambda: display_cartes_m(['2_of_clubs', '3_of_clubs', '12_of_hearts']))
shuffle_button.pack()





root.mainloop()

