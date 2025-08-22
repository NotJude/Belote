import tkinter as tk
from PIL import Image, ImageTk
from const import *
from user_action import *


class BeloteWindow(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.title("Belote")
        self.configure(background=BG)
        
        self.main_frame = BeloteFrame(self)
        self.main_frame.place(x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT)



class BeloteFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, bg=BG, **kwargs)

        self.img_dict = self.get_resized()
        self.mid_current_imgs = [None]*4
        self.my_current_imgs = [None]*8
        self.n_of_current_imgs = 0
        self.on_card_click = None

    def configure_on_card_click(self, on_card_click):
        self.on_card_click = on_card_click

    def img_my(self, cards):
        self.n_of_current_imgs = len(cards)
        n = self.n_of_current_imgs
        taille = n*CARD_WIDTH + (n-1)*PAD_CARTES_MY
        x_min = WIN_WIDTH/2 - taille/2
        
        for i, card in enumerate(cards):
            x = x_min + i*(CARD_WIDTH + PAD_CARTES_MY)
            lb = CardDisplayer(self, card, x=x, y=MY_Y)
            def helper(j):
                return lambda event : self.on_card_click(j)
            lb.bind("<Button-1>", helper(card))
            self.my_current_imgs[i] = lb

    def add_img_mid(self, card, n): #numéro du joueur
        lb = CardDisplayer(self, card, x=MID_POS[n][0], y=MID_POS[n][1])
        self.mid_current_imgs[n] = lb

    def get_resized(self):
        deck = DECK.copy()
        dick = {}
        for card in deck:
            card_image = Image.open(f"cards/{card}.png")
            resized = card_image.resize(CARD_DIM)
            # global tk_card
            tk_card = ImageTk.PhotoImage(resized)
            dick[card] = tk_card
        return dick
    
    def destroy_all_images(self):
        for e in self.my_current_imgs:
            e.destroy()
        self.my_current_imgs = [None]*8

        for e in self.mid_current_imgs:
            e.destroy()
        self.mid_current_imgs = [None]*4
    
    def render_pli(self, first, table):
        for i in range(len(table)):
            self.add_img_mid(table[i], (first + i) % 4)

    def only_playable(self):
        pass # grise (DESACTIVATE) les cartes non valables



def butt(event):
    print("le btn cliqueé")

class CardDisplayer(tk.Label):
    def __init__(self, parent, card, x=50, y=50, **kwargs):
        tk.Label.__init__(self, parent, bg=BG, **kwargs)
        self.parent = parent
        self.card = card
        self.x = x
        self.y = y

        self.place_card()
        self.render()

    def place_card(self): 
        self.place(x=self.x, y=self.y, width=CARD_WIDTH, height=CARD_HEIGHT)

    def place_with_coord(self, x, y):
        self.x = x
        self.y = y
        self.place_card()

    def render(self):
        image = self.parent.img_dict[f"{self.card}"]
        self.config(image=image)




if __name__ == '__main__':

    root = BeloteWindow()
    leb = CardDisplayer(root.main_frame, "2_of_spades")
    
    leb.place_with_coord(350, 50)


    root.mainloop()