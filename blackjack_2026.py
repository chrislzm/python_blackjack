'''
Blackjack: Milestone 2 Project for "The Complete Python Bootcamp"
Author: Chris Leung
January 9, 2026
'''

import random

CARD_SUITS = ('Hearts', 'Clubs', 'Diamonds', 'Spades')
CARD_SUIT_SYMBOLS = {'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦',
                     'Spades': '♠'}
CARD_RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
CARD_RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                    '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 1}
PLAYER_STARTING_BANK = 500
MINIMUM_BET = 15
NUM_SHOE_DECKS = 6
SHOE_CUT_CARD_POSITION = 52  # Reshuffle when one deck remains in the shoe
SCREEN_WIDTH = 80


class Card():

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_up = False

    def __str__(self):
        if self.face_up:
            return f"[{self.rank}{CARD_SUIT_SYMBOLS[self.suit]}]"
        else:
            return "[  ]"


class Deck():

    def __init__(self):
        self.cards = []
        for suit in CARD_SUITS:
            for rank in CARD_RANKS:
                new_card = Card(rank, suit)
                self.cards.append(new_card)


class Hand():

    def __init__(self):
        self.cards = []
        self.soft = False

    def value(self):
        total_value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank == 'A':
                num_aces += 1
            total_value += CARD_RANK_VALUES[card.rank]
        self.soft = False
        for _ in range(num_aces):
            if total_value + 10 <= 21:
                total_value += 10
                self.soft = True
        return total_value

    def bust(self):
        return self.value() > 21

    def is_blackjack(self):
        return self.value() == 21

    def is_hard_17(self):
        return self.value() == 17 and not self.soft

    def __str__(self):
        string_output = ""
        for card in self.cards:
            string_output += f"{card} "
        return string_output


class Dealer():

    def __init__(self, num_shoe_decks, shoe_cut_card_position):
        self.hand = Hand()
        self.shoe = []
        self.discard = []
        self.shoe_cut_card_position = shoe_cut_card_position
        self.drew_cut_card = False

        # Fill shoe and shuffle
        for _ in range(num_shoe_decks):
            deck = Deck()
            self.shoe.extend(deck.cards)
        random.shuffle(self.shoe)

    def deal_one(self, face_up):
        if len(self.shoe) <= self.shoe_cut_card_position:
            self.drew_cut_card = True
        if len(self.shoe) == 0:
            # Special case: Put discard into shoe, shuffle, then deal
            self.shoe.extend(self.discard)
            random.shuffle(self.shoe)
        dealt_card = self.shoe.pop()
        dealt_card.face_up = face_up
        return dealt_card

    def reshuffle_shoe_if_needed(self):
        if self.drew_cut_card:
            self.shoe.extend(self.discard)
            self.discard.clear()
            random.shuffle(self.shoe)
            self.drew_cut_card = False


class Player():

    def __init__(self, number, name, bank):
        self.number = number
        self.name = name
        self.bank = bank
        self.bet = 0
        self.hand = Hand()

    def __str__(self):
        return f"Player {self.number} ({self.name})"


def clear_screen() -> None:
    """
    Clears the display to a blank screen.
    """
    print('\n'*100)


def get_num_players() -> int:
    while True:
        try:
            num_players = int(input("Please enter number of players: "))
        except ValueError:
            print("Sorry, that's not a valid input.")
        else:
            if num_players > 0:
                return num_players
            print("Please enter a number greater than 0.")


def get_player_name(player_num) -> str:
    while True:
        player_name = input(f"Player {player_num} - Please enter your name: ")
        if len(player_name) > 0:
            return player_name


def get_player_bet(player, minimum_bet) -> None:
    while True:
        try:
            bet = int(input(f"{player} has ${player.bank}. Your bet: "))
        except ValueError:
            print("Sorry, that's not a valid input.")
        else:
            if bet >= minimum_bet:
                if bet > player.bank:
                    print("Sorry, that's more than you have in your bank.")
                else:
                    player.bet = bet
                    player.bank -= bet
                    print(f"{player.name} bets ${bet}")
                    return
            else:
                print(f"Bet must be at least ${minimum_bet}.")


def hit(player) -> bool:
    while True:
        response = input(f"Hit or Stay? (h/s): ")
        if response.lower() == 'h':
            return True
        elif response.lower() == 's':
            return False
        else:
            print("Please enter 'h' or 's'.")


def print_header(message) -> None:
    padding_amount = int((SCREEN_WIDTH - len(message)) / 2) - 2
    for _ in range(padding_amount):
        print("-", end="")
    print(" ", end="")
    print(message, end="")
    print(" ", end="")
    for _ in range(padding_amount):
        print("-", end="")
    print("")


