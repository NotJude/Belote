
from random import shuffle

from const import NDECK



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
    
    def distribue_cinq_each(self):
        assert(len(self.current_deck)==32)
        cd = self.current_deck
        return cd[:5], cd[5:10], cd[10:15], cd[15:20]
    
    def distribue_le_reste(self, j):
        cd = self.current_deck
        t = []
        c = 21
        for i in range(4):
            if i==j:
                t.append(cd[c:c+2])
                c = c + 2
            else:
                t.append(cd[c:c+3])
                c = c + 3
        print("il reste (normalemnt 0) cartes :", 32-c)
        return t
    
    def single(self):
        return self.current_deck[20]
   
    def free_refill(self):
        self.current_deck = NDECK.copy()
