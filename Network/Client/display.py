
import tkinter as tk
from PIL import Image, ImageTk

from const_clt import *



# véritable maitre owner
class BeloteWindow(tk.Tk):
    def __init__(self, applyer, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # autres paramètres
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.title("Belote")
        self.configure(background=BG)

        container = tk.Frame(self, background=BG)
        self.frame_place(container)
        
        self.frames = {} # Frame -> Frame()

        self.applyer = applyer

        self.img_dict_big = self.get_resized(CARD_DIM) 
        self.img_dict_small = self.get_resized(S_CARD_DIM) # dictionnaire des plus petites cartes (pour le pli passé)

        for F in (WelcomeFrame, GameFrame):
            frame = F(container, self)
            self.frames[F] = frame
            self.frame_place(frame)

        self.show_frame(WelcomeFrame)


    def frame_place(self, frame):
        frame.place(x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT)


    def show_frame(self, cont):
        frame = self.frames[cont]
        self.current_frame = frame
        frame.tkraise()


    def get_resized(self, taille):
        deck = NDECK.copy()
        dick = {}
        for card in deck:
            convert = str(card[1])+"_of_"+str(SUITS[card[0]])
            card_image = Image.open(f"cards/{convert}.png")
            resized = card_image.resize(taille)
            tk_card = ImageTk.PhotoImage(resized)
            dick[card] = tk_card
        return dick


    def launch_gme(self):
        self.show_frame(GameFrame)


class BeloteFrame(tk.Frame):
    def __init__(self, parent, master, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg=BG, *args, **kwargs)
        self.master = master

        self.apply = master.applyer


class WelcomeFrame(BeloteFrame):
    def __init__(self, parent, master, *args, **kwargs):
        BeloteFrame.__init__(self, parent, master, *args, **kwargs)

        self.display_elements()


    def display_elements(self):
        # pseudo
        self.t_pseudo = tk.Text(self, height=PSEUDO_HEIGHT, width=PSEUDO_WIDTH)
        self.t_pseudo.place(x=PSEUDO_X, y=PSEUDO_Y, width=PSEUDO_WIDTH, height=PSEUDO_HEIGHT)

        # créer room
        self.b_creer = tk.Button(self, text="Créer une partie")
        self.b_creer.place(x=B_CR_X, y=B_CR_Y, width=B_CR_WIDTH, height=B_CR_HEIGHT)

        # rejoindre une room
        self.b_rej = tk.Button(self, text="Rejoindre")
        self.b_rej.place(x=B_REJ_X, y=B_REJ_Y, width=B_CR_WIDTH, height=B_REJ_HEIGHT)
        self.t_room = tk.Text(self, height=REJ_HEIGHT, width=REJ_WIDTH)
        self.t_room.place(x=REJ_X, y=REJ_Y, width=REJ_WIDTH, height=REJ_HEIGHT)

        # bind
        self.b_creer.bind("<Button-1>", lambda event: self.creer())
        self.b_rej.bind("<Button-1>", lambda event: self.rejoindre())


    def retrieve_pseudo(self):
        return self.t_pseudo.get("1.0",'end-1c')[:10]

    def retrieve_room(self): # return : str
        return self.t_room.get("1.0",'end-1c')

    def creer(self):
        pseudo = self.retrieve_pseudo()
        self.apply("connect")("1", pseudo) # f
        
    def rejoindre(self):
        pseudo = self.retrieve_pseudo()
        room = self.retrieve_room()
        self.apply("connect")("0", pseudo, room) # f




class GameFrame(BeloteFrame):
    def __init__(self, parent, master, *args, **kwargs):
        BeloteFrame.__init__(self, parent, master, *args, **kwargs)

        # constantes de master 
        self.img_dict = master.img_dict_big
        self.img_small = master.img_dict_small


        # variables de table
        self.middle = [None]*4
        self.ma_main = {} # à une carte (tuple) on associe le label
        self.single = None
        self.card_backgrounds = {
            "ma_main" : [],
            "middle"  : [],
        }
        self.at_butts = []

        # display
        # points
        lb_ttl_puntos = tk.Label(self, bg=BG, text="PUNTOS")
        w = 10*6
        lb_ttl_puntos.place(x=WIN_WIDTH-w, y=0, width=w, height=25)

        w_ne = 10*4
        self.lb_tgs = []
        self.lb_ggs = []
        for i, txt in enumerate(["Nous", "Eux"]):
            lb = tk.Label(self, bg=BG, text=txt)
            lb.place(x=WIN_WIDTH+(i-2)*w_ne, y=20, width=w_ne, height=15)
            self.lb_tg = tk.Label(self, bg = BG) # label_this_game
            self.lb_tg.place(x=WIN_WIDTH+(i-2)*w_ne, y=40, width=w_ne, height=15)
            self.lb_tgs.append(self.lb_tg)
            self.lb_gg = tk.Label(self, bg=BG) # label_nous_global_game
            self.lb_gg.place(x=WIN_WIDTH+(i-2)*w_ne, y=60, width=w_ne, height=15)
            self.lb_ggs.append(self.lb_gg)

        self.psd_lbls = [None]*4
        for j in range(4):
            lbl = tk.Label(self, text="")
            x, y = PSEUDO_POS[j][0], PSEUDO_POS[j][1]
            lbl.place(x=x, y=y)
            self.psd_lbls[j] = lbl
        
        self.room_lbl = tk.Label(self)
        self.room_lbl.place(x=ROOM_X, y=ROOM_Y)

        self.at_label = tk.Label(self, bg=BG)
        self.at_label.place(x=0, y=0)



    def draw_pix(self, x, y):
        p = tk.Label(self, bg=BG)
        p.place(x=x, y=y, width=1, height=1)



    def draw6_pix(self, x, y, vx, vy):
        self.draw_pix(x, y)
        self.draw_pix(x+vx, y)
        self.draw_pix(x, y+vy)
        self.draw_pix(x+vx, y+vy)
        self.draw_pix(x+2*vx, y)
        self.draw_pix(x, y+2*vy)
    


    def render_carte(self, card, x, y, bg=BG, big=True):
        lbl = tk.Label(self, bg=bg)
        lbl.place(x=x, y=y, width=CARD_WIDTH, height=CARD_HEIGHT)
        if big: img_dict = self.img_dict
        else: img_dict = self.img_small
        image = img_dict[card]
        lbl.config(image = image)
        return lbl



    def render_with_atout(self, card, x, y, at, where): # where : mid or ma_main
        if card[0] == at:
            b_lbl = tk.Label(self, bg=GOLD)
            xn, yn = x-BORDER, y-BORDER
            w, h = CARD_WIDTH + 2*BORDER, CARD_HEIGHT + 2*BORDER
            b_lbl.place(x=xn, y=yn, width=w, height=h)
            self.card_backgrounds[where].append(b_lbl)
            self.draw6_pix(xn, yn, 1, 1)
            self.draw6_pix(xn+w-1, yn, -1, 1)
            self.draw6_pix(xn, yn+h-1, 1, -1)
            self.draw6_pix(xn+w-1, yn+h-1, -1, -1)
            bg = GOLD
        else: bg = BG
        c_lbl = self.render_carte(card, x, y, bg=bg)
        return c_lbl



    def hide_invalides(self, invalides): # invalides: liste de cartes (tuples)
        for card in self.ma_main.keys():
            if card in invalides:
                lbl = self.ma_main[card]
                lbl.config(state="disabled")


    # méthodes utilisées dire par jeu
    def dsp_pseudo(self, j, psd):
        self.psd_lbls[j].config(text=psd)
    
    def dsp_room(self, room): # room : str
        self.room_lbl.config(text=room)

    def get_but(self, txt):
        lbl = tk.Label(self, text=txt) # bg, etc...
        return lbl

    def set_atout(self, a):
        self.at_label.config(text=TRAD_SUITS[a])
    
    def actualiser_puntos_tg(self, e, puntos):
        self.lb_tgs[e].config(text=f'{puntos}')

    
    def clear_puntos_tg(self):
        for e in range(2):
            self.actualiser_puntos_tg(e, 0)
        
    def display_but_une(self, n_suit): # n_suit \in {0, 1, 2, 3}
        for i, tup in enumerate([("Une", 4), (TRAD_SUITS[n_suit], n_suit)]):
            lbl = self.get_but(tup[0])
            lbl.place(x=SINGLE_X+(2*i-1)*CARD_WIDTH, y=SINGLE_Y)
            def helper(j):
                return lambda event: self.apply("tr_req_at", [j]) # f
            lbl.bind("<Button-1>", helper(tup[1]))
            self.at_butts.append(lbl)


    def display_but_deux(self, n_suits):

        for i, tup in enumerate([("Deux", 4)] + [(TRAD_SUITS[k], k)  for k in n_suits]):
            lbl = self.get_but(tup[0])
            lbl.place(x=SINGLE_X+(i-1.3)*CARD_WIDTH, y=SINGLE_Y-40)
            def helper(j):
                return lambda event: self.apply("tr_req_at", [j]) # f
            lbl.bind("<Button-1>", helper(tup[1]))
            self.at_butts.append(lbl)


    def clear_at_butts(self):
        for but in self.at_butts:
            but.destroy()
        self.at_butts = []

    def display_single(self, card):
        lbl = self.render_carte(card, SINGLE_X, SINGLE_Y)
        self.single = lbl


    def clear_single(self):
        self.single.destroy()
        self.single = None 


    def display_ma_main(self, a, cards):

        n = len(cards)
        taille = n*CARD_WIDTH + (n-1)*PAD_CARTES_MY
        x_min = WIN_WIDTH/2 - taille/2

        for i, card in enumerate(cards):
            x = x_min + i*(CARD_WIDTH + PAD_CARTES_MY)
            if card[0]==a: c_lbl = self.render_with_atout(card, x, MY_Y, a, "ma_main")
            else: c_lbl = self.render_carte(card, x=x, y=MY_Y)
            self.ma_main[card] = c_lbl


    def activate_ma_main(self, valides):
        inv = []
        for card in self.ma_main.keys():
            if card in valides:
                def helper(j):
                    return lambda event: self.apply("jouer_cart", cs=[j])
                lbl = self.ma_main[card]
                lbl.bind("<Button-1>", helper(card))
            else:
                inv.append(card)
        self.hide_invalides(inv)

    def clear_ma_main(self):
        my_local_main = list(self.ma_main.values())
        for clbl in my_local_main:
            clbl.destroy()
        self.ma_main = {}    
        for blbl in self.card_backgrounds["ma_main"]:
            blbl.destroy()
        self.card_backgrounds["ma_main"] = []
        
    def add_to_mid(self, j, at, card):
        x, y = MID_POS[j][0], MID_POS[j][1]
        lbl = self.render_with_atout(card, x, y, at, "middle")
        self.middle[j] = lbl

    def clear_mid(self):
        for lbl in self.middle:
            if lbl!=None:
                lbl.destroy()
        for blbl in self.card_backgrounds["middle"]:
            blbl.destroy()
        self.middle = [None]*4
