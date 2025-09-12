
import tkinter as tk
from PIL import Image, ImageTk

from const import *

class BeloteWindow:
    """
    Je propose de mettre ce qui était BeloteWindow, BeloteFrame et CardDisplayer dans une seul classe BeloteWindow
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.root.title("Belote")
        self.root.configure(background=BG)

        self.main_frame = tk.Frame(self.root, bg=BG) # à comploter
        self.main_frame.place(x=0, y=0, height=WIN_HEIGHT, width=WIN_WIDTH)

        self.img_dict = self.get_resized_big()

        # labelzzz
        self.middle = [None]*4 # une liste suffit ici (pour l'instant)
        self.my_main = {} # à une carte (tuple) on associe le label
        self.single = None

        self.on_card_click = None
        # self.ready_for_next_pli_click = None

        #Newww (10/09)
        self.at_butts = []

        self.at_label = tk.Label(self.main_frame, bg=BG)
        self.at_label.place(x=0, y=0)






    def configure_on_card_click(self, on_card_click):
        self.on_card_click = on_card_click

    def configure_waiter_click(self, waiter_click_function):
        self.waiter_click = waiter_click_function

    def configure_at_click(self, at_click_function):
        self.at_click = at_click_function





    def taille_main(self):
        return len(self.my_main)
    


    # juju l'tueur
    def get_resized_big(self): # pas vraiment une fonction : on peut la laisser dans le __init__
        deck = NDECK.copy()
        dick = {}
        for card in deck:
            convert = str(card[1])+"_of_"+str(SUITS[card[0]])
            card_image = Image.open(f"cards/{convert}.png")
            resized = card_image.resize(CARD_DIM)
            # global tk_card
            tk_card = ImageTk.PhotoImage(resized)
            dick[card] = tk_card
        return dick
    
    # ATOMIC
    def render_carte(self, card, x, y): 
        lbl = tk.Label(self.main_frame) #bg = BG
        lbl.place(x=x, y=y, width=CARD_WIDTH, height=CARD_HEIGHT)
        image = self.img_dict[card]
        lbl.config(image = image)
        return lbl



    def display_my_hand(self, cards):

        n = len(cards)
        taille = n*CARD_WIDTH + (n-1)*PAD_CARTES_MY
        x_min = WIN_WIDTH/2 - taille/2

        for i, card in enumerate(cards):
            x = x_min + i*(CARD_WIDTH + PAD_CARTES_MY)
            c_lbl = self.render_carte(card, x=x, y=MY_Y)
            self.my_main[card] = c_lbl


    def hide_invalides(self, invalides): # invalides: liste de cartes (tuples)
        for card in self.my_main.keys():
            if card in invalides:
                lbl = self.my_main[card]
                lbl.config(state="disabled")


    def activate_my_hand(self, valides):
        inv = []
        for card in self.my_main.keys():
            if card in valides:
                def helper(j):
                    return lambda event: self.on_card_click(j)
                lbl = self.my_main[card]
                lbl.bind("<Button-1>", helper(card))
            else:
                inv.append(card)
        self.hide_invalides(inv)

    def clear_my_main(self):
        # print("Begin to destroy", self.my_main.keys())
        my_local_main = list(self.my_main.values())
        # print()
        for clbl in my_local_main:
            clbl.destroy()
            # print("abzzzzzzzzzzzzz")
        # print("End of destroy", self.my_main.values())
        self.my_main = {}

    def set_atout(self, a):
        self.at_label.config(text=SUITS[a])

        

    def waiter(self):
        self.main_frame.bind("<Button-1>", self.waiter_click)

    
    def done_waiting(self):
        self.main_frame.unbind("<Button-1>")


    
    def add_to_mid(self, j, card):
        lbl = self.render_carte(card, MID_POS[j][0], MID_POS[j][1])
        self.middle[j] = lbl


    def clear_mid(self):
        for lbl in self.middle:
            try:
                lbl.destroy()
            except:
                pass
                # print("================bipboup pouquoi clear_mid alors que toutes les cartes n'ont pas été jouées ? =")
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

        lbl = self.get_but("Une")
        lbl.place(x=SINGLE_X-CARD_WIDTH, y=SINGLE_Y)
        lbl.bind("<Button-1>", lambda event: self.at_click(4))
        self.at_butts.append(lbl)

        lal = self.get_but(SUITS[n_suit])
        lal.place(x=SINGLE_X+CARD_WIDTH, y=SINGLE_Y)
        lal.bind("<Button-1>", lambda event: self.at_click(n_suit))
        self.at_butts.append(lal)


    def display_but_deux(self, n_suits):

        lbl = self.get_but("Deux")
        lbl.place(x=SINGLE_X-2*CARD_WIDTH, y=SINGLE_Y)
        lbl.bind("<Button-1>", lambda event: self.at_click(4))
        self.at_butts.append(lbl)

        q = n_suits[0]
        lbl = self.get_but(SUITS[q])
        lbl.place(x=SINGLE_X-CARD_WIDTH, y=SINGLE_Y)
        lbl.bind("<Button-1>", lambda event: self.at_click(q))
        self.at_butts.append(lbl)

        r = n_suits[1]
        lbl = self.get_but(SUITS[r])
        lbl.place(x=SINGLE_X+CARD_WIDTH, y=SINGLE_Y)
        lbl.bind("<Button-1>", lambda event: self.at_click(r))
        self.at_butts.append(lbl)

        s = n_suits[2]
        lbl = self.get_but(SUITS[s])
        lbl.place(x=SINGLE_X+2*CARD_WIDTH, y=SINGLE_Y)
        lbl.bind("<Button-1>", lambda event: self.at_click(s))
        self.at_butts.append(lbl)


    def clear_at_butts(self):
        for but in self.at_butts:
            but.destroy()

        self.at_butts = []
        
        
    # FOR ACTIONS














    
