
"""
server : 
playerIDCount is useless
ajouter joueur dans helper
"""


import socket
from _thread import start_new_thread

from manageGame import ManageGame, N_alpha


games = {}




def threaded_game(conns, gameID): # to recieve data from game
    mg = games[gameID]
    mg.set_conns(conns)
    mg.start_game()




def start_server():
    server = "192.168.0.26"
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        print("Erreur detecteee, server")
        str(e)

    
    playerIDCount = 0 # players count
    gameIDCount = 0
    need_new_game = True
    conn_lst = [None]*N_alpha

    s.listen()
    print("Waiting for a connection, Server Started")


    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        def helper(c, n): # c : texte, n : num du joueur
            conn_lst[n].send(str.encode(c))

        if need_new_game:
            games[gameIDCount] = ManageGame()
            games[gameIDCount].set_sender_func(helper)
            need_new_game = False

        g = games[gameIDCount]
        n = g.add_player()

        conn_lst[n] = conn
        playerIDCount += 1
        
        
        conn.send(str.encode(str(n)))


        if g.is_ready():
            # print("C'estmiantenan")
            start_new_thread(threaded_game, (conn_lst, gameIDCount))
            gameIDCount += 1
            need_new_game = True





if __name__ == '__main__':
    start_server()