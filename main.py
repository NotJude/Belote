
from jeu import Partie



if __name__ == '__main__':
    p = Partie()

    p.win.configure_on_card_click(lambda c: p.jeu_courant.pli_courant.try_to_play(0,c))
    p.win.configure_waiter_click(lambda event: p.jeu_courant.init_next_pli())
    p.win.configure_at_click(lambda a: p.jeu_courant.at_def(a))
    p.init_jeu()
    
    p.win.root.mainloop()

