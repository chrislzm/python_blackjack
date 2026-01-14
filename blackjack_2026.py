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

    def value(self) -> int:
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

    def is_bust(self) -> bool:
        return self.value() > 21

    def is_blackjack(self) -> bool:
        return self.value() == 21

    def is_hard_17(self) -> bool:
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

    def deal_one(self, face_up) -> Card:
        if len(self.shoe) <= self.shoe_cut_card_position:
            self.drew_cut_card = True
        if len(self.shoe) == 0:
            # Special case: Put discard into shoe, shuffle, then deal
            self.shoe.extend(self.discard)
            random.shuffle(self.shoe)
        dealt_card = self.shoe.pop()
        dealt_card.face_up = face_up
        return dealt_card

    def reveal_blackjack(self) -> None:
        self.hand.cards[0].face_up = True
        print(f"Dealer Blackjack! Dealer shows: {self.hand}")

    def reshuffle_shoe_if_needed(self) -> None:
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


def setup_players(num_players: int, starting_bank: int) -> list[Player]:
    '''
    Sets up each player object. Gets player names (via input) and prints a
    message to welcome them.
    '''
    players = []
    for player_num in range(1, num_players+1):
        while True:
            player_name = input(f"Player {player_num} - "
                                f"Please enter your name: ")
            if len(player_name) > 0:
                break
        players.append(Player(player_num, player_name, starting_bank))
        print(f"Welcome, {player_name}!")
    return players


def get_player_bets(players: list[Player], minimum_bet: int) -> None:
    print_header("Place your bets!")
    for player in players:
        placed_bet = False
        while not placed_bet:
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
                        placed_bet = True
                else:
                    print(f"Bet must be at least ${minimum_bet}.")


def hit(player: Player) -> bool:
    while True:
        response = input(f"Hit or Stay? (h/s): ")
        if response.lower() == 'h':
            return True
        elif response.lower() == 's':
            return False
        else:
            print("Please enter 'h' or 's'.")


def print_header(message: str) -> None:
    printed_chars = 0
    padding_amount = int((SCREEN_WIDTH - len(message)) / 2) - 2
    for _ in range(padding_amount):
        print("-", end="")
        printed_chars += 1

    print(f" {message} ", end="")
    printed_chars += len(message) + 2

    for _ in range(padding_amount):
        print("-", end="")
        printed_chars += 1

    # Fill any remaining available space
    for _ in range(SCREEN_WIDTH-printed_chars):
        print("-", end="")

    print("")  # Line break


def print_game_rules() -> None:
    print_header("HOUSE RULES")
    print(f"All players start with {PLAYER_STARTING_BANK}.\n"
          f"Dealer must hit on soft 17.\n"
          f"Shoe contains {NUM_SHOE_DECKS} decks.\n"
          f"Shoe is reshuffled when less than {SHOE_CUT_CARD_POSITION} cards "
          "remain in the shoe.\n"
          f"Minimum bet is ${MINIMUM_BET}.\n"
          f"Blackjack pays 3:2.")


def print_final_stats(players: list[Player],
                      player_starting_bank: int) -> None:
    for player in players:
        won_or_lost = "Won" if player.bank >= player_starting_bank else "Lost"
        print(f"{player} - Leaves with ${player.bank} - "
              f"{won_or_lost} ${abs(player_starting_bank-player.bank)}")


def play_player_rounds(players: list[Player], dealer: Dealer) -> None:
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
                    if player.hand.is_bust():
                        print(player.hand)
                        print("Bust! You lost your bet of "
                              f"${player.bet}.")
                        player.bet = 0
                        stay = True
                    if player.hand.is_blackjack():
                        print(player.hand)
                        print(f"Twenty one!")
                        stay = True
                else:
                    stay = True


def resolve_player_bets(players: list[Player], dealer: Dealer) -> None:
    print_header("Resolving bets")
    for player in players:
        if player.bet == 0:
            continue
        if (dealer.hand.is_bust() or
                player.hand.value() > dealer.hand.value()):
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


def play_dealer_round(dealer: Dealer) -> None:
    print_header("Dealer")
    dealer.hand.cards[0].face_up = True
    print(dealer.hand)
    while dealer.hand.value() <= 17 and not dealer.hand.is_hard_17():
        print("Dealer hits.")
        dealer.hand.cards.append(dealer.deal_one(True))
        print(dealer.hand)
    if dealer.hand.is_bust():
        print("Dealer busted!")
    else:
        print("Dealer stays.")


def discard_cards(players: Player, dealer: Dealer) -> None:
    while len(dealer.hand.cards) != 0:
        dealer.discard.append(dealer.hand.cards.pop())
    for player in players:
        while len(player.hand.cards) != 0:
            dealer.discard.append(player.hand.cards.pop())


def remove_bankrupt_players(players: list[Player], minimum_bet: int):
    bankrupt_players = []
    for player in players:
        if player.bank < minimum_bet:
            bankrupt_players.append(player.number)
            print(f"{player} only has ${player.bank} which is less than "
                  f"the minimum bet of ${minimum_bet}. They are being "
                  f"removed from the table.")
    while len(bankrupt_players) != 0:
        # Remove players moving backwards, with 0-based index, since removing
        # them in forwards order would change the order
        players.pop(bankrupt_players[-1]-1)
        bankrupt_players.pop(-1)


def deal_first_two_cards(players: list[Player], dealer: Dealer) -> None:

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


def should_game_on(players: list[Player]) -> bool:
    if len(players) == 0:
        print("There are no more eligible players.")
        return False
    else:
        while True:
            response = input(f"Play another round? (y/n): ")
            if response.lower() == 'y':
                return True
            elif response.lower() == 'n':
                return False
            else:
                print("Please enter 'y' or 'n'.")


def main():
    clear_screen()
    print_header("Welcome to Blackjack!")

    num_players = get_num_players()
    active_players = setup_players(num_players, PLAYER_STARTING_BANK)
    all_players = active_players.copy()

    dealer = Dealer(NUM_SHOE_DECKS, SHOE_CUT_CARD_POSITION)

    print_game_rules()

    game_on = True

    while game_on:
        get_player_bets(active_players, MINIMUM_BET)

        deal_first_two_cards(active_players, dealer)

        if dealer.hand.is_blackjack():
            dealer.reveal_blackjack()
        else:
            play_player_rounds(active_players, dealer)
            play_dealer_round(dealer)

        resolve_player_bets(active_players, dealer)

        discard_cards(active_players, dealer)

        remove_bankrupt_players(active_players, MINIMUM_BET)

        if should_game_on(active_players):
            dealer.reshuffle_shoe_if_needed()
        else:
            game_on = False

    print_header("Game over")
    print_final_stats(all_players, PLAYER_STARTING_BANK)
    print_header("Have a nice day! :)")


if __name__ == '__main__':
    main()
