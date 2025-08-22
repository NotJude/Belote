from tkinter import *
from time import sleep

from const import *
from display import *
from jeu import *
from user_action import *

WHO_AM_I = 0

def card_to_ua(card, sender):
    return PlayCard(sender, card)

def send_ua(frame, game, ua):
    game.process_ua(ua)

    frame.destroy_hand()
    pli = game.jeu.pli
    valides = pli.filtre_main(game.l_joueurs[WHO_AM_I].main)
    frame.img_my(game.l_joueurs[WHO_AM_I].main, valides) # J'affiche mon jeu :D

    frame.render_pli(pli.premier_joueur, pli.table)

    look_for_bot_action(frame, game, ua)

def look_for_bot_action(frame, game, ua):
    joueur_courant = game.jeu.pli.joueur_courant
    le_j = game.l_joueurs[joueur_courant]
    if le_j.bot: # C'est un bot
        sleep(SLEEPING_TIME)
        ua = card_to_ua(le_j.action_de_bot(game.jeu.pli), joueur_courant)
        send_ua(frame, game, ua)
"""
def butt(main_frame):
    main_frame.img_my(['2_of_clubs', '5_of_diamonds', (3,12), (2,13), (3,14)])
    main_frame.add_img_mid('14_of_diamonds', 0)
    main_frame.add_img_mid('14_of_diamonds', 1)
    main_frame.add_img_mid('14_of_diamonds', 2)
    main_frame.add_img_mid('14_of_diamonds', 3)
"""
    
if __name__ == '__main__':
    # D'abord la partie graphique
    root = BeloteWindow()
    frame = root.main_frame
    # Ensutie la partie jeu
    game = Partie()
    jeu = game.jeu
    
    # Puis on met les deux en communication
    frame.configure_on_card_click(lambda card : send_ua(frame, game, card_to_ua(card, WHO_AM_I)))





    frame.img_my(game.l_joueurs[WHO_AM_I].main, game.jeu.pli.filtre_main(game.l_joueurs[WHO_AM_I].main))

    root.mainloop()