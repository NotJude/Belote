class UserAction:
    def __init__(self, sender):
        self.sender = sender

class PlayCard(UserAction):
    def __init__(self, sender, card):
        UserAction.__init__(self, sender)
        self.card = card