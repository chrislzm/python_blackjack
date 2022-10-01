'''
Blackjack Game
By Chris Leung
'''
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}

def play_again():
    choice = ''
    while choice not in ('Y', 'N'):
        choice = input("Would you like to play again? (Y/N): ").capitalize()
    return choice == 'Y'

def get_num_players():
    choice = ''
    while not choice.isdigit():
        choice = input("How many players? ")
    return int(choice)

def get_player_details(player_number):
    name = input(f"Player {player_number}, enter your name: ")
    money = 0
    while True:
        choice = input(f"{name}, enter your starting money: ")
        if choice.isdigit() and int(choice) > 0:
            money = int(choice)
            return (name,money)

def has_money_to_play(players):
    for player in players:
        if player.money != 0:
            return True
    return False

class Card:
    pass

class Deck:
    pass

class Hand:
    # List of cards
    # Value
    pass

class Player:
    def __init__(self,name,money):
        self.name = name
        self.money = money
        self.current_bet = 0
        self.hand = []

while True:
    # Game setup
    dealer = Player('Dealer', 0)
    players = []

    # Ask for the number of players
    num_players = get_num_players()
    for player_num in range(1,num_players+1):
        (name, money) = get_player_details(player_num)
        players.append(Player(name,money))

    # Ask for the starting amount of money
    # Ask for the number of decks

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
