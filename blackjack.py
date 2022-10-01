'''
Blackjack Game
By Chris Leung
'''
import random

suits = ('♥', '♦', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
          '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}

class Card:
    ''' Represents a single card in a standard deck of cards '''
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + self.suit

class Deck:
    ''' Represents one or more standard 52-card decks '''
    def __init__(self,num_decks):
        self.deck = []
        for _ in range(0,num_decks):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_string = f"{len(self.deck)} cards in total.\n"
        for card in self.deck:
            deck_string += card.__str__() + '\n'
        return deck_string

    def shuffle(self):
        ''' Shuffles the deck randomly in place '''
        random.shuffle(self.deck)

class Player:
    ''' Represents a human player in a blackjack game '''
    def __init__(self,name,money):
        self.name = name
        self.money = money
        self.current_bet = 0
        self.hand = []

def play_again():
    '''
    Gets input from user: Whether player wants to continue playing
    Returns: True to continue playing, False otherwise
    '''
    choice = ''
    while choice not in ('Y', 'N'):
        choice = input("Would you like to play again? (Y/N): ").capitalize()
    return choice == 'Y'

def get_positive_integer_input(prompt):
    '''
    Gets input from user: Loops until a positive non-zero integer is input by the user
    Returns: Positive non-zero integer
    '''
    while True:
        choice = input(prompt)
        if choice.isdigit() and int(choice) > 0:
            return int(choice)

def get_player_details(player_number):
    '''
    Gets input from user: Name and starting money amount
    Returns: Tuple of (str, int) for (name, money)
    '''
    name = input(f"Player {player_number}, enter your name: ")
    money = get_positive_integer_input(f"{name}, enter your starting money: ")
    return (name,money)

def has_money_to_play(players):
    '''
    Returns True if any of the players still has money > 0
    '''
    for player in players:
        if player.money != 0:
            return True
    return False

def main():
    '''
    The main game logic.
    '''
    while True:
        # Game setup
        dealer = Player('Dealer', 0)
        players = []

        # Player(s) setup
        num_players = get_positive_integer_input("Enter number of players: ")
        for player_num in range(1,num_players+1):
            (name, money) = get_player_details(player_num)
            players.append(Player(name,money))

        # Deck(s) setup
        num_decks = get_positive_integer_input("Enter number of decks: ")
        deck = Deck(num_decks)
        deck.shuffle()
        print(deck)

        game_on = True

        while game_on:
            # Print players and amounts

            # Deal to all players
            # Show dealer's 2nd card
            # For each player

            if not has_money_to_play(players):
                game_on = False

        # Ask to continue playing or not
        if not play_again():
            break

if __name__ == '__main__':
    main()
