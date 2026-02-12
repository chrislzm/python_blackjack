'''
Blackjack: Milestone 2 Project for "The Complete Python Bootcamp"
Author: Chris Leung

Future improvements:
* Refactor into MVC implementation to separate game state from UI and logic
* Use enums for suits/ranks
* Support dollar amounts < $1
* Expand unit test coverage

'''

import os
import random
from dataclasses import dataclass, field

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
MAX_SPLITS = 4
SCREEN_WIDTH = 80


@dataclass
class Card:
    '''
    Represents a single card in a standard 52-card deck.
    '''

    rank: str
    suit: str
    face_up: bool = False

    def __str__(self):
        if self.face_up:
            return f"[{self.rank}{CARD_SUIT_SYMBOLS[self.suit]}]"
        return "[  ]"

    def value(self) -> int:
        '''
        Returns the numberic value of the Blackjack card based on the
        CARD_RANK_VALUES dictionary.
        '''
        return CARD_RANK_VALUES[self.rank]


@dataclass
class Deck:
    '''
    Represents a standard 52-card deck.
    '''
    cards: list[Card] = field(default_factory=list)

    def __post_init__(self):
        for suit in CARD_SUITS:
            for rank in CARD_RANKS:
                new_card = Card(rank, suit)
                self.cards.append(new_card)


class Hand:
    '''
    Represents a hand in Blackjack.
    '''

    def __init__(self):
        self.bet: int = 0
        self.cards: list[Card] = []

    def _evaluate(self) -> tuple[int, bool]:
        '''
        Evalutes the numeric value of the Blackjack hand (maximizing the value
        of any aces) and returns a tuple of that value and a boolean that
        indicates whether the hand is soft (e.g. includes an ace valued at 11)
        or hard (e.g. any aces are valued at 1).
        '''
        total_value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank == 'A':
                num_aces += 1
            total_value += card.value()
        is_soft = False
        for _ in range(num_aces):
            if total_value + 10 <= 21:
                total_value += 10
                is_soft = True
        return (total_value, is_soft)

    def value(self) -> int:
        '''
        Returns the numeric value of the Blackjack hand
        '''
        return self._evaluate()[0]

    def is_soft(self) -> bool:
        '''
        Returns a boolean indicating whether the hand is soft.
        '''
        return self._evaluate()[1]

    def is_bust(self) -> bool:
        '''
        Returns True if the hand is a bust.
        '''
        return self.value() > 21

    def is_blackjack(self) -> bool:
        '''
        Returns True if the hand is a blackjack.
        '''
        return len(self.cards) == 2 and self.value() == 21

    def __str__(self):
        return " ".join(str(card) for card in self.cards)


class Dealer:
    '''
    Represents a dealer in a game of Blackjack.
    '''

    def __init__(self, num_shoe_decks: int, shoe_cut_card_position: int):
        self.hand: Hand = Hand()
        self.shoe: list[Card] = []
        self.discard: list[Card] = []
        self.shoe_cut_card_position: int = shoe_cut_card_position
        self.drew_cut_card: bool = False

        # Fill shoe and shuffle
        for _ in range(num_shoe_decks):
            deck = Deck()
            self.shoe.extend(deck.cards)
        random.shuffle(self.shoe)

    def deal_one(self, face_up: bool = False) -> Card:
        '''
        Deals one card from the shoe and returns it. Tracks whether the shoe
        should be reshuffled using the attributes 'shoe_cut_card_position' and
        'drew_cut_card'.
        '''
        if len(self.shoe) <= self.shoe_cut_card_position:
            self.drew_cut_card = True
        if len(self.shoe) == 0:
            # Special case: Put discard into shoe, shuffle, then deal
            self.shoe.extend(self.discard)
            random.shuffle(self.shoe)
            self.discard.clear()
        dealt_card = self.shoe.pop()
        dealt_card.face_up = face_up
        return dealt_card

    def reveal_blackjack(self) -> None:
        '''
        Reveals and announces dealer blackjack.
        '''
        if self.hand.is_blackjack():
            self.hand.cards[0].face_up = True
            print(f"Dealer Blackjack! Dealer shows: {self.hand}")

    def reshuffle_shoe_if_needed(self) -> None:
        '''
        Reshuffles the entire shoe (adding cards from the discard pile) if the
        cut card has been reached.
        '''
        if self.drew_cut_card:
            self.shoe.extend(self.discard)
            self.discard.clear()
            random.shuffle(self.shoe)
            self.drew_cut_card = False


