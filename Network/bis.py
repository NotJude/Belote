

class Partie:
    def __init__(self, mg):
        self.mg = mg
        self.send("a", 0)
        # self.send("a", 2)

    def send(self, c, n):
        self.mg.send(c, n)