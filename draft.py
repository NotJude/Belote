from tkinter import *




w = Tk()
w.geometry("300x300")
lab = Label(w, width=50, bg="red")
lab.pack()
w.mainloop()
"""

    def display_my_hand111111(self, cards, valides=None): 
        if self.my_main != None:
            for c_lbl in self.my_main:
                c_lbl.destroy()
            self.clear_my_main()

        n = len(cards)
        taille = n*CARD_WIDTH + (n-1)*PAD_CARTES_MY
        x_min = WIN_WIDTH/2 - taille/2

        for i, card in enumerate(cards):
            x = x_min + i*(CARD_WIDTH + PAD_CARTES_MY)
            c_lbl = self.render_carte(card, x=x, y=MY_Y)
            if valides == None:
                c_lbl.config(state="disabled")
            elif card not in valides:
                c_lbl.config(state="disabled")
            else:
                def helper(j):
                    return lambda event: self.on_card_click(j)
                c_lbl.bind("<Button-1>", helper(card))
            self.my_main.append(c_lbl)

    def abt_to_play(self, cards, valides): # plus tard : la suppr

        self.display_my_hand(cards, valides)

    def display_new_to_middle(self, j, card): # dès que quelqu'un joue

        lbl = self.render_carte(card, MID_POS[j][0], MID_POS[j][1])
        # assert(self.middle[j]==None)
        # print(self.middle[j])
        self.middle[j] = lbl


    def display_end_of_pli(self):
        self.main_frame.bind("<Button-1>", self.ready_for_next_pli_click)

    def display_beg_of_pli(self):
        self.main_frame.unbind("<Button-1>")
        for lbl in self.middle:
            if lbl != None:
                lbl.destroy()
        self.clear_middle()



    def display_end_of_jeu(self):
        print("la fin du jeu")

"""