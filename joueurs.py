from tkinter import *

# Deux équipes 0 (N) et 1 (E)

class Joueur:
    def __init__(self, n):
        self.n = n # 0 (J), 1, 2, 3
        self.ekip = n%2
        
