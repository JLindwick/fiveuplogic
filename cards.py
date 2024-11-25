import pygame
import sys
from gameLogic import FiveUpFiveDown
from player import Player

pygame.init()

screenWidth, screenHeight = 800, 600
white, black, red, green = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)
bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Five Up, Five Down")
clock = pygame.time.Clock()
fps = 30

font = pygame.font.SysFont("arial", 24)
cardWidth, cardHeight = 70, 100

def drawCard(card, x, y):
    suitColors = {"♠": black, "♣": black, "♥": red, "♦": red}
    pygame.draw.rect(screen, white, (x, y, cardWidth, cardHeight), border_radius=5)
    rank, suit = card
    if rank == 11:
        rank = "J"
    elif rank == 12:
        rank = "Q"
    elif rank == 13:
        rank = "K"
    elif rank == 14:
        rank = "A"
    text = font.render(f"{rank}{suit}", True, suitColors[suit])
    screen.blit(text, (x + 5, y + 5))

def drawPlayerHand(player, yDistanceOffset):
    x = 50
    for card in player.hand:
        drawCard(card, x, screenHeight - yDistanceOffset)
        x += 80

def drawPile(playPile, currentCard):
    x, y = screenWidth // 2 - cardWidth // 2, screenHeight // 2 - cardHeight // 2

    if playPile:
        drawCard(playPile[-1], x, y)
    elif currentCard:
        drawCard(currentCard, x, y)
    else:
        pygame.draw.rect(screen, black, (x, y, cardWidth, cardHeight), border_radius=5)
        text = font.render("Pile", True, white)
        screen.blit(text, (x + 10, y + 35))

def getCollection(player, playFrom):
    if playFrom == "hand":
        return player.hand
    if playFrom == "face up":
        return player.faceUpCards
    if playFrom == "face down":
        return player.faceDownCards

def handlePlayerActions(game, player):
    while True:
        playFrom = game.checkWhereCardsArePlayed(player)
        currentCardCollection = getCollection(player, playFrom)
        validCards = [card for card in currentCardCollection if game.isValidPlay(card, player)]
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for i, card in enumerate(currentCardCollection):
                    cardRect = pygame.Rect(50 + i * 80, screenHeight - 150, cardWidth, cardHeight)
                    if cardRect.collidepoint(mousePos):
                        if card in validCards:
                            game.playCard(player, card, playFrom)
                            return
                        else:
                            game.attemptInvalidPlay(player, card, playFrom)
                            break  
        for i, card in enumerate(currentCardCollection):
            x, y = 50 + i * 80, screenHeight - 150
            color = green if card in validCards else red
            pygame.draw.rect(screen, color, (x - 2, y - 2, cardWidth + 4, cardHeight + 4), 2)
            drawCard(card, x, y)
        drawPile(game.playPile, game.currentCard)
        pygame.display.flip()
        clock.tick(fps)


# Main game loop
def main():
    game = FiveUpFiveDown(2)
    game.flipStartCard()
    while True:
        screen.fill(black)
        screen.blit(bg, (0, 0))
        for player in game.players:
            if len(player.hand) == 0 and len(player.faceUpCards) == 0 and len(player.faceDownCards) == 0:
                print(f"{player.getName()} wins!")
                pygame.quit()
                sys.exit()
            if player.getName() == "Player 2":
                game.computerPlay(player)
            else:
                handlePlayerActions(game, player)
        drawPlayerHand(game.players[0], 150)
        drawPile(game.playPile, game.currentCard)
        pygame.display.flip()
        clock.tick(fps)
if __name__ == "__main__":
    main()
