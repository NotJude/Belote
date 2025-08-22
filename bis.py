from tkinter import *

from const import *

from display import *



def butt(main_frame):
    main_frame.add_img_my(['2_of_clubs', '5_of_diamonds', '12_of_hearts', '13_of_spades', '14_of_hearts'])
    main_frame.add_img_mid('14_of_diamonds', 0)

if __name__ == '__main__':
    root = BeloteWindow()
    shuffle_button = Button(root.main_frame, text=" button", command=lambda:butt(root.main_frame))
    shuffle_button.pack()

    root.mainloop()

