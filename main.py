
from jeu import Partie



if __name__ == '__main__':
    p = Partie()

    p.win.configure_on_card_click(lambda c: p.jeu_courant.pli_courant.jouer_carte(c))
    p.win.configure_waiter_click(lambda event: p.jeu_courant.pli_fini())
    p.win.configure_at_click(lambda a: p.jeu_courant.tr_req_at(a))
    p.init_jeu()
    
    p.win.root.mainloop()