def main():
    clear_screen()
    print_header("Welcome to Blackjack!")
    players = []
    num_players = get_num_players()

    for player_num in range(1, num_players+1):
        player_name = get_player_name(player_num)
        players.append(Player(player_num, player_name, PLAYER_STARTING_BANK))
        print(f"Welcome, {player_name}!")

    dealer = Dealer(NUM_SHOE_DECKS, SHOE_CUT_CARD_POSITION)

    # Print rules
    print_header("HOUSE RULES")
    print(f"All players start with ${PLAYER_STARTING_BANK}.\n"
          f"Dealer must hit on soft 17.\n"
          f"Shoe contains {NUM_SHOE_DECKS} decks.\n"
          f"Shoe is reshuffled when less than {SHOE_CUT_CARD_POSITION} cards "
          "remain in the shoe.\n"
          f"Minimum bet is ${MINIMUM_BET}.\n"
          f"Blackjack pays 3:2.")

    game_on = True

    while game_on:
        print_header("Place your bets")
        for player in players:
            get_player_bet(player, MINIMUM_BET)

        print_header("Dealer")
        print("Dealing cards...")

        # Deal first card
        dealer.hand.cards.append(dealer.deal_one(False))
        for player in players:
            player.hand.cards.append(dealer.deal_one(True))

        # Deal second card
        dealer.hand.cards.append(dealer.deal_one(True))
        for player in players:
            player.hand.cards.append(dealer.deal_one(True))

        # Announce cards
        print(f"Dealer shows: {dealer.hand}")
        for player in players:
            print(f"{player} shows: {player.hand}")

        if dealer.hand.is_blackjack():
            dealer.hand.cards[0].face_up = True
            print(f"Dealer Blackjack! Dealer shows: {dealer.hand}")
        else:
            for player in players:
                print_header(f"{player}")
                if player.hand.is_blackjack():
                    print(f"Hand: {player.hand} - Blackjack! ")
                    win_amount = player.bet * 1.5
                    player.bank += win_amount + player.bet
                    player.bet = 0
                    print(f"You win ${win_amount} and now have "
                          f"${player.bank}")
                else:
                    stay = False
                    while not stay:
                        print(player.hand)
                        if hit(player):
                            player.hand.cards.append(dealer.deal_one(True))
                            if player.hand.bust():
                                print(player.hand)
                                print(f"Bust! You lose your bet of ${player.bet}.")
                                player.bet = 0
                                stay = True
                            if player.hand.is_blackjack():
                                print(player.hand)
                                print(f"Twenty one!")
                                stay = True
                        else:
                            stay = True

            print_header("Dealer")
            dealer.hand.cards[0].face_up = True
            print(dealer.hand)
            while dealer.hand.value() <= 17 and not dealer.hand.is_hard_17():
                print("Dealer hits.")
                dealer.hand.cards.append(dealer.deal_one(True))
                print(dealer.hand)
            if dealer.hand.bust():
                print("Dealer busted!")
            else:
                print("Dealer stays.")

        print_header("Resolving bets")
        for player in players:
            if player.bet == 0:
                continue
            if dealer.hand.bust() or player.hand.value() > dealer.hand.value():
                player.bank += player.bet * 2
                print(f"{player} hand {player.hand}wins ${player.bet} "
                      f"and now has ${player.bank}")
                player.bet = 0
            elif dealer.hand.value() == player.hand.value():
                player.bank += player.bet
                print(f"{player} hand {player.hand}is a push, ${player.bet} "
                      f"is returned and they now have ${player.bank}.")
                player.bet = 0
            elif dealer.hand.value() > player.hand.value():
                print(f"{player} hand {player.hand}loses to dealer's hand and "
                      f"they lose their ${player.bet} bet. "
                      f"They now have ${player.bank}.")
                player.bet = 0

        # Round end - Cleanup
        while len(dealer.hand.cards) != 0:
            dealer.discard.append(dealer.hand.cards.pop())
        bankrupt_players = []
        for player in players:
            while len(player.hand.cards) != 0:
                dealer.discard.append(player.hand.cards.pop())
            if player.bank < MINIMUM_BET:
                bankrupt_players.append(player.number)
                print(f"{player} only has ${player.bank} which is less than "
                      f"the minimum bet of ${MINIMUM_BET}. They are being "
                      f"removed from the table.")
        while len(bankrupt_players) != 0:
            # Remove players moving backwards, with 0-based index
            players.pop(bankrupt_players[-1]-1)
            bankrupt_players.pop(-1)

        if len(players) == 0:
            print_header("Game Over")
            print("There are no more eligible players. Have a nice day!")
            game_on = False
        # Option to end the game
            # Print stats (bank)
        # If cards left in shoe < cut card, then add discard pile and reshuffle


if __name__ == '__main__':
    main()
