
from jeu import Partie

def click_event(event):
    """
    doit appeler send_card_to_play sur le pli
    puis dans display :
    - erase_all
    - render_deck
    - render_pli
    pour mettre l'affichage à jour
    """

if __name__ == '__main__':
    p = Partie()

    p.win.configure_on_card_click(lambda c: p.jeu_courant.pli_courant.try_to_play(0,c))
    p.win.configure_ready_pli_click(lambda event: p.jeu_courant.init_next_pli())
    p.init_jeu()
    
    p.win.root.mainloop()

