from joueurs import Joueur
from random import randint


class Partie:
    def __init__(self):
        pass


class Jeu:
    def __init__(self, frame, init_dealer):
        
        self.dealer = init_dealer
        # animation pour sélectionner l'atout
        self.atout = 0

        # à mettre dans "Partie"
        l_joueurs = []
        j = Joueur(0, bot=False)
        l_joueurs.append(j)
        for i in range(1, 4):
            j = Joueur(i, bot=True)
            l_joueurs.append(j)
        self.l_joureurs = l_joueurs

        self.pli_courant = Pli(self, 1, (init_dealer + 1) % 4)
    
    def carte_jouee(self, carte, joueur):
        qui_joue = self.pli_courant.joueur_courant
        if joueur != qui_joue: # C'est ciao
            return

        



class Pli:
    def __init__(self, jeu, n, premier_joueur):
        self.jeu = jeu
        self.joueur_courant = premier_joueur
        self.première_carte = None # couple (carte)
        self.n = n # numéro du pli : int \in {1, ..., 8}
        self.gagnant = self.premier_joueur # actualisé à chaque fois que quelqu'un joue une carte,
                         # à la fin du pli prend la valeur du gagnant (donc de celui
                         #  qui joue le suivant)
        self.carte_gagnante = None # Ca va être un couple
        self.l_joueurs = self.jeu.l_joueurs

    def single_card(self, i):
        pass



    def filtre_main(self, main):
        return #main_filtrée, cartes indisponibles grisées   
    