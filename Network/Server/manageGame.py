

"""
à mettre dans server.py (?)
lignes 60-61 à décomenter
enlever N_alpha
"""


from jeu_n import Partie
from joueurs import Joueur, Ekip
from const_srv import SERIALIZED_LENGTH, str_to_card

N_alpha = 4

class ManageGame:
    def __init__(self):
        self.joueurs = [None]*4
        self.n_players = 0
        self.equipes = [Ekip(i) for i in range(2)]
        self.equipes_len = [0, 0]
        
        self.started = False
        self.conns = None
        self.sender_func = None

        # self.partie = None

    def set_sender_func(self, f):
        self.sender_func = f

    def set_conns(self, conns):
        self.conns = conns

    def is_ready(self):
        return self.n_players == N_alpha
    
    def add_player(self, eq=None, is_nobod=False): 
        # assert(not self.is_ready())
        
        if eq==None:
            ep = 1
            if self.equipes_len[0] < 2:
                ep = 0
        
        elif self.equipes_len[eq]<2:
            ep = eq
        

        n_joueur = 2*self.equipes_len[ep]+ep
        joueur = Joueur(n_joueur, ep, is_nobod)
        self.joueurs[n_joueur] = joueur
        self.n_players += 1
        self.equipes_len[ep] += 1

        return n_joueur


    def start_game(self):
        assert(self.is_ready())
        print("Game being start")

        nnn = 4 - N_alpha
        for _ in range(nnn):
            self.add_player(is_nobod = True)

        self.started = True

        self.equipes[0].init_joueurs(self.joueurs[0], self.joueurs[2])
        self.equipes[1].init_joueurs(self.joueurs[1], self.joueurs[3])

        Partie(self)
        
        # print("self.partie1", self.partie)

    def set_jeu_courant(self, jeu):
        self.jeu_courant = jeu
    
    def set_pli_courant(self, pli):
        self.pli_courant = pli


    def send(self, c, n):
        assert(self.started)
        if not self.joueurs[n].is_bot:
            # print("sending")
            c = c + '/'
            l = len(c)
            c = c + ' '*(SERIALIZED_LENGTH-l)
            self.sender_func(c, n)


    def recieve(self, j): # des "j" en trop
        data = self.conns[j].recv(SERIALIZED_LENGTH).decode()
        # print("data", data)
        l = data.split('/')[1:-1]
        m = data[0]
        
        if m == 'A':
            sender_j = int(l[0]) # iciiii
            assert(sender_j == j)
            card = str_to_card(l[1])
            self.pli_courant.jouer_carte(card)

        elif m == 'B':
            a = int(l[0])
            self.jeu_courant.tr_req_at(a)
