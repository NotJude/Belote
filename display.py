
import tkinter as tk
from PIL import Image, ImageTk

from const import *


class BeloteWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.root.title("Belote")
        self.root.configure(background=BG)

        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.place(x=0, y=0, height=WIN_HEIGHT, width=WIN_WIDTH)

        self.img_dict = self.get_resized_big()

        self.middle = [None]*4
        self.ma_main = {} # à une carte (tuple) on associe le label
        self.single = None

        self.bgs_ma_main= [] # les backgrounds des cartes de ma main

        self.on_card_click = None

        self.at_butts = []

        self.at_label = tk.Label(self.main_frame, bg=BG)
        self.at_label.place(x=0, y=0)

        ACTION_FONT = tkinter.font.Font(family="Arial", size=25)
        self.action_label = tk.Label(self.main_frame, bg=BG, fg="red", font=ACTION_FONT)
        self.action_label.place(x=WIN_WIDTH-105, y=0, width=105, height=25)


    def configure_on_card_click(self, on_card_click):
        self.on_card_click = on_card_click

    def configure_waiter_click(self, waiter_click_function):
        self.waiter_click = waiter_click_function

    def configure_at_click(self, at_click_function):
        self.at_click = at_click_function

    def taille_main(self):
        return len(self.ma_main)
    

    def get_resized_big(self): # pas une vraie fonction
        deck = NDECK.copy()
        dick = {}
        for card in deck:
            convert = str(card[1])+"_of_"+str(SUITS[card[0]])
            card_image = Image.open(f"cards/{convert}.png")
            resized = card_image.resize(CARD_DIM)
            tk_card = ImageTk.PhotoImage(resized)
            dick[card] = tk_card
        return dick


    def render_carte(self, card, x, y, bg=BG):
        lbl = tk.Label(self.main_frame, bg=bg)
        lbl.place(x=x, y=y, width=CARD_WIDTH, height=CARD_HEIGHT)
        image = self.img_dict[card]
        lbl.config(image = image)
        return lbl
    

    def render_card_for_ma_main(self, card, x, y, bg):
        b_lbl = tk.Label(self.main_frame, bg=bg)
        b_lbl.place(x=x-BORDER, y=y-BORDER, width=CARD_WIDTH+2*BORDER, height=CARD_HEIGHT+2*BORDER)
        self.bgs_ma_main.append(b_lbl)
        c_lbl = self.render_carte(card, x, y, bg=bg)
        return c_lbl


    def display_ma_main(self, cards, a):

        n = len(cards)
        taille = n*CARD_WIDTH + (n-1)*PAD_CARTES_MY
        x_min = WIN_WIDTH/2 - taille/2

        for i, card in enumerate(cards):
            x = x_min + i*(CARD_WIDTH + PAD_CARTES_MY)
            if card[0]==a: c_lbl = self.render_card_for_ma_main(card, x, MY_Y, GOLD)
            else: c_lbl = self.render_carte(card, x=x, y=MY_Y)
            self.ma_main[card] = c_lbl


    def hide_invalides(self, invalides): # invalides: liste de cartes (tuples)
        for card in self.ma_main.keys():
            if card in invalides:
                lbl = self.ma_main[card]
                lbl.config(state="disabled")


    def activate_ma_main(self, valides):
        inv = []
        for card in self.ma_main.keys():
            if card in valides:
                def helper(j):
                    return lambda event: self.on_card_click(j)
                lbl = self.ma_main[card]
                lbl.bind("<Button-1>", helper(card))
            else:
                inv.append(card)
        self.hide_invalides(inv)


    def clear_ma_main(self):
        my_local_main = list(self.ma_main.values())
        for clbl in my_local_main:
            clbl.destroy()
        for blbl in self.bgs_ma_main:
            blbl.destroy()
        self.ma_main = {}


    def set_atout(self, a):
        self.at_label.config(text=SUITS[a])

        

    def waiter(self):
        self.action_label.config(text="CLICK!")
        self.main_frame.bind("<Button-1>", self.waiter_click)

    
    def done_waiting(self):
        self.action_label.config(text="")
        self.main_frame.unbind("<Button-1>")


    
    def add_to_mid(self, j, card):
        lbl = self.render_carte(card, MID_POS[j][0], MID_POS[j][1])
        self.middle[j] = lbl


    def clear_mid(self):
        for lbl in self.middle:
            if lbl!=None:
                lbl.destroy()
        self.middle = [None]*4

    
    def display_single(self, card):
        lbl = self.render_carte(card, SINGLE_X, SINGLE_Y)
        self.single = lbl


    def clear_single(self):
        self.single.destroy()
        self.single = None 

    
    def get_but(self, txt):
        lbl = tk.Label(self.main_frame, text=txt) # bg, etc...
        return lbl

    def display_but_une(self, n_suit): # n_suit \in {0, 1, 2, 3}
        for i, tup in enumerate([("Une", 4), (SUITS[n_suit], n_suit)]):
            lbl = self.get_but(tup[0])
            lbl.place(x=SINGLE_X+(2*i-1)*CARD_WIDTH, y=SINGLE_Y)
            def helper(j):
                return lambda event: self.at_click(j)
            lbl.bind("<Button-1>", helper(tup[1]))
            self.at_butts.append(lbl)


    def display_but_deux(self, n_suits):

        for i, tup in enumerate([("Deux", 4)] + [(SUITS[k], k)  for k in n_suits]):
            lbl = self.get_but(tup[0])
            lbl.place(x=SINGLE_X+(i-1.3)*CARD_WIDTH, y=SINGLE_Y-40)
            def helper(j):
                return lambda event: self.at_click(j)
            lbl.bind("<Button-1>", helper(tup[1]))
            self.at_butts.append(lbl)


    def clear_at_butts(self):
        for but in self.at_butts:
            but.destroy()
        self.at_butts = []
