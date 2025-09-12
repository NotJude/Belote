
from random import choice

from joueurs import Ekip, Joueur
from deck import BeloteDeck
from const import ORDRE_ATOUT, ORDRE_SANS
from display import BeloteWindow


class Partie:

    def __init__(self):
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
        # self.jeu_courant = Jeu(self, 3)
        self.jeu_courant= None

    def init_jeu(self):
        self.jeu_courant = Jeu(self, 3)
    

    def jeu_fini(self):
        pass
        





class Jeu:
    def __init__(self, partie, dealer):
        self.partie = partie
        self.dealer = dealer

        self.pli_courant = None
        self.n_pli = 0
        self.atout = None

        self.joueur_courant = (self.dealer + 1)%4
        
        self.tour_atout = 1

        self.initialiser()

    def pli_fini(self):
        if self.n_pli == 8:
            print("Le jeu est finito (c'est ciao)")
            self.partie.jeu_fini()
        else:
            # plus tard : remballer les cartes dans l'ordre
            w = self.partie.win
            w.waiter()
            # w.clear_mid()


    def get_stjc(self):
        return self.partie.joueurs[self.joueur_courant]

    def init_next_pli(self):
        w = self.partie.win
        # w.display_beg_of_pli()
        w.clear_mid()
        w.done_waiting()
        if self.n_pli==0:
            g = (self.dealer + 1)%4
        else:
            g = self.pli_courant.joueur_leader
        self.nouv_pli(g)

    
    def initialiser(self):
        part = self.partie
        deck = part.deck
        joueurs = part.joueurs
        deez = deck.distribue_cinq_each()
        w = self.partie.win

        for j in range(4):
            joueurs[j].main = deez[j]

        self.single = deck.single()

        # affichage
        w.display_single(self.single)
        # w.clear_my_main()
        w.display_my_hand(joueurs[0].main)

        self.suiv_at()

    
    def suiv_at(self):
        stjc = self.get_stjc()
        if stjc.is_bot:
            self.at_def(4)
        elif self.joueur_courant == 0:
            # affichage
            coul_single = self.single[0]
            w = self.partie.win
            if self.tour_atout == 1:
                w.display_but_une(coul_single)
            elif self.tour_atout == 2:
                l = list(range(4))
                l.remove(coul_single)
                w.display_but_deux(l)
            else:
                print("erreur de tour", self.tour_atout)
                raise ValueError

        


    def at_def(self, a): # 4 : passer, 0 : clubs
        """
        si self.jc = self.dealer && a==4: s.tour = 2 & suiv_at()
        """
        stjc = self.get_stjc()
        w = self.partie.win

        if self.joueur_courant == 0: # si c'est nous
            w.clear_at_butts()

        if a == 4: # si on a passé
            if self.joueur_courant != self.dealer: # on a fait un tour entier
                self.joueur_courant = (self.joueur_courant + 1)%4
                self.suiv_at()
            else:  
                if self.tour_atout == 1:
                    self.tour_atout = 2
                    self.joueur_courant = (self.joueur_courant + 1)%4
                    self.suiv_at()
                else:
                    #print("self.tour_atout (normalemnt 2) : ", self.tour_atout)
                    w.clear_my_main()
                    w.clear_single()
                    # w.clear_at_butts()
                    self.partie.jeu_fini()                


        else: # start_game
            self.atout = a
            w.set_atout(a)
            stjc.main.append(self.single)
            t = self.partie.deck.distribue_le_reste(self.joueur_courant)
            for i, joueur in enumerate(self.partie.joueurs):
                for c in t[i]:
                    joueur.main.append(c)
            w.clear_single()
            w.clear_my_main()
            w.waiter()

        


    def nouv_pli(self, g):
        # w = self.partie.win
        self.n_pli += 1
        self.pli_courant = Pli(self, g)
        



class Pli:
    
    def __init__(self, jeu, premier_joueur):
        self.premier_joueur = premier_joueur
        self.joueur_courant = premier_joueur
        self.joueur_leader = None
        
        self.card_leader = None 
        self.couleur_demandee = None

        self.jeu = jeu
        self.tapis = []

        w = self.jeu.partie.win
        st_nous = self.jeu.partie.joueurs[0]
        
        w.clear_my_main()
        w.display_my_hand(st_nous.main)
        w.done_waiting()
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
        w.add_to_mid(self.joueur_courant, card)

        # mettre à jour la main et si besoin, afficher notre nouvelle main
        st_joueur_courant = self.get_stjc()
        st_joueur_courant.main.remove(card)
        if self.joueur_courant == 0: # plus tard : réfléchir
            w.clear_my_main()
            # w.waiter()
            w.display_my_hand(st_joueur_courant.main) # affiche la nouvelle main en désactivant les cartes

        # la suite du pli
        assert(0<n and n<=4)
        if n == 4:
            b = self.compare_bis(self.card_leader, card)
            if not b:
                self.card_leader = card
                self.joueur_leader = self.joueur_courant
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
            w.activate_my_hand(valides)
            # w.abt_to_play(st_jc.main, valides) # active les bonnnes cartes

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
                if len(atouts_sup) > 0: 
                    return atouts_sup
                elif len(nos_atouts) > 0:
                    return nos_atouts
                else:
                    return main
            else:
                nos_coul, _ = self.filtrer_couleur(main, self.couleur_demandee)
                if len(nos_coul)>0:
                    return nos_coul
                elif self.joueur_leader%2 != self.joueur_courant%2:
                    if len(atouts_sup)>0:
                        return atouts_sup
                    elif len(nos_atouts)>0:
                        return nos_atouts
                    else:
                        return main
                else:
                    return main

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

    