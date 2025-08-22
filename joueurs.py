from tkinter import *
# from jeu import Pli
from random import choice

# Deux équipes 0 (N) et 1 (E)

class Joueur:
    def __init__(self, n, bot=True):
        self.n = n # 0 (J), 1, 2, 3
        self.ekip = n%2
        self.main = []
        self.bot = bot
    
    def joue(self, pli):
        possibles = pli.filtre_main(self.main)
        return choice(possibles)