@dataclass
class Player:
    '''
    Represents a player in a game of Blackjack.
    '''
    number: int
    name: str
    bank: int
    hands: list[Hand] = field(default_factory=list)

    def __str__(self):
        return f"Player {self.number} ({self.name})"


def get_num_players() -> int:
    '''
    Requests number of players from the user and returns it as an int.
    '''
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
    Sets up each Player object. Requests player names and prints a message to
    welcome them.
    '''
    players = []
    for player_num in range(1, num_players+1):
        while True:
            player_name = input(f"Player {player_num} - "
                                "Please enter your name: ")
            if len(player_name) > 0:
                break
        players.append(Player(player_num, player_name, starting_bank))
        print(f"Welcome, {player_name}!")
    return players


def get_player_bets(players: list[Player], minimum_bet: int) -> None:
    '''
    Requests the initial bet for each player.
    '''
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
                        initial_hand = Hand()
                        initial_hand.bet = bet
                        player.hands.append(initial_hand)
                        player.bank -= bet
                        print(f"{player.name} bets ${bet}")
                        placed_bet = True
                else:
                    print(f"Bet must be at least ${minimum_bet}.")


def hit_stay_split_or_dd(offer_double_down: bool, offer_split: bool) -> str:
    '''
    Requests that a user hit, stay, split or double down and performs input
    validation until a valid input is received.
    '''
    if offer_split:
        while True:
            response = input(
                "Hit, Stay, Split, or Double Down? (h/s/p/d): ").lower()
            if response in ('h', 's', 'p', 'd'):
                return response
            print("Please enter 'h', 's', 'p' or 'd'.")
    elif offer_double_down:
        while True:
            response = input("Hit, Stay, or Double Down? (h/s/d): ").lower()
            if response in ('h', 's', 'd'):
                return response
            print("Please enter 'h', 's' or 'd'.")
    else:
        while True:
            response = input("Hit or Stay? (h/s): ").lower()
            if response in ('h', 's'):
                return response
            print("Please enter 'h' or 's'.")


def print_header(message: object) -> None:
    '''
    Prints a message center aligned and padded by dashes. Fills the width of
    the screen defined by the global SCREEN_WIDTH.
    '''
    print(f" {message} ".center(SCREEN_WIDTH, "-"))


def print_game_rules() -> None:
    '''
    Prints all the rules of the Blackjack game to the screen.
    '''
    print_header("HOUSE RULES")
    print(f"All players start with {PLAYER_STARTING_BANK}.\n"
          "Dealer must hit on soft 17.\n"
          f"Shoe contains {NUM_SHOE_DECKS} decks.\n"
          f"Shoe is reshuffled when less than {SHOE_CUT_CARD_POSITION} cards "
          "remain in the shoe.\n"
          f"Minimum bet is ${MINIMUM_BET}.\n"
          f"Player can split their hand a maximum of {MAX_SPLITS} times.\n"
          "Blackjack pays 3:2.")


def print_final_stats(players: list[Player],
                      player_starting_bank: int) -> None:
    '''
    Prints final stats for all players to the screen.
    '''
    for player in players:
        won_or_lost = "Won" if player.bank >= player_starting_bank else "Lost"
        print(f"{player} - Leaves with ${player.bank} - "
              f"{won_or_lost} ${abs(player_starting_bank-player.bank)}")


def payout_any_player_blackjacks(players: list[Player]) -> None:
    '''
    Announces and immediately pays out any blackjacks, just like in a real
    casino!
    '''
    for player in players:
        initial_hand = player.hands[0]
        if initial_hand.is_blackjack():
            print_header(player)
            print(f"Hand: {initial_hand} - Blackjack! ")
            win_amount = initial_hand.bet * 3 // 2
            player.bank += win_amount + initial_hand.bet
            initial_hand.bet = 0
            print(f"You win ${win_amount} and now have "
                  f"${player.bank}")


def print_hand(player_name: str,
               hand: Hand,
               num_hands: int,
               current_hand_index: int) -> None:
    '''
    Helper function to print the hand -- includes hand number only if there are
    multiple hands (due to a split), otherwise just print the hand.
    '''
    if num_hands == 1:
        print(f"{player_name}: {hand}")
    else:
        print(f"{player_name} Hand {current_hand_index+1}: {hand}")


def play_player_rounds(players: list[Player], dealer: Dealer) -> None:
    '''
    Plays each player's hand (for players with an active bet, e.g. > 0),
    requesting hit/stay. Automatically handles busts and 21s.
    '''
    for player in players:
        initial_bet = player.hands[0].bet
        if initial_bet > 0:
            print_header(player)
            num_hands = 1
            current_hand_index = 0
            print(f"Dealer: {dealer.hand}")
            while current_hand_index < num_hands:
                stay = False
                first_turn = True
                hand = player.hands[current_hand_index]
                print_hand(player.name, hand, num_hands, current_hand_index)
                while not stay:
                    offer_double_down = (first_turn and
                                         player.bank >= hand.bet)
                    offer_split = (len(hand.cards) == 2 and
                                   (hand.cards[0].value() ==
                                    hand.cards[1].value()) and
                                   player.bank >= hand.bet and
                                   num_hands < MAX_SPLITS)

                    # Automatically hit if we have split
                    if len(hand.cards) == 1:
                        response = 'auto_hit_split'
                    else:
                        response = hit_stay_split_or_dd(offer_double_down,
                                                        offer_split)

                    if response == 's':  # Stay
                        stay = True
                        continue

                    # Any other response means we deal one card to the hand

                    if response == 'd':  # Double down
                        player.bank -= hand.bet
                        hand.bet *= 2
                        print(f"Doubling down: Increasing bet to ${hand.bet}")
                        stay = True

                    if response == 'p':  # Split
                        split_hand = Hand()
                        split_hand.cards.append(hand.cards.pop())
                        split_hand.bet = hand.bet
                        player.bank -= hand.bet
                        player.hands.append(split_hand)
                        num_hands += 1
                        print_hand(player.name,
                                   hand,
                                   num_hands,
                                   current_hand_index)

                    # Hit and handle the outcome
                    hand.cards.append(dealer.deal_one(True))
                    print_hand(player.name,
                               hand,
                               num_hands,
                               current_hand_index)
                    if hand.is_bust():
                        print(f"Bust! You lost your bet of ${hand.bet} and "
                              f"have ${player.bank} remaining.")
                        hand.bet = 0
                        stay = True
                    elif hand.value() == 21:
                        print("Twenty one!")
                        stay = True

                    if response in ('h', 'd'):  # Hit or double down
                        # Leave True when we are splitting so they have the
                        # option to double down
                        first_turn = False

                    if (response in ('p', 'auto_hit_split')
                            and hand.cards[0].rank == 'A'):
                        # Split aces are only allowed one card
                        stay = True

                current_hand_index += 1


def resolve_player_bets(players: list[Player], dealer: Dealer) -> None:
    '''
    Resolves each player's bet by evaluating their hand against the dealer's
    hand and taking the appropriate action regarding their bet.
    '''
    print_header("Resolving bets")
    for player in players:
        for hand in player.hands:
            if hand.is_bust() or hand.bet == 0:
                continue
            if (dealer.hand.is_bust() or
                    hand.value() > dealer.hand.value()):
                player.bank += hand.bet * 2
                print(f"{player} hand {hand} wins ${hand.bet} "
                      f"and now has ${player.bank}")
            elif dealer.hand.value() == hand.value():
                player.bank += hand.bet
                print(f"{player} hand {hand} is a push, ${hand.bet} "
                      f"is returned and they now have ${player.bank}.")
            elif dealer.hand.value() > hand.value():
                print(f"{player} hand {hand} loses to dealer's hand and "
                      f"they lose their ${hand.bet} bet. "
                      f"They now have ${player.bank}.")


def play_dealer_round(dealer: Dealer) -> None:
    '''
    Plays the dealer's hand.
    '''
    print_header("Dealer")
    dealer.hand.cards[0].face_up = True
    print(dealer.hand)
    while (dealer.hand.value() < 17 or
           (dealer.hand.value() == 17 and dealer.hand.is_soft())):
        print("Dealer hits.")
        dealer.hand.cards.append(dealer.deal_one(True))
        print(dealer.hand)
    if dealer.hand.is_bust():
        print("Dealer busted!")
    else:
        print("Dealer stays.")


def discard_cards(players: list[Player], dealer: Dealer) -> None:
    '''
    Moves cards from dealer and player hands to the discard pile. Used at the
    end of a round.
    '''
    dealer.discard.extend(dealer.hand.cards)
    dealer.hand.cards.clear()
    for player in players:
        for hand in player.hands:
            dealer.discard.extend(hand.cards)
        player.hands.clear()


def remove_bankrupt_players(players: list[Player], minimum_bet: int) -> None:
    '''
    Remove players from the player list who cannot meet the minimum bet.
    '''
    for player in players[:]:
        if player.bank < minimum_bet:
            players.remove(player)
            print(f"{player} only has ${player.bank} which is less than the "
                  f"minimum bet of ${minimum_bet}. They are removed from the "
                  "table.")


def deal_first_two_cards(players: list[Player], dealer: Dealer) -> None:
    '''
    Deals the first two cards to the dealer and players. The first dealer card
    is face down, all other cards are face up. Prints the results.
    '''
    print_header("Dealer")
    print("Dealing cards...")

    # Deal first card
    dealer.hand.cards.append(dealer.deal_one(False))
    for player in players:
        player.hands[0].cards.append(dealer.deal_one(True))

    # Deal second card
    dealer.hand.cards.append(dealer.deal_one(True))
    for player in players:
        player.hands[0].cards.append(dealer.deal_one(True))

    # Announce cards
    print(f"Dealer shows: {dealer.hand}")
    for player in players:
        print(f"{player} shows: {player.hands[0]}")


def should_game_on(players: list[Player]) -> bool:
    '''
    Decides whether the game should continue and returns True (continue) or
    False (end game).
    '''
    if len(players) == 0:
        print("There are no more eligible players.")
        return False

    while True:
        response = input("Play another round? (y/n): ")
        if response.lower() == 'y':
            return True
        if response.lower() == 'n':
            return False
        print("Please enter 'y' or 'n'.")


def main():
    '''
    The Blackjack game.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    print_header("Welcome to Blackjack!")

    num_players = get_num_players()
    active_players = setup_players(num_players, PLAYER_STARTING_BANK)
    all_players = active_players[:]

    dealer = Dealer(NUM_SHOE_DECKS, SHOE_CUT_CARD_POSITION)

    print_game_rules()

    game_on = True

    while game_on:
        get_player_bets(active_players, MINIMUM_BET)

        deal_first_two_cards(active_players, dealer)

        if dealer.hand.is_blackjack():
            dealer.reveal_blackjack()
        else:
            payout_any_player_blackjacks(active_players)
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
