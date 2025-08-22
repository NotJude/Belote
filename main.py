from tkinter import *

from const import *

from display import *



def butt(main_frame):
    main_frame.img_my(['2_of_clubs', '5_of_diamonds', '12_of_hearts', '13_of_spades', '14_of_hearts'])
    main_frame.add_img_mid('14_of_diamonds', 0)
    main_frame.add_img_mid('14_of_diamonds', 1)
    main_frame.add_img_mid('14_of_diamonds', 2)
    main_frame.add_img_mid('14_of_diamonds', 3)

if __name__ == '__main__':
    root = BeloteWindow()
    # j = Jeu(frame=root.main_frame)

    root.mainloop()