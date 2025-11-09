
import socket
from _thread import start_new_thread

from const_clt import send, recieve, process, unprocess
from display import BeloteWindow, WelcomeFrame, GameFrame



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.234.175.153"
        self.port = 5555
        self.addr = (self.server, self.port)

        self.w = BeloteWindow(self.applyer)
        w = self.w.frames[GameFrame]
        self.fonctions_display = {
            "launch_gme": lambda n, c: self.w.launch_gme(),
        #   "dsp_pseudo": w.dsp_pseudo,
            "dsp_room"  : lambda n, c: w.dsp_room(*n),
            "act_pun_tg": lambda n, c: w.actualiser_puntos_tg((n[0]+(self.p)%2)%2, n[1]),
            "cpuntos_tg": lambda n, c: w.clear_puntos_tg(),
            "dspbut_une": lambda n, c: w.display_but_une(*n),
            "dspbutdeux": lambda n, c: w.display_but_deux(n),
            "clr_atbuts": lambda n, c: w.clear_at_butts(),
            "dsp_single": lambda n, c: w.display_single(c[0]),
            "clr_single": lambda n, c: w.clear_single(),
            "dsp_main"  : lambda n, c: w.display_ma_main(*n, c),
            "act_main"  : lambda n, c: w.activate_ma_main(c),
            "clear_main": lambda n, c: w.clear_ma_main(),
            "add_to_mid": lambda n, c: w.add_to_mid((n[0]-self.p)%4, n[1], c[0]),
            "clear_mid" : lambda n, c: w.clear_mid(),
            "set_atout" : lambda n, c: w.set_atout(*n),
        }


    def applyer(self, f, ns=[], cs=[]):
        if f == 'connect':
            return self.connect
        else: # fonctions à send
            l_data = process(f, ns, cs)
            self.send_c(l_data)


    def send_c(self, l_data):
        send(self.client, l_data)


    def recieve_c(self):
        return recieve(self.client)

    
    def connect(self, need_new_game, pseudo, room=""): # nng==1 => room==""
        try:
            self.client.connect(self.addr)
            self.send_c([need_new_game, pseudo, room])
            self.p = int(self.recieve_c()[0])
            start_new_thread(self.recv_n_redirect, ())
        except:
            print("====ecxcept 1 (network.py)")


    def recv_n_redirect(self): 
        while True:
            l_data = self.recieve_c()
            print("rnr", l_data)
            if l_data[0] == "dsp_pseudo":
                pseudo = l_data[2]
                j = int(l_data[1])
                self.w.current_frame.dsp_pseudo((j-self.p)%4, pseudo)
            else:
                f, r_ns, r_cs = unprocess(l_data)
                self.fonctions_display[f](r_ns, r_cs)



if __name__ == '__main__':
    n = Network()

    n.w.mainloop()
