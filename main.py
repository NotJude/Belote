from tkinter import *

from const import *
from display import *
from jeu import *
from user_action import *

WHO_AM_I = 0

def send_ua(frame, game, ua):
    game.process_ua(ua)

    pli = game.jeu.pli
    frame.render_pli(pli.premier_joueur, pli.table)

def card_to_ua(card):
    return PlayCard(WHO_AM_I, card)

def butt(main_frame):
    main_frame.img_my(['2_of_clubs', '5_of_diamonds', '12_of_hearts', '13_of_spades', '14_of_hearts'])
    main_frame.add_img_mid('14_of_diamonds', 0)
    main_frame.add_img_mid('14_of_diamonds', 1)
    main_frame.add_img_mid('14_of_diamonds', 2)
    main_frame.add_img_mid('14_of_diamonds', 3)

if __name__ == '__main__':
    # D'abord la partie graphique
    root = BeloteWindow()
    frame = root.main_frame
    # Ensutie la partie jeu
    game = Partie(frame)
    jeu = game.jeu

    # Puis on met les deux en communication
    frame.configure_on_card_click(lambda card : send_ua(frame, game, card_to_ua(card)))





    frame.img_my(['12_of_hearts', '13_of_spades', '14_of_hearts'])

    root.mainloop()