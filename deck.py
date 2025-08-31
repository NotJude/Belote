
from random import shuffle

from const import NDECK


def compare(c1, c2, atout, demandee): # demandée est la couleur de la première carte du pli
    pass


class BeloteDeck:
    def __init__(self):
      
        self.current_deck = []
        self.free_refill()
        self.shuffleD()

    def shuffleD(self):
        shuffle(self.current_deck)

    def distribue(self): # plus tard : distribuer en 2-3 (ou 3-2 avec proba 1/2) puis vider le jeu
        self.shuffleD()
        assert(len(self.current_deck)==32)
        cu = self.current_deck.copy()
        # self.current_deck = []
        return cu[:8], cu[8:16], cu[16:24], cu[24:32]
   
    def free_refill(self):
        self.current_deck = NDECK.copy()
