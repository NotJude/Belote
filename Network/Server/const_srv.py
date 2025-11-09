

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

SERIALIZED_LENGTH = 100
MAX_ROOMS = 4

def card_to_str(card):
    return str(card[0])+"-"+str(card[1])
        

def str_to_card(s):
    l = s.split("-")
    return (int(l[0]), int(l[1]))

def recieve(conn):
    data = conn.recv(SERIALIZED_LENGTH).decode()
    l_data = data.split("/")
    return l_data[:-1]

def unprocess(l_data): # return : f, liste de nombres, liste de cartes
    # print("unprocess", l_data)
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
    s,t = "",""
    for i in raw_numbers:
        s = s + str(i) + '*'
    for c in raw_cards:
        t = t + card_to_str(c) + '*'
    l_data = [m, s, t]
    return l_data