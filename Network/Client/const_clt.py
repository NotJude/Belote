

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

# network

SERIALIZED_LENGTH = 100
MAX_ROOMS = 4

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

def recieve(conn):
    data = conn.recv(SERIALIZED_LENGTH).decode()
    print("reciv clt",data)
    l_data = data.split("/")
    return l_data[:-1]

def unprocess(l_data): # return : f, liste de nombres, liste de cartes
    print("unprocesss clt", l_data)
    f = l_data[0]
    ns = l_data[1]
    cs = l_data[2]
    raw_numbers = [int(e) for e in ns.split("*")[:-1]]
    raw_cards = [str_to_card(e) for e in cs.split("*")[:-1]]
    return f, raw_numbers, raw_cards

def send(conn, l_data):
    data = ""
    for e in l_data:
        data = data + e + "/"
    l = len(data)
    c = data + ' '*(SERIALIZED_LENGTH-l)
    conn.send(str.encode(c))

def process(m, raw_numbers, raw_cards):
    s, t = "", ""
    for i in raw_numbers:
        s = s + str(i) + '*'
    for c in raw_cards:
        t = t + card_to_str(c) + '*'
    l_data = [m, s, t]
    return l_data


WIN_WIDTH = ada(960)
WIN_HEIGHT = ada(540)
WIN_DIM = (WIN_WIDTH, WIN_HEIGHT)

BORDER = 2

CARD_WIDTH = ada(98)
CARD_HEIGHT = ada(142)
CARD_DIM = (CARD_WIDTH,CARD_HEIGHT)

S_CARD_WIDTH = ada(1/10*CARD_WIDTH)
S_CARD_HEIGHT = ada(1/10*CARD_HEIGHT)
S_CARD_DIM = (S_CARD_WIDTH,S_CARD_HEIGHT)

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

H_TEXT = 10 # hauteur du texte
PSEUDO_0_X = ada(0)
PSEUDO_0_Y = ada(WIN_HEIGHT-CARD_HEIGHT/2-H_TEXT/2)

PSEUDO_1_X = ada(10)
PSEUDO_1_Y = ada(WIN_HEIGHT/2 - H_TEXT/2)

PSEUDO_2_X = ada(WIN_WIDTH/2-CARD_WIDTH/2)
PSEUDO_2_Y = ada(10)

PSEUDO_3_X = ada(WIN_WIDTH-100)
PSEUDO_3_Y = ada(PSEUDO_1_Y)

PSEUDO_POS = [(PSEUDO_0_X, PSEUDO_0_Y), (PSEUDO_1_X, PSEUDO_1_Y), (PSEUDO_2_X, PSEUDO_2_Y), (PSEUDO_3_X, PSEUDO_3_Y)]

ROOM_X = 0
ROOM_Y = ada(WIN_HEIGHT - 20)



# welcome page
T_HEIGHT = 20
# texte pseudo
PSEUDO_WIDTH = 40
PSEUDO_HEIGHT = T_HEIGHT
PSEUDO_X = ada(WIN_WIDTH/2-PSEUDO_WIDTH/2)
PSEUDO_Y = 50

# bouton créer
B_CR_WIDTH = 100
B_CR_HEIGHT = T_HEIGHT
B_CR_X = ada(WIN_WIDTH/2-B_CR_WIDTH/2)
B_CR_Y = 100

# bouton rejoindre
B_REJ_WIDTH = 100
B_REJ_HEIGHT = T_HEIGHT
B_REJ_X = ada(WIN_WIDTH/2-B_REJ_WIDTH-5)
B_REJ_Y = 150

# texte rejoindre
REJ_WIDTH = MAX_ROOMS*10
REJ_HEIGHT = T_HEIGHT
REJ_X = ada(WIN_WIDTH/2+5)
REJ_Y = 150



SLEEPING_TIME = 0.3
