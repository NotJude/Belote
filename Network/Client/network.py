
"""
On ne récupère pas d'information pendant la connexion (possibilité de le faire)
CLIENT = SOCKET
changer Network.recieve en dict
au lieu de self.recieving : mettre toutes les fonctions de display qui sont appelées en meme temps dans une seule fonction (???)

"""


import socket
# import pickle
from _thread import start_new_thread

from const_clt import str_to_card, strz_to_cards, card_to_str, SERIALIZED_LENGTH
from display import BeloteWindow



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.26"
        self.port = 5555
        self.addr = (self.server, self.port)
        
        # self.methods = {"a": }
        self.p = int(self.connect())
        self.e = self.p%2
        print("Notre p", self.p)
        self.w = BeloteWindow()

        # 2/10
        self.recieving = True

        # self.recieve()



    def getP(self):
        return self.p
    
    def set_w(self, w):
        self.w = w
    
    def connect(self):
        try:
            print("Je (client) connecté")
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print("====ecxcept 1 (network.py)")


    def send(self, data):
        c = data + '/'
        l = len(c)
        c = c + ' '*(SERIALIZED_LENGTH-l)
        try:
            self.client.send(str.encode(c))
        except socket.error as e:
            print("========== Erreur détectée, network.send")
            print(e)


    def recieve(self): # remplacer par un dict ??
        if self.recieving:
            full = self.client.recv(SERIALIZED_LENGTH).decode()
            l_full = full.split('/')[1:-1]
            m = full[0]
            w = self.w
            
            if m == 'a':
                # print("Entered, is affiching")
                # self.w.affiche()
                w.clear_puntos_tg()
                # self.reciving = True
            elif m == 'b':
                card = str_to_card(l_full[0])
                w.display_single(card)
                # self.reciving = True
            elif m == 'c':
                l = l_full[:-1]
                cards = strz_to_cards(l)
                suit = int(l_full[-1])
                w.display_ma_main(cards, suit)
                # self.reciving = False
            elif m == 'd':
                coul_single = int(l_full[0])
                w.display_but_une(coul_single)
            elif m == 'e':
                w.clear_ma_main()
            elif m == 'f':
                l_coul = []
                for c in l_full:
                    l_coul.append(int(c))
                w.display_but_deux(l_coul)
            elif m == 'g':
                w.clear_at_butts()
            elif m == 'h':
                w.clear_single()
            elif m == 'i':
                a = int(l_full[0])
                w.set_atout(a)
            elif m == 'j':
                e = int(l_full[0])
                all = int(l_full[1])
                w.actualiser_puntos_tg((e+self.e)%2, all)
            elif m == 'k':
                w.clear_mid()
            elif m == 'l':
                a = int(l_full[1])
                card = str_to_card(l_full[0])
                jc = int(l_full[2])
                w.add_to_mid((jc-self.p)%4, card, a)
            elif m == "m":
                cards = strz_to_cards(l_full)
                w.activate_ma_main(cards)
            else:
                raise ValueError

            
            self.recieve()

    def send_jouer_carte(self, c):
        s = "A/" + str(self.p) + "/" + card_to_str(c)
        self.send(s)

    def send_pass(self):
        print("240 CC!!?, is that a yamaha?")

    def send_tra(self, a): # tr_req_at
        s = "B/" + str(a)
        self.send(s)


if __name__ == '__main__':
    n = Network()
    win = n.w
    
    win.configure_on_card_click(lambda c: n.send_jouer_carte(c))
    win.configure_waiter_click(lambda event: n.send_pass())
    win.configure_at_click(lambda a: n.send_tra(a))
    
    start_new_thread(n.recieve, ()) # gros tunnel ici
    # n.recieve()
    n.w.root.mainloop()