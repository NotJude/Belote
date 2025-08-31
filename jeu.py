
from random import choice

from joueurs import Ekip, Joueur
from deck import BeloteDeck
from const import ORDRE_ATOUT, ORDRE_SANS
from display import BeloteWindow


class Partie:
    """
    Créer une Partie (__init__)
    Créer les 4 joueurs (args ?)
    Lancer un Jeu
     - self.jeu_courant
    """

    def __init__(self):
        """
        Initialiser les équipes, joueurs, jeu_courant, init_jeu
        """
        # display
        self.win = BeloteWindow()

        # equipes
        nous = Ekip(0)
        eux = Ekip(1)
        self.equipes = [nous, eux]

        # joueurs
        self.joueurs = []
        j = Joueur(0, 0, is_nobod=False)
        self.joueurs.append(j)
        for i in range(1,4):
            j = Joueur(i, i%2, True)
            self.joueurs.append(j)
        nous.init_joueurs(self.joueurs[0], self.joueurs[2])
        eux.init_joueurs(self.joueurs[1], self.joueurs[3])

        # deck
        self.deck = BeloteDeck()

        # jeu
        self.jeu_courant = None
    

        
    def init_jeu(self):
        distribution = self.deck.distribue()
        for i,j in enumerate(self.joueurs):
            j.main = distribution[i]
        self.jeu_courant = Jeu(self, 3)

    def jeu_fini(self):
        w = self.win
        w.display_end_of_jeu() 

class Jeu:
    """
    Lancer un Pli
    """
    def __init__(self, partie, dealer):
        self.partie = partie
        self.dealer = dealer

        self.pli_courant = None
        self.n_pli = 0
        self.atout = None

        self.init_atout()
        self.init_pli()

    def init_pli(self):
        jc = (self.dealer + 1)%4 # joueur qui commence se trouve à la droite de dealer
        self.n_pli += 1
        self.pli_courant = Pli(self, jc)

    def pli_fini(self):
        if self.n_pli == 8:
            print("Le jeu est finito (c'est ciao)")
            self.partie.jeu_fini()
        else:
            # plus tard : remballer les cartes dans l'ordre
            w = self.partie.win
            w.display_end_of_pli()

    def init_next_pli(self):
            w = self.partie.win
            w.display_beg_of_pli()
            g = self.pli_courant.joueur_leader
            self.pli_courant = Pli(self, g)

    def init_atout(self):
        self.atout = 0 # trèfle pour l'instant



class Pli:
    
    def __init__(self, jeu, premier_joueur):
        self.premier_joueur = premier_joueur
        self.joueur_courant = premier_joueur
        self.joueur_leader = None
        
        self.card_leader = None 
        self.couleur_demandee = None

        self.jeu = jeu
        self.tapis = []

        self.next_()

    def send_card_to_play(self, j, card): ## pb : qui appele cette méthode
        self.try_to_play(j, card)


    def try_to_play(self, j, card):
        if j == self.joueur_courant:
            if self.est_jouable(card):
                self.jouer_carte(card)
        else:
            self.next_() # on réessaye (le print pour s'assurer de ne pas avoir + infini)
            # print("pas moyen de jouer")


    def nb_cartes_jouees(self):
        return len(self.tapis)
    
    def get_stjc(self): # renvoie le joueur courant (en tant qu'instance de joueurs.Joueur)
        return self.jeu.partie.joueurs[self.joueur_courant]
        

    def jouer_carte(self, card): # on passe par ici dès qu'une carte est jouée
        # param utils
        n = self.nb_cartes_jouees() + 1 # plus tard : c'est un peu bof (mettre cette ligne après avoir ajouté la carte au tapis ?)
        w = self.jeu.partie.win

        # nouvelle carte sur la table
        self.tapis.append(card)
        w.display_new_to_middle(self.joueur_courant, card)

        # mettre à jour la main et si besoin, afficher notre nouvelle main
        st_joueur_courant = self.get_stjc()
        st_joueur_courant.main.remove(card)
        if self.joueur_courant == 0: # plus tard : réfléchir
            w.display_my_hand(st_joueur_courant.main) # affiche la nouvelle main en désactivant les cartes



        # la suite du pli
        assert(0<n and n<=4)
        if n == 4:
            self.jeu.pli_fini()

        else:
            if n==1:
                self.card_leader = self.tapis[0]
                self.joueur_leader = self.premier_joueur
                self.couleur_demandee = self.tapis[0][0]
            else:
                b = self.compare_bis(self.card_leader, card)
                if not b:
                    self.card_leader = card
                    self.joueur_leader = self.joueur_courant

            self.joueur_courant = (self.joueur_courant + 1)%4
            self.next_()

    def next_(self):
        # regarder si le jc (le nouveau joueur courant) est un nobod, si oui appeler bot_play (fonction de ua ou méthode de joueur idk)
        st_jc = self.get_stjc()
        valides = self.cartes_jouables()
        if st_jc.is_bot:
            c = choice(valides)
            
            self.send_card_to_play(self.joueur_courant, c)
        else: # self.joueur_courant is me -> "affichage"
            w = self.jeu.partie.win
            stjc = self.get_stjc()
            w.abt_to_play(stjc.main, valides) # active les bonnnes cartes

    def est_jouable(self, card):
        return card in self.cartes_jouables()

    def cartes_jouables(self): # plus tard : à vérifier...
        stjc = self.get_stjc()
        main = stjc.main.copy()
        if self.joueur_courant == self.premier_joueur:
            return main
        else:
            nos_atouts, atouts_sup = self.filtrer_couleur(main, self.jeu.atout)
            if self.couleur_demandee==self.jeu.atout:

                if len(atouts_sup) > 0: return atouts_sup
                elif len(nos_atouts) > 0: return nos_atouts
                else: return main
            else:
                nos_coul, _ = self.filtrer_couleur(main, self.couleur_demandee)
                if len(nos_coul)>0: return nos_coul
                elif self.joueur_leader%2 != self.joueur_courant%2 and len(nos_atouts)>0: return nos_atouts
                else: return main

    def compare_bis(self, maitre, candidat): # renvoie True si Émillien conserve son titre
        at = self.jeu.atout
        dmd = self.couleur_demandee
        if candidat[0] == at:
            if maitre[0] == at:
                return ORDRE_ATOUT.index(maitre[1]) > ORDRE_ATOUT.index(candidat[1])
            else: # maitre[0] == dmd
                return False
        elif candidat[0] == dmd and maitre[0] == dmd:
            return ORDRE_SANS.index(maitre[1]) > ORDRE_SANS.index(candidat[1])
        
        return True
    
    def filtrer_couleur(self, main, couleur):
        nos_atouts, atouts_sup = [], []
        for card in main:
            if card[0] == couleur:
                nos_atouts.append(card)
                if self.compare_bis(card, self.card_leader):
                    atouts_sup.append(card)
        return nos_atouts, atouts_sup

    