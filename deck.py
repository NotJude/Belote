import random
from const import NDECK

class Deck:
    def __init__(self):
      
        self.current_deck = []
        self.free_refill()

    def shuffleD(self):
        random.shuffle(self.current_deck)

    def distribue(self):
        self.shuffleD()
        assert(len(self.current_deck)==32)
        cu = self.current_deck
        return cu[:8], cu[8:16], cu[16:24], cu[24:32]

    def pick(self):
        card = random.choice(self.current_deck)
        self.current_deck.remove(card)
        return card
    
    def pick_and_put_back(self):
        return random.choice(self.current_deck) 

    def empty_deck(self):
        return len(self.current_deck)==0
    
    def free_refill(self):
        self.current_deck = NDECK.copy()
