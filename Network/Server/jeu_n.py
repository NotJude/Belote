
from random import choice

from deck import BeloteDeck
from const_srv import ORDRE_ATOUT, ORDRE_SANS, VALEURS_ATOUT, VALEURS_SANS, card_to_str, cardz_to_str


"""
waiter ????
"""


def seri_dmm(main, coul_mid):
    return "c" + cardz_to_str(main) + "/" + str(coul_mid)

def helper_seri(l, c):
    s = c
    for e in l:
        s = s + '/' + str(e)
    return s

def seri_dbd(l_col):
    return helper_seri(l_col, "f")

# innutile (for now)
def seri_apt(l_scr):
    return helper_seri(l_scr, )
    

class Partie:

    def __init__(self, mg):
        # display
        # self.win = BeloteWindow() # CEST CIAO

        self.mg = mg
        self.joueurs = mg.joueurs
        self.equipes = mg.equipes

        # deck
        self.deck = BeloteDeck()

        # jeu
        self.jeu_courant = None
        self.init_jeu()


    def init_jeu(self):
        self.jeu_courant = Jeu(self, 3)
    

    def jeu_fini(self):
        pass
        


class Jeu:
    def __init__(self, partie, dealer):
        self.partie = partie
        self.dealer = dealer
        # self.w = self.partie.win
        self.joueurs = self.partie.joueurs
        self.equipes = self.partie.equipes

        self.pli_courant = None
        self.n_pli = 0
        self.atout = None

        self.jc = (self.dealer + 1)%4
        self.tour_atout = 1

        self.sendf = self.partie.mg.send
        self.recievf = self.partie.mg.recieve

        for equipe in self.equipes:
            equipe.reset_points_current_game()

        self.partie.mg.set_jeu_courant(self)

        self.jeu_initialiser()


    def get_stjc(self):
        return self.joueurs[self.jc]
    
    def get_equipe(self, j):
        joueur = self.joueurs[j]
        return joueur.n_equipe
    
    def act_puntos(self, j, tot):
        e = self.get_equipe(j)
        equipe = self.equipes[e]
        all = equipe.ajouter_puntos(tot)

        s = "j/" + str(e) + "/" + str(all)
        self.send_all(s)
        # self.w.actualiser_puntos_tg(e, all)
        

    def jeu_initialiser(self): # pas une vraie fonction
        part = self.partie
        deck = part.deck
        joueurs = self.joueurs
        deez = deck.distribue_cinq_each()

        for j in range(4):
            joueurs[j].main = deez[j]

        self.single = deck.single()

        # affichage
        # self.w.clear_puntos_tg()
        self.send_all("a")
        self.send_all("b/"+card_to_str(self.single))
        
        self.send_dmm()
            
        # self.w.display_ma_main(joueurs[0].main, self.single[0]) # affichage en jaune si c'est de l'atout potentiel (de la couleur de single)
        self.suiv_at()


    def send_all(self, c): # on veut envoyer la meme chose aux 4 joueurs
        for j in range(4):
            self.sendf(c, j)

    def send_dmm(self):
        for i in range(4):
            s = seri_dmm(self.joueurs[i].main, self.single[0])
            self.sendf(s, i)


    def suiv_at(self):

        stjc = self.get_stjc()
        if stjc.is_bot:
            self.tr_req_at(4)

        else: # on n'a pas affaire à un nobod
            # if self.jc == 0:
            # affichage
            coul_single = self.single[0]
            if self.tour_atout == 1:
                # self.w.display_but_une(coul_single)
                self.sendf("d/"+str(coul_single), self.jc)
                self.recievf(self.jc) # ça part en traitement dans manageGame

            else: 
                l = list(range(4))
                l.remove(coul_single)
                self.sendf("e", self.jc)
                # self.w.clear_ma_main()
                s = seri_dmm(self.joueurs[self.jc].main, 5)
                self.sendf(s, self.jc)
                # self.display_ma_main(self.joueurs[0].main, 5) # 5 : pas de signification
                s = seri_dbd(l)
                self.sendf(s, self.jc)
                # self.w.display_but_deux(l)
                self.recievf(self.jc)

            

    def tr_req_at(self, a): # traite requete atout

        s = "g"
        self.sendf(s, self.jc)
        # self.w.clear_at_butts()

        if a == 4: # si on a passé
            self.jc = (self.jc + 1)%4
            if self.jc != (self.dealer + 1)%4: 
                self.suiv_at()
            else:  # on a fait un tour entier
                if self.tour_atout == 1:
                    self.tour_atout = 2
                    self.suiv_at()
                else:
                    self.send_all("e")
                    # self.w.clear_ma_main()
                    self.send_all("h")
                    # self.w.clear_single()
                    self.partie.jeu_fini()

        else: # start_game
            self.atout = a
            stjc = self.get_stjc()
            stjc.main.append(self.single)
            t = self.partie.deck.distribue_le_reste(self.jc)
            for i, joueur in enumerate(self.joueurs):
                for c in t[i]:
                    joueur.main.append(c)
                joueur.trie_cartes(a)

            s = "i/" + str(a)
            self.send_all(s)
            # self.w.set_atout(a)
            self.send_all("h")
            # self.w.clear_single()

            self.send_all("e")
            for i in range(4):
                s = seri_dmm(self.joueurs[i].main, self.atout)
                self.sendf(s, i)
            self.pli_fini((self.dealer + 1)%4)
            
            # self.w.clear_ma_main() ; self.w.display_ma_main(st_nous.main, a)
            # self.w.waiter()


    def compter_puntos(self, tbl):
        s = 0
        for card in tbl:
            if card[0] == self.atout: s += VALEURS_ATOUT[card[1]]
            else: s += VALEURS_SANS[card[1]]
        return s
            

    def pli_fini(self, jl):

        self.send_all("k")
        # self.w.clear_mid()
        # self.w.done_waiting()

        if self.n_pli == 8: # le jeu est fini
            self.act_puntos(jl, 10) # 10 de der
            self.partie.jeu_fini()

        else: # commencer le pli suivant
            
            # if self.n_pli==0:
            #     g = (self.dealer + 1)%4
            # else:
            #     g = pli.jl
            self.n_pli += 1
            self.pli_courant = Pli(self, jl)

 


