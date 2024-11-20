import random

class FiveUpFiveDown:
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = self.create_deck()
        self.players = [Player(i) for i in range(num_players)]
        self.play_pile = []  # The current play pile
        self.current_card = None  # The card that the players need to beat or match
        self.max_turns = 100  # Maximum number of turns to avoid infinite loops
        self.turn_count = 0  # Counter for the number of turns played
        self.deal_cards()

    def create_deck(self):
        suits = ['♠', '♥', '♦', '♣']  # Spades, Hearts, Diamonds, Clubs
        ranks = list(range(2, 15))  # 2 to Ace (14)
        
        # Generate a full deck: Each card is a tuple of (rank, suit)
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        for player in self.players:
            player.face_down_cards = [self.deck.pop() for _ in range(5)]  # Face-down cards
            player.face_up_cards = [self.deck.pop() for _ in range(5)]    # Face-up cards
            player.hand = [self.deck.pop() for _ in range(5)]             # Cards in hand

    def flip_start_card(self):
        self.current_card = self.deck.pop()  # Flip the first card from the deck to start the play pile

    def is_valid_play(self, card):
        return card[0] >= self.current_card[0]

    def prompt_player_for_card(self, player):
        print(f"\n{player.get_name()}'s turn:")
        print(f"Current card to beat: {self.card_to_str(self.current_card)}")

        if player.picked_up_pile:
            print("\nYou have picked up the pile! You can now choose any card from your hand to set as the new card to beat.")
            print("\nChoose any card from your hand to set as the new card to beat:")
            for i, card in enumerate(player.hand, 1):
                print(f"{i}. {self.card_to_str(card)}")

            while True:
                try:
                    choice = int(input("Enter the number of the card you want to play: ")) - 1
                    if choice < 0 or choice >= len(player.hand):
                        raise ValueError("Invalid option. Try again.")
                    
                    selected_card = player.hand[choice]
                    player.hand.remove(selected_card)  # Remove selected card from hand
                    self.play_pile.append(selected_card)  # Add to play pile
                    self.current_card = selected_card  # Set as the new current card to beat
                    print(f"You have set {self.card_to_str(selected_card)} as the new card to beat.")
                    player.picked_up_pile = False  # Reset the flag after playing
                    break
                except ValueError as e:
                    print(f"Invalid input. {e}. Please enter a valid option.")
        else:
            if player.get_name() == "Player 2":  # If it is the computer's turn
                self.computer_play(player)
            else:
                self.user_play(player)

    def computer_play(self, player):
        # Computer's turn logic
        valid_cards = [card for card in player.hand if self.is_valid_play(card)]

        if not valid_cards:
            # If no valid cards, the computer must play an invalid card and flip a card
            print(f"{player.get_name()} has no valid cards to play. They play a card and flip from the deck.")
            
            # Choose any card from the computer's hand (in this case, we just pick the first card)
            selected_card = player.hand[0]
            player.hand.remove(selected_card)  # Remove the selected card from the hand
            print(f"{player.get_name()} plays {self.card_to_str(selected_card)}.")

            # Now flip a card from the deck
            flipped_card = self.deck.pop()
            print(f"The flipped card is: {self.card_to_str(flipped_card)}")

            # Compare the flipped card to the current card
            if flipped_card[0] >= self.current_card[0]:
                # If the flipped card beats the current card, it becomes the new card to beat
                self.current_card = flipped_card
                self.play_pile.append(flipped_card)  # Add the flipped card to the play pile
                print(f"The flipped card {self.card_to_str(flipped_card)} beats the current card.")
            else:
                # If the flipped card does not beat the current card, the computer picks up the pile
                print(f"The flipped card {self.card_to_str(flipped_card)} does not beat the current card.")
                print(f"{player.get_name()} picks up the play pile!")  # The computer picks up the entire pile
                self.pick_up_pile(player)  # The computer picks up all cards in the pile

                # After picking up the pile, the computer now plays a card from its larger hand
                print(f"{player.get_name()}, you now have the following cards in your hand:")
                for i, card in enumerate(player.hand, 1):
                    print(f"{i}. {self.card_to_str(card)}")

                # Prompt the computer to play a card from the new hand
                self.computer_pick_and_play(player)  # New helper method to play the next card
            return

        # If the computer has valid cards, it will play the first valid card
        selected_card = valid_cards[0]
        player.hand.remove(selected_card)
        self.play_pile.append(selected_card)

        print(f"{player.get_name()} plays {self.card_to_str(selected_card)}.")

        # Handle special card effects (e.g., 2s or 10s)
        self.handle_card_effect(selected_card, player)

        # Update the current card to beat
        self.current_card = selected_card

    def computer_pick_and_play(self, player):
        # Helper method for the computer to play a card after picking up the pile
        # The computer selects a card from its (larger) hand to set as the new card to beat
        print(f"{player.get_name()} must now play a card as the new card to beat.")

        while True:
            # Select the first card from the hand (for simplicity, we can just play the first card)
            selected_card = player.hand[0]  # In a more advanced version, we'd have smarter logic here
            player.hand.remove(selected_card)  # Remove it from the hand
            self.play_pile.append(selected_card)  # Add to the play pile

            print(f"{player.get_name()} plays {self.card_to_str(selected_card)} as the new card to beat.")
            self.current_card = selected_card  # Set the new card to beat
            break  # Exit after playing the card


    def user_play(self, player):
        valid_cards = [card for card in player.hand if self.is_valid_play(card)]

        print("\nYour hand options (valid cards and special cards are marked):")
        for i, card in enumerate(player.hand, 1):
            status = "(VALID)" if card in valid_cards else "(INVALID)"
            if card[0] == 10:
                status = "(10 - SHUFFLE PILE)"
            elif card[0] == 2:
                status = "(2 - RESET)"
            print(f"{i}. {self.card_to_str(card)} {status}")

        if not valid_cards:
            print(f"{player.get_name()} has no valid cards to play. You must play a card, and a flip will occur.")
            self.handle_invalid_play(player)
            return

        while True:
            try:
                choice = int(input("Enter the number of the card you want to play: ")) - 1
                if choice < 0 or choice >= len(player.hand):
                    raise ValueError("Invalid option. Try again.")
                
                selected_card = player.hand[choice]
                if selected_card not in valid_cards:
                    flipped_card = self.deck.pop()
                    print(f"Invalid card played! Flipping a card from the deck: {self.card_to_str(flipped_card)}")

                    if flipped_card[0] >= self.current_card[0]:
                        self.current_card = flipped_card  # New card to beat
                        print(f"The flipped card {self.card_to_str(flipped_card)} beats the current card.")
                        break
                    else:
                        print(f"The flipped card {self.card_to_str(flipped_card)} does not beat the current card.")
                        print(f"{player.get_name()} picks up the play pile!")
                        self.pick_up_pile(player)  # Handle picking up the pile
                        return

                    self.play_pile.append(flipped_card)
                    return

                else:
                    break
            except ValueError as e:
                print(f"Invalid input. {e}. Please enter a valid option.")
        
        player.hand.remove(selected_card)
        print(f"{player.get_name()} plays {self.card_to_str(selected_card)}.")
        self.handle_card_effect(selected_card, player)
        self.current_card = selected_card

    def handle_invalid_play(self, player):
        while True:
            try:
                # Prompt the player to choose a card to play that will trigger a flip
                choice = int(input("Enter the number of the card you want to play (this will trigger a flip): ")) - 1
                if choice < 0 or choice >= len(player.hand):
                    raise ValueError("Invalid option. Try again.")

                selected_card = player.hand[choice]
                print(f"You played {self.card_to_str(selected_card)}. A card will be flipped.")
                flipped_card = self.deck.pop()

                print(f"The flipped card is: {self.card_to_str(flipped_card)}")

                # If the flipped card beats the current card, update the current card to beat
                if flipped_card[0] >= self.current_card[0]:
                    print(f"The flipped card {self.card_to_str(flipped_card)} beats the current card.")
                    self.current_card = flipped_card  # Set the flipped card as the new card to beat
                    self.play_pile.append(flipped_card)  # Add the flipped card to the play pile
                    break  # Valid play, move to the next player's turn
                else:
                    print(f"The flipped card {self.card_to_str(flipped_card)} does not beat the current card.")
                    print(f"{player.get_name()} picks up the play pile!")  # The player picks up the pile
                    self.pick_up_pile(player)  # The player picks up all cards in the pile

                    # Now allow the player to immediately play a card from their hand
                    print(f"\n{player.get_name()}, you now have the following cards in your hand:")
                    for i, card in enumerate(player.hand, 1):
                        print(f"{i}. {self.card_to_str(card)}")

                    # Prompt the player to choose a card to play
                    while True:
                        try:
                            play_choice = int(input(f"Choose a card from your hand to play: ")) - 1
                            if play_choice < 0 or play_choice >= len(player.hand):
                                raise ValueError("Invalid option. Try again.")

                            selected_card = player.hand[play_choice]
                            player.hand.remove(selected_card)
                            self.play_pile.append(selected_card)

                            # Set the new card to beat
                            self.current_card = selected_card
                            print(f"{player.get_name()} plays {self.card_to_str(selected_card)} as the new card to beat.")
                            break  # Player has played a card, so exit the loop

                        except ValueError as e:
                            print(f"Invalid input. {e}. Please try again.")

                    return  # This return prevents the other player from getting a turn until this player is done

            except ValueError as e:
                print(f"Invalid input. {e}. Please try again.")




    def handle_card_effect(self, card, player):
        if card[0] == 2:
            print(f"{player.get_name()} played a 2! A new card will be played to reset the card to beat.")
            self.reset_card_to_beat()
        elif card[0] == 10:
            print(f"{player.get_name()} played a 10! The play pile will be shuffled.")
            self.shuffle_pile()

    def reset_card_to_beat(self):
        if self.deck:
            self.current_card = self.deck.pop()
            print(f"New card to beat: {self.card_to_str(self.current_card)}")

    def shuffle_pile(self):
        random.shuffle(self.play_pile)
        self.deck.extend(self.play_pile)
        self.play_pile.clear()
        print("The play pile has been shuffled and added back to the deck.")

    def card_to_str(self, card):
        rank_names = {
            2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
            10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"
        }
        return f"{rank_names.get(card[0], str(card[0]))} of {card[1]}"

    def pick_up_pile(self, player):
        # This function handles the case when a player picks up the pile
        # Add all the cards from the play pile to the player's hand
        player.hand.extend(self.play_pile)  # Add all cards from the play pile to the player's hand
        self.play_pile.clear()  # Clear the play pile after it's been picked up
        print(f"{player.get_name()} has picked up the pile and now has {len(player.hand)} cards in their hand.")


    def play_game(self):
        self.flip_start_card()
        while self.turn_count < self.max_turns:
            for player in self.players:
                if player.get_name() == "Player 2":  # Computer's turn
                    self.prompt_player_for_card(player)
                else:  # Player 1's turn
                    self.prompt_player_for_card(player)

                if len(player.hand) == 0:  # Check if any player has no cards left
                    print(f"{player.get_name()} wins!")
                    return
                self.turn_count += 1

        print("Game over! No one won after 100 turns.")


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.hand = []  # Hidden cards in hand
        self.face_up_cards = []  # Cards face up, visible to others
        self.face_down_cards = []  # Cards face down, hidden
        self.picked_up_pile = False  # Flag to track if player picked up the pile

    def get_name(self):
        return f"Player {self.id + 1}"

    def __repr__(self):
        return f"Player({self.id})"

# Run the game with 2 players (one human and one computer-controlled)
game = FiveUpFiveDown(2)
game.play_game()

