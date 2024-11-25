class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.hand = []  
        self.faceDownCards = []  
        self.faceUpCards = []  
        self.pickedUpPile = False  

    def getName(self):
        return f"Player {self.id + 1}"