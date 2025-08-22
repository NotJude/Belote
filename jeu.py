from joueurs import Joueur
from random import randint
from const import VALEURS_ATOUT, VALEURS_SANS
from deck import Deck


class Partie:
    def __init__(self):

        l_joueurs = []
        j = Joueur(0, bot=False)
        l_joueurs.append(j)
        for i in range(1, 4):
            j = Joueur(i, bot=True)
            l_joueurs.append(j)
        self.l_joueurs = l_joueurs
        self.jeu = Jeu(self, 3)


    def process_ua(self, ua):
        if self.jeu.pli.joueur_courant != ua.sender:
            print("pas à ton tour")
            return # a joué quand c'est pas à son tour
        
        self.l_joueurs[ua.sender].defausser(ua.card)
        self.jeu.carte_jouee(ua.card)

class Jeu:
    def __init__(self, partie, init_dealer):
        self.dealer = init_dealer
        # animation pour sélectionner l'atout
        self.atout = 0
        self.partie = partie

        self.deck = Deck()
        distribution = self.deck.distribue()

        self.l_joueurs = self.partie.l_joueurs
        for i in range(4):
            self.l_joueurs[i].main = distribution[i]



        self.pli = Pli(self, 1, (init_dealer + 1) % 4)

    def carte_jouee(self, carte):
        self.pli.ajouter_carte(carte)

        if len(self.pli.table) == 4:
            print("Il faudra changer de pli")
            n_pli = self.pli.n
            if n_pli == 8:
                print("Le pli est fini")
                self.est_fini()
            else:
                gagnant = self.pli.joueur_leader
                Pli(self, n_pli+1, gagnant)
    
    def est_fini(self):
        pass

class Pli:
    def __init__(self, jeu, n, premier_joueur): # joueur est un int entre \in {0, ..., 3}
        self.jeu = jeu
        self.premier_joueur = premier_joueur
        self.joueur_leader = premier_joueur
        self.joueur_courant = premier_joueur
        self.card_leader = None
        self.n = n # numéro du pli : int \in {1, ..., 8}
        self.table = [] # Les cartes jetées sur la table (dans l'ordre chronologique)

        self.premiere_couleur = None

    def ajouter_carte(self, carte):
        self.table.append(carte)
        if len(self.table)==1:
            self.card_leader = carte
            self.premiere_couleur = carte[0]
        else:
            if self.compare(self.card_leader, carte) == carte:
                self.card_leader = carte
                self.joueur_leader = (self.premier_joueur + len(self.table)-1)%4

        self.joueur_courant = (self.joueur_courant + 1) % 4

    def compare(self, c1, c2): # appelée seulement si la première carte à été jouée ou si c1 et c2 sont des atouts
        atout = self.jeu.atout
        if c1[0]==atout:
            if c2[0] != atout:
                return c1
            else:
                def f(k):
                    return VALEURS_ATOUT[k] + 1/100*k
                if f(c1[1])>f(c2[1]):
                    return c1
                else:
                    return c2
        elif c2[0] == atout:
            return c2
        else:
            if c1[0] == self.premiere_couleur:
                if c2[0] != self.premiere_couleur:
                    return c1
                else:
                    def f(k):
                        return VALEURS_SANS[k] + 1/100*k
            elif c2[0] == self.premiere_couleur:
                return c2
            else:
                raise ZeroDivisionError


    def filtre_main(self, main):
        if self.joueur_courant == self.premier_joueur:
            return main
        else:
            nos_atouts, atouts_sup = self.filtrer_couleur(main, self.jeu.atout)
            if self.premiere_couleur==self.jeu.atout:
                if len(atouts_sup) > 0: return atouts_sup
                elif len(nos_atouts) > 0: return nos_atouts
                else: return main
            else:
                nos_coul, _ = self.filtrer_couleur(main, self.premiere_couleur)
                if len(nos_coul)>0: return nos_coul
                elif self.joueur_leader%2 != self.joueur_courant%2 and len(nos_atouts)>0: return nos_atouts
                else: return main

    def filtrer_couleur(self, main, couleur):
        nos_atouts, atouts_sup = [], []
        for card in main:
            if card[0] == couleur:
                nos_atouts.append(card)
            if self.compare(card, self.card_leader) == card:
                atouts_sup.append(card)
        return nos_atouts, atouts_sup

    
    