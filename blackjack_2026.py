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

    def value(self):
        total_value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank == 'A':
                num_aces += 1
            total_value += CARD_RANK_VALUES[card.rank]
        for _ in range(num_aces):
            if total_value + 10 <= 21:
                total_value += 10
        return total_value

    def bust(self):
        return self.value() > 21

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

    def deal_one(self):
        if len(self.shoe) <= self.shoe_cut_card_position:
            self.drew_cut_card = True
        if len(self.shoe) == 0:
            # Special case: Put discard into shoe, shuffle, then deal
            self.shoe.extend(self.discard)
            random.shuffle(self.shoe)
        return self.shoe.pop()

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


def main():
    clear_screen()
    print("Welcome to Blackjack!")
    players = []
    num_players = get_num_players()

    for player_num in range(1, num_players+1):
        player_name = get_player_name(player_num)
        players.append(Player(player_num, player_name, PLAYER_STARTING_BANK))
        print(f"Welcome, {player_name}!")

    dealer = Dealer(NUM_SHOE_DECKS, SHOE_CUT_CARD_POSITION)

    # Print rules
    print("-------------------------- HOUSE RULES --------------------------\n"
          f"All players start with ${PLAYER_STARTING_BANK}.\n"
          f"Dealer must hit on soft 17.\n"
          f"Shoe contains {NUM_SHOE_DECKS} decks.\n"
          f"Shoe is reshuffled when less than {SHOE_CUT_CARD_POSITION} cards "
          "remain in the shoe.")


if __name__ == '__main__':
    main()
