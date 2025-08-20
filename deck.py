import random
from const import DECK

class Deck:
    def __init__(self):
        suits = ["clubs", "diamonds", "spades", "hearts"]
        values = [i for i in range(2,15)]

        self.DECK = DECK.copy()
      
        self.current_deck = []
        self.free_refill()

    def shuffle(self):
        random.shuffle(self.current_deck)

    def pick(self):
        card = random.choice(self.current_deck)
        self.current_deck.remove(card)
        return card
    
    def pick_and_put_back(self):
        return random.choice(self.current_deck) 

    def empty_deck(self):
        return len(self.current_deck)==0
    
    def free_refill(self):
        self.current_deck = self.DECK.copy()
