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
PLAYER_BANK_START = 500
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
