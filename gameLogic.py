import random
from player import Player

class FiveUpFiveDown:
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.deck = self.createDeck()
        self.players = [Player(i) for i in range(numPlayers)]
        self.playPile = []  
        self.currentCard = None  
        self.maxTurns = 250 
        self.turnCount = 0  
        self.dealCards()

    def createDeck(self):
        suits = ['♠', '♥', '♦', '♣']  
        ranks = list(range(2, 15))  
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def dealCards(self):
        for player in self.players:
            player.faceDownCards = [self.deck.pop() for _ in range(5)]  
            player.faceUpCards = [self.deck.pop() for _ in range(5)]    
            player.hand = [self.deck.pop() for _ in range(5)]             

    def flipStartCard(self):
        if self.deck:
            self.currentCard = self.deck.pop()
            print(f"Starting card: {self.cardToStr(self.currentCard)}")

    def isValidPlay(self, card, player):
        if player.pickedUpPile:
            return True
        return card[0] >= self.currentCard[0] or card[0] in {2, 10}

    def pickUpPile(self, player):
        if self.playPile:
            print(f"{player.getName()} picks up the pile!")
            player.hand.extend(self.playPile)
            self.playPile.clear()
            player.pickedUpPile = True
            print(f"The current card is reset. {player.getName()} can start a new pile.")
        else:
            print("The pile is empty; nothing to pick up!")

    def shufflePile(self):
        if self.playPile:
            print("Shuffling the play pile back into the deck, including the current card.")
            self.playPile.extend(self.currentCard)  
            random.shuffle(self.playPile)  
            self.deck.extend(self.playPile)
            self.playPile.clear()  
            random.shuffle(self.deck)  
        print("The current card has been reset. A new pile will start.") 
    
    def cardToStr(self, card):
        rankNames = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}
        return f"{rankNames.get(card[0], str(card[0]))} of {card[1]}"

    def handleSpecialCards(self, card, player):
        if card[0] == 2:
            print(f"{player.getName()} played a 2! Resetting the play pile count.")
            self.currentCard = (2, card[1])  
        elif card[0] == 10:
            print(f"{player.getName()} played a 10! Shuffling the play pile and including the 10 in the shuffle.")
            self.shufflePile()

    def playCard(self, player, card, fromWhere):
        if fromWhere == "hand":
            currentPlayCollection = player.hand
        elif fromWhere == "face up":
            currentPlayCollection = player.faceUpCards
        elif fromWhere == "face down":
            currentPlayCollection = player.faceDownCards
        currentPlayCollection.remove(card)
        self.playPile.append(card)
        print(f"{player.getName()} plays {self.cardToStr(card)}.")
        if card[0] == 10 or card[0] == 2:
            self.handleSpecialCards(card, player)
        else:
            self.currentCard = card  
            player.pickedUpPile = False

    def attemptInvalidPlay(self, player, attemptedCard,playFromWhere):
        if playFromWhere == "hand":
            currentPlayCollection = player.hand
        if playFromWhere == "face up":
            currentPlayCollection = player.faceUpCards
        if playFromWhere == "face down":
            currentPlayCollection = player.faceDownCards

        print(f"{player.getName()} attempts to play {self.cardToStr(attemptedCard)}.")
        currentPlayCollection.remove(attemptedCard)
        self.playPile.append(attemptedCard)
        if len(self.deck) < 1:
            print("No cards left in the deck to flip!")
            self.pickUpPile(player)
        else:
            flippedCard = self.deck.pop()
            print(f"Flipped card: {self.cardToStr(flippedCard)}.")

            if flippedCard[0] >= self.currentCard[0] or flippedCard[0] in {2, 10}:
                self.currentCard = flippedCard
                print(f"{player.getName()} avoids picking up the pile! {self.cardToStr(self.currentCard)} is now the current card.")
            else:
                print(f"{player.getName()} fails to beat the pile and must pick it up.")
                self.playPile.append(flippedCard)  
                self.pickUpPile(player)
                self.promptPlayerCard(player)

    def promptPlayerCard(self, player):
        if player.getName() == "Player 2":  
            self.computerPlay(player)
        else:  
            print(f"\n{player.getName()}'s turn:")
            if player.pickedUpPile:
                print("You are starting a new pile. Choose a card to play.")
            else:
                print(f"Current card to beat: {self.cardToStr(self.currentCard)}")
            playFromWhere = self.checkWhereCardsArePlayed(player)
            if playFromWhere == "hand":
                currentPlayCollection = player.hand
            elif playFromWhere == "face up":
                currentPlayCollection = player.faceUpCards
            elif playFromWhere == "face down":
                currentPlayCollection = player.faceDownCards
            sortedCards = enumerate(currentPlayCollection, 1)
            if playFromWhere == "face down":
                print(f"Your {playFromWhere} cards are hidden, choose one at random!")
                for i in range(len(player.faceDownCards)):
                    print(f"{i+1}.", end="\t")
            else:
                print(f"Your {playFromWhere} cards:")
                for i, (originalIndex, card) in enumerate(sortedCards, 1):
                    print(f"{originalIndex}. {self.cardToStr(card):<15}", end="\t")
                    if i % 5 == 0:  
                        print()
                print()  
            while True:
                try:
                    choice = int(input("Choose a card to play: ")) - 1
                    selectedCard = currentPlayCollection[choice]
                    if player.pickedUpPile:
                        self.playCard(player, selectedCard, playFromWhere)  
                        player.pickedUpPile = False  
                    elif self.isValidPlay(selectedCard, player):
                        self.playCard(player, selectedCard, playFromWhere)
                        player.pickedUpPile = False  
                    else:
                        self.attemptInvalidPlay(player, selectedCard, playFromWhere)
                        player.pickedUpPile = False  
                    break
                except (ValueError, IndexError):
                    print("Invalid input. Please try again.")

    def checkWhereCardsArePlayed(self,player):
        if len(player.hand) <= 0:
            if len(player.faceUpCards) <=0:
                return "face down"
            else:
                return "face up"
        else:
            return "hand"

    def computerPlay(self, player):
        print(f"\n{player.getName()}'s turn:")
        if player.pickedUpPile == False:
            print(f"Card to beat {self.cardToStr(self.currentCard)}")
        playFrom = self.checkWhereCardsArePlayed(player)
        if playFrom == "hand":
            validCards = [card for card in player.hand if self.isValidPlay(card, player)]
        elif playFrom == "face up":
            validCards = [card for card in player.faceUpCards if self.isValidPlay(card,player)]
        elif playFrom == "face down":
            validCards = [card for card in player.faceDownCards if self.isValidPlay(card,player)]
        if validCards:
            selectedCard = validCards[0]
            self.playCard(player, selectedCard,playFrom)
        else:
            if playFrom == "hand":
                selectedCard = player.hand[0]
            elif playFrom == "face up":
                selectedCard = player.faceUpCards[0]
            elif playFrom == "face down":
                selectedCard = player.faceDownCards[0]
            self.attemptInvalidPlay(player, selectedCard,playFrom)
        
    def playGame(self):
        self.flipStartCard()
        while self.turnCount < self.maxTurns:
            for player in self.players:
                if player.pickedUpPile:
                    self.promptPlayerCard(player)
                    player.pickedUpPile = False  
                else:
                    self.promptPlayerCard(player)
                if len(player.hand) == 0 and len(player.faceUpCards) == 0 and len(player.faceDownCards) == 0:  
                    print(f"{player.getName()} wins!")
                    return
                print(f"End of {player.getName()}'s turn. Current card to beat: {self.cardToStr(self.currentCard)}")
            self.turnCount += 1
        print("Game over! Turn limit reached, Draw!")

if __name__ == "__main__":
    game = FiveUpFiveDown(2)  
    game.playGame()
