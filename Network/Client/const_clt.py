

#deck      0          1          2         3
SUITS = ['clubs', 'diamonds', 'spades', 'hearts']

VALUES = [i for i in range(7, 15)]
# DECK = []

NDECK = []
for i in range(4):
    for j in range(7,15):
        NDECK.append((i,j))

TRAD_SUITS = ["Trèfle", "Carreau", "Pique", "Coeur"]


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


# network

SERIALIZED_LENGTH = 50

def card_to_str(card):
    return str(card[0])+"-"+str(card[1])

def cardz_to_str(cards):
    s = ""
    for card in cards:
        s = s + "/" + card_to_str(card)
    return s

def strz_to_cards(sts):
    l = []
    for s in sts:
        c = str_to_card(s)
        l.append(c)
    return l
        

def str_to_card(s):
    l = s.split("-")
    return (int(l[0]), int(l[1]))