
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

        self.middle = None 
        self.clear_middle()

        self.my_main = None
        self.clear_my_main()

        self.on_card_click = None
        self.ready_for_next_pli_click = None

    def configure_on_card_click(self, on_card_click):
        self.on_card_click = on_card_click

    def configure_ready_pli_click(self, ready_on_click):
        self.ready_for_next_pli_click = ready_on_click

    def clear_middle(self):
        self.middle = [None]*4

    def clear_my_main(self):
        self.my_main = []

    def taille_main(self):
        return len(self.my_main)
    
    def render_carte(self, card, x, y): # !!!!!!!! à l'ordre entre place et config
        # renvoie le label lui meme, ne pas oublier d'ajouter la valeur de retour (Label lbl) à la liste correspondante (self.my_main ou self.middle)
        lbl = tk.Label(self.main_frame) #bg = BG
        lbl.place(x=x, y=y, width=CARD_WIDTH, height=CARD_HEIGHT)
        image = self.img_dict[card]
        lbl.config(image = image)
        return lbl

    # juju l'tueur
    def get_resized_big(self):
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
    
    def display_my_hand(self, cards, valides=None): 
        """
        fonction à appeler après que l'on a joué
        - effacer les cartes de my
        - les remettre avec un bind désactivé pour toute carte.
        - afficher la carte middle: T.
        """
        if self.my_main != None:
            for c_lbl in self.my_main:
                c_lbl.destroy()
            self.clear_my_main()

        n = len(cards)
        taille = n*CARD_WIDTH + (n-1)*PAD_CARTES_MY
        x_min = WIN_WIDTH/2 - taille/2

        for i, card in enumerate(cards):
            x = x_min + i*(CARD_WIDTH + PAD_CARTES_MY)
            c_lbl = self.render_carte(card, x=x, y=MY_Y)
            def helper(j):
                return lambda event: self.on_card_click(j)
            c_lbl.bind("<Button-1>", helper(card))
            if valides == None:
                c_lbl.config(state="disabled")
            elif card not in valides:
                c_lbl.config(state="disabled")
            self.my_main.append(c_lbl)

    def abt_to_play(self, cards, valides): # plus tard : la suppr
        """
        peut etre pour bind seulement les cartes valides
        - activer les cartes disponibles
        """
        self.display_my_hand(cards, valides)

    def display_new_to_middle(self, j, card): # dès que quelqu'un joue
        """
        appeler dès que quelqu'un à joué
        - afficher la carte du middle
        j : entier entre 0 et 3
        card : la carte qui est jouée
        """
        lbl = self.render_carte(card, MID_POS[j][0], MID_POS[j][1])
        # assert(self.middle[j]==None)
        # print(self.middle[j])
        self.middle[j] = lbl


    def display_end_of_pli(self):
        """
        à appeler à la fin du pli : 
        - effacer le middle
        - self.middle = [None]*4

        """
        self.main_frame.bind("<Button-1>", self.ready_for_next_pli_click)

    def display_beg_of_pli(self):
        self.main_frame.unbind("<Button-1>")
        for lbl in self.middle:
            lbl.destroy()
        self.clear_middle()



    def display_end_of_jeu(self):
        """
        à appeler à la fin du jeu
        - 
        """
        print("la fin du jeu")