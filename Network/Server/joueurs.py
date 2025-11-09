
from const_srv import VALEURS_ATOUT, VALEURS_SANS

class Ekip:
    def __init__(self, n):
        self.joueurs = None
        self.points = 0
        self.points_cg = None # points current_game
        self.n = n

    def init_joueurs(self, j1, j2):
        self.joueurs = [j1, j2]

    def reset_points_current_game(self):
        self.points_cg = 0

    def ajouter_puntos(self, pu):
        self.points_cg += pu
        return self.points_cg



class Joueur:
    def __init__(self, n, n_equipe, is_nobod, pseudo):
        self.n = n # identifiant unique
        self.pseudo = pseudo
        self.n_equipe = n_equipe 
        self.is_bot = is_nobod
        """éventuellement rajouter un attribu 'équipe'"""
        assert(self.n%2 == self.n_equipe)

        # Propre à un jeu
        self.main = None



    def trie_cartes(self, at):
        trker = [[], [], [], []]
        
        for card in self.main:
            trker[card[0]].append(card)

        new = []
        for i in range(4):
            n = (at+i)%4
            t = trker[n]
            if i == 0: v = VALEURS_ATOUT
            else: v = VALEURS_SANS
            key = lambda e: v[e[1]]
            t.sort(key=key, reverse=True)
            new += t


        self.main = new
    