class Pli:
    
    def __init__(self, jeu, premier_joueur):
        self.pj = premier_joueur
        self.jc = premier_joueur
        self.atout = jeu.atout
        self.jl = None
        self.card_leader = None 
        self.couleur_demandee = None
        self.tapis = []

        self.jeu = jeu
        # self.w = self.jeu.w

        self.send_all = self.jeu.send_all
        self.sendf = self.jeu.sendf

        self.jeu.partie.mg.set_pli_courant(self)

        # self.w.done_waiting()
        self.next_()


    def nb_cartes_jouees(self):
        return len(self.tapis)
    
    def get_stjc(self): # renvoie le joueur courant (en tant qu'instance de joueurs.Joueur)
        return self.jeu.partie.joueurs[self.jc]
        

    def jouer_carte(self, card):
        # nouvelle carte sur la table
        self.tapis.append(card)
        s = "l/" + card_to_str(card) + "/" + str(self.atout) + "/" + str(self.jc)
        self.send_all(s)
        # self.w.add_to_mid(self.jc, card, self.atout)

        # mettre à jour la main et si besoin, afficher notre nouvelle main
        st_joueur_courant = self.get_stjc()
        st_joueur_courant.main.remove(card)

        self.sendf("e", self.jc)
        s = seri_dmm(st_joueur_courant.main, self.atout)
        self.sendf(s, self.jc)

        # if self.jc == 0: # plus tard : réfléchir
        #     self.w.clear_ma_main()
        #     self.w.display_ma_main(st_joueur_courant.main, self.atout)
        

        n = self.nb_cartes_jouees()
        if 1<n<=4:
            b = self.compare_bis(self.card_leader, card)
            if not b:
                self.card_leader = card
                self.jl = self.jc
            if n==4:
                deck = self.jeu.partie.deck
                eg = self.jeu.get_equipe(self.jl) # equipe_gagnante
                self.jeu.act_puntos(self.jl, self.jeu.compter_puntos(self.tapis))
                # remballer les cartes
                deck.remballe(eg, self.tapis)
                # self.w.waiter()
                self.jeu.pli_fini(self.jl)
        if 1<=n<4:
            if n==1:
                self.card_leader = self.tapis[0]
                self.jl = self.pj
                self.couleur_demandee = self.tapis[0][0]
            self.jc = (self.jc + 1)%4
            self.next_()            


    def next_(self):
        
        st_jc = self.get_stjc()
        valides = self.cartes_jouables()

        if st_jc.is_bot:
            c = choice(valides)
            self.jouer_carte(c)

        else:
            # self.w.activate_ma_main(valides)
            s = "m" + cardz_to_str(valides)
            self.sendf(s, self.jc)
            self.jeu.recievf(self.jc)


    def cartes_jouables(self): 
        stjc = self.get_stjc()
        main = stjc.main.copy()
        if self.jc == self.pj:
            return main
        else:
            nos_atouts, atouts_sup = self.filtrer_couleur(main, self.atout)
            if self.couleur_demandee==self.atout:
                if len(atouts_sup) > 0: return atouts_sup
                elif len(nos_atouts) > 0: return nos_atouts
                else: return main
            else:
                nos_coul, _ = self.filtrer_couleur(main, self.couleur_demandee)
                if len(nos_coul)>0: return nos_coul
                elif self.jl%2 != self.jc%2:
                    if len(atouts_sup)>0: return atouts_sup
                    elif len(nos_atouts)>0: return nos_atouts
                    else: return main
                else: return main

    
    def filtrer_couleur(self, main, couleur):
        coul_nos, coul_sup = [], []
        for card in main:
            if card[0] == couleur:
                coul_nos.append(card)
                if self.compare_bis(card, self.card_leader):
                    coul_sup.append(card)
        return coul_nos, coul_sup


    def compare_bis(self, maitre, candidat): # renvoie True si Émillien conserve son titre
        at = self.atout
        dmd = self.couleur_demandee
        if candidat[0] == at:
            if maitre[0] == at:
                return ORDRE_ATOUT.index(maitre[1]) > ORDRE_ATOUT.index(candidat[1])
            else: # maitre[0] == dmd
                return False
        elif candidat[0] == dmd and maitre[0] == dmd:
            return ORDRE_SANS.index(maitre[1]) > ORDRE_SANS.index(candidat[1])
        return True    