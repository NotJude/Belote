from joueurs import Joueur
from random import randint


class Partie:
    def __init__(self, frame):
        self.jeu = Jeu(frame, 3)

        l_joueurs = []
        j = Joueur(0, bot=False)
        l_joueurs.append(j)
        for i in range(1, 4):
            j = Joueur(i, bot=True)
            l_joueurs.append(j)
        self.l_joueurs = l_joueurs

    def process_ua(self, ua):
        if self.jeu.pli.joueur_courant != ua.sender:
            print("pas à ton tour")
            return # a joué quand c'est pas à son tour
        
        self.l_joueurs[ua.sender].defausser(ua.card)
        self.jeu.carte_jouee(ua.card)

class Jeu:
    def __init__(self, partie, init_dealer):
        self.game = partie
        self.dealer = init_dealer
        # animation pour sélectionner l'atout
        self.atout = 0

        self.pli = Pli(self, 1, (init_dealer + 1) % 4)

    def carte_jouee(self, carte):
        self.pli.ajouter_carte(carte)

        if len(self.pli.table) == 4:
            print("Il faudra changer de pli")

class Pli:
    def __init__(self, jeu, n, premier_joueur):
        self.jeu = jeu
        self.premier_joueur = premier_joueur
        self.joueur_courant = premier_joueur
        self.n = n # numéro du pli : int \in {1, ..., 8}
        self.table = [] # Les cartes jetées sur la table (dans l'ordre chronologique)

    def ajouter_carte(self, carte):
        self.table.append(carte)
        self.joueur_courant = (self.joueur_courant + 1) % 4

    def filtre_main(self, main):
        return main
    