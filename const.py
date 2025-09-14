
import tkinter.font

#deck      0          1          2         3
SUITS = ['clubs', 'diamonds', 'spades', 'hearts']
VALUES = [i for i in range(7, 15)]
# DECK = []

# TRAD_SUITS


NDECK = []
for i in range(4):
    for j in range(7,15):
        NDECK.append((i,j))


VALEURS_ATOUT = {
    7 : 0,
    8 : 0,
    9 : 14,
    10 : 10,
    11 : 21,
    12 : 3,
    13 : 4,
    14 : 11
}
ORDRE_ATOUT = sorted(VALEURS_ATOUT.keys(), key=lambda x: VALEURS_ATOUT[x])
VALEURS_SANS = {
    7 : 0,
    8 : 0,
    9 : 0,
    10 : 10,
    11 : 2,
    12 : 3,
    13 : 4,
    14 : 11
}
ORDRE_SANS = sorted(VALEURS_SANS.keys(), key=lambda x: VALEURS_SANS[x])


"""graphique"""

#couleurs
BG = "green"
GOLD = "#ffd700"

#dimensions
N = 1

def ada(n):
    return round(n*N)



WIN_WIDTH = ada(960)
WIN_HEIGHT = ada(540)
WIN_DIM = (WIN_WIDTH, WIN_HEIGHT)

BORDER = 2

CARD_WIDTH = ada(98)
CARD_HEIGHT = ada(142)
CARD_DIM = (CARD_WIDTH,CARD_HEIGHT)

PAD_CARTES_MY = ada(10)

PAD_CARTES_MID_HORIZ = 10*N
PAD_CARTES_MID_VERT = 10*N

PAD_CARD_PL_H = (WIN_HEIGHT/3-CARD_HEIGHT)/2

MY_Y = ada(2/3*WIN_HEIGHT + PAD_CARD_PL_H) 

MID_0_X = ada(WIN_WIDTH/2-CARD_WIDTH/2)
MID_0_Y = ada(2*WIN_HEIGHT/3 - PAD_CARTES_MID_VERT - CARD_HEIGHT)

MID_1_X = ada(MID_0_X-PAD_CARTES_MID_HORIZ-CARD_WIDTH)
MID_1_Y = ada(WIN_HEIGHT/3 - CARD_HEIGHT/2)

MID_2_X = ada(MID_0_X)
MID_2_Y = ada(PAD_CARTES_MID_VERT)

MID_3_X = ada(WIN_WIDTH/2 + CARD_WIDTH/2 + PAD_CARTES_MID_HORIZ)
MID_3_Y = ada(MID_1_Y)

MID_POS = [(MID_0_X, MID_0_Y), (MID_1_X, MID_1_Y), (MID_2_X, MID_2_Y), (MID_3_X, MID_3_Y)]

SINGLE_X = ada(MID_0_X)
SINGLE_Y = ada(MID_1_Y)

SLEEPING_TIME = 0.3




