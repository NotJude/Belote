


N = 1

#deck
SUITS = ['clubs', 'diamonds', 'spades', 'hearts']
VALUES = [i for i in range(2, 15)]
DECK = []
for suit in SUITS:
    for value in VALUES:
        DECK.append(f'{value}_of_{suit}')

#couleurs
BG = "green"

#dimensions
def ada(n):
    return round(n*N)


WIN_WIDTH = ada(960)
WIN_HEIGHT = ada(540)
WIN_DIM = (WIN_WIDTH, WIN_HEIGHT)

CARD_WIDTH = ada(98)
CARD_HEIGHT = ada(142)
CARD_DIM = (CARD_WIDTH,CARD_HEIGHT)

PAD_CARTES_M = ada(10)

PAD_CARTES_MID_HORIZ = ada(10)
PAD_CARTES_MID_VERT = ada(40)

MID_0_X = ada(WIN_WIDTH/2-CARD_WIDTH/2)
MID_0_Y = ada(WIN_HEIGHT/3 + PAD_CARTES_MID_VERT/2)

MID_1_X = MID_0_X-PAD_CARTES_MID_HORIZ-CARD_WIDTH
MID_1_H = None

# MID_2_W = MID_0_X
# MID_2_H =

# MID_3_W = 
# MID_3_H =





