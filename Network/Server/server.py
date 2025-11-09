
"""
enlever N_alpha
"""

import socket
from _thread import start_new_thread
from random import choice

from jeu_n import Partie
from joueurs import Joueur, Ekip
from const_srv import MAX_ROOMS, send, recieve, unprocess, process

N_alpha = 4



class ManageGame:
    def __init__(self, room):
        self.room = room

        self.joueurs = [None]*4
        self.n_real_players = 0
        self.equipes = [Ekip(i) for i in range(2)]
        self.equipes_len = [0, 0]
        
        self.conns = [None]*4

        self.fonctions_jeu = {
            "jouer_cart": lambda n, c: self.pli_courant.jouer_carte(*c),
            "tr_req_at" : lambda n, c: self.jeu_courant.tr_req_at(*n)
        }


    def is_ready(self):
        return self.n_real_players == N_alpha

    
    def add_player(self, conn, pseudo, eq=None, is_nobod=False):
        def bapt(ban):
            return pseudo[:len(ban)].lower()==ban
        # gérer les mauvais pseudos 
        if bapt("caca") or bapt("prout") or bapt("pipi"):
            pseudo = "_baptiste"
        elif bapt("cocobapt"):
            pseudo = "cacabapt38"
        
        elif pseudo=="" or pseudo=="ss":
            pseudo = "---"

        # gérer les choix d'équipe
        if eq==None:
            ep = 1
            if self.equipes_len[0] < 2:
                ep = 0
        elif self.equipes_len[eq]<2:
            ep = eq
        
        # ajout des instances de Ekip, Joueur
        n_joueur = 2*self.equipes_len[ep]+ep
        joueur = Joueur(n_joueur, ep, is_nobod, pseudo)
        self.joueurs[n_joueur] = joueur
        self.n_real_players += 1
        self.equipes_len[ep] += 1
        self.conns[n_joueur] = conn

        # envoie les ordres de démarage au joueur
        self.send_s(n_joueur, [str(n_joueur)])
        self.applyer("launch_gme", n_joueur)
        self.applyer("dsp_room", n_joueur, [self.room])

        # afficher chez nous, et chez les autres joueurs que l'on est arrivé
        for j in range(4):
            joueur = self.joueurs[j]
            if joueur != None:
                self.send_s(n_joueur, ["dsp_pseudo", str(j), joueur.pseudo])
                self.send_s(j, ["dsp_pseudo", str(n_joueur), pseudo])

        return n_joueur


    def start_game(self):
        assert(self.is_ready())
        print("Game being start")

        # On ajoute les bots pour arriver jusqu'à 4
        nnn = 4 - N_alpha
        for i in range(nnn):
            self.add_player(None, "bot"+str(i), is_nobod=True)

        self.equipes[0].init_joueurs(self.joueurs[0], self.joueurs[2])
        self.equipes[1].init_joueurs(self.joueurs[1], self.joueurs[3])

        Partie(self)


    def set_jeu_courant(self, jeu):
        self.jeu_courant = jeu
    
    def set_pli_courant(self, pli):
        self.pli_courant = pli


    def applyer(self, f, j, ns=[], cs=[]):
        l_data = process(f, ns, cs)
        self.send_s(j, l_data)


    def apply_all(self, f, ns=[], cs=[]):
        l_data = process(f, ns, cs)
        for j in range(4):
            self.send_s(j, l_data)

    def recv_n_redirect(self, j):
        m, raw_ns, raw_cs = unprocess(self.recieve_s(j))
        self.fonctions_jeu[m](raw_ns, raw_cs)


    def send_s(self, j, l_data):
        if not self.joueurs[j].is_bot:
            send(self.conns[j], l_data)

    def recieve_s(self, j):
        return recieve(self.conns[j])

    



class Server:
    def __init__(self):
        self.server = "192.168.0.26" # "10.28.26.228"
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.server, self.port))
        except socket.error:
            print("Belote terminée")
            self.socket.close()

        self.games = {}
        self.open_rooms = list(range(1,10**MAX_ROOMS))
        self.n_open_rooms = 10**MAX_ROOMS - 1
        self.player_count = 0
        self.n_active_games = 0

        self.socket.listen()
        self.open()


    def get_random_id(self):
        if self.n_open_rooms > 0:
            c = choice(self.open_rooms)
            self.open_rooms.remove(c)
            self.n_open_rooms -= 1
            return c
        else:
            self.socket.close()
            return None


    def open(self):
        print("Waiting for a connection, server started.")

        while True:
            conn, addr = self.socket.accept()
            print("Connected to:", addr)

            # recevoir un message de la part du joueur qui donne la room
            l_data = recieve(conn)
            need_new_game = bool(int(l_data[0]))
            pseudo = l_data[1]
            
            if need_new_game:
                room = self.get_random_id()
                self.games[room] = ManageGame(room)
                g = self.games[room]
            else:
                try:
                    room = int(l_data[2])
                    g = self.games[room]
                except ValueError:
                    message = "Veuillez entrer un code valide (entier entre 1 et 1"+"9"*(MAX_ROOMS)+")."
                    send(conn, ["dsp_error", message])
                    conn.close()
                    continue
                except KeyError:
                    message = "Veuillez entrer le code d'une partie déjà créee"
                    send(conn, ["dsp_error", message])
                    conn.close()
                    continue

            g.add_player(conn, pseudo)

            if g.is_ready():
                start_new_thread(self.games[room].start_game, ())
                self.n_active_games += 1


    def close_game(self, room_id): # propre au thread d'un game (right?)
        del self.games[room_id]
        self.n_active_games -= 1



if __name__ == '__main__':
    s = Server()