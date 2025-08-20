import tkinter as tk
from PIL import Image, ImageTk
from joueurs import Joueur
from const import *
from deck import Deck

class BeloteWindow(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        

        self.main_frame = BeloteFrame(self)
        self.main_frame.place(x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT)
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

class BeloteFrame(tk.Frame):
    def __init__(self, parent, deck, **kwargs):
        tk.Frame.__init__(self, parent, bg=BG, **kwargs)

        self.img_cardz = self.get_resized()

    def get_resized(self):
        deck = DECK.copy()
        dick = {}
        for card in deck:
            card_image = Image.open(card)
            resized = card_image.resize(CARD_DIM)
            global tk_card
            tk_card = ImageTk.PhotoImage(resized)
            dick[card] = tk_card
        return dick



class CardDisplayer(tk.Label):
    def __init__(self, parent, card, x=50, y=50, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        self.bg = "red"
        self.bd = -2
        self.card = card
        self.x = x
        self.y = y

        self.place_card(x=self.x, y=self.y, width=CARD_WIDTH, height=CARD_HEIGHT)

    def place_card(self): 
        self.place(x=self.x, y=self.y, width=CARD_WIDTH, height=CARD_HEIGHT)

    def place_with_coord(self, x, y):
        self.x = x
        self.y = y
        self.place_card()

    def render(self):
        image = self.parent.img_cardz[f"cards/{self.card}.png"]
        self.config(image=image)


if __name__ == '__main__':

    root = BeloteWindow()
    leb = CardDisplayer(root.main_frame, "2_of_spades")
    leb.render()

    root.mainloop()