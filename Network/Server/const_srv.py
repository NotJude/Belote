

#deck      0          1          2         3
SUITS = ['clubs', 'diamonds', 'spades', 'hearts']

VALUES = [i for i in range(7, 15)]
# DECK = []

TRAD_SUITS = ["Trèfle", "Carreau", "Pique", "Coeur"]


NDECK = []
for i in range(4):
    for j in range(7,15):
        NDECK.append((i,j))


VALEURS_ATOUT = {
    7 : 0,
    8 : 0,
    9 : 14,
    10 : 10,
    11 : 20,
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