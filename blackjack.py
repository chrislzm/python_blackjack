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
        self.value = values[rank]

    def face(self):
        ''' Returns the card face as a string '''
        return self.rank + self.suit

class Deck:
    ''' Represents one or more standard 52-card decks '''
    def __init__(self,num_decks):
        self.deck = []
        self.discard = []
        for _ in range(0,num_decks):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_string = f"{len(self.deck)} cards in total.\n"
        for card in self.deck:
            deck_string += card.face() + '\n'
        return deck_string

    def shuffle(self):
        ''' Shuffles the deck randomly in place '''
        random.shuffle(self.deck)

    def deal_card(self):
        '''
        Returns one card from the deck.
        If deck is empty, add back cards from discard pile, shuffle, then deal.
        '''
        if len(self.deck) == 0:
            print("Deck is out of cards. Adding back the discard pile and shuffling.")
            self.deck = self.discard
            self.discard = []
            random.shuffle(self.deck)
        return self.deck.pop()

class Player:
    ''' Represents a human player in a blackjack game '''
    def __init__(self,name,money):
        self.name = name
        self.money = money
        self.bet = 0
        self.hand = []

    def name_and_money(self):
        ''' Returns a string with the player's name and money to gamble '''
        return f"{self.name} has ${self.money} to bet"

    def name_and_hand(self):
        ''' Returns a string with the player's name, cards and value '''
        output_string = f"{self.name}:"
        for card in self.hand:
            output_string += ' ' + card.face()
        hand_value = self.max_hand_value()
        output_string += ", Total: " + str(hand_value) if hand_value <= 21 else ' **BUST**'
        return output_string

    def max_hand_value(self):
        ''' Returns maximum integer value of hand '''
        hand_value = 0
        num_aces = 0
        for card in self.hand:
            if card.rank == 'A':
                num_aces += 1
            else:
                hand_value += card.value
        hand_value += num_aces
        for _ in range(0,num_aces):
            if hand_value + 10 <= 21:
                hand_value += 10
        return hand_value

def get_valid_string_input(prompt, valid_strings):
    '''
    Gets an input and validates it. Case insensitive.
    Returns the lowercase version of the string chosen.
    '''
    lowercase_valid_strings = []
    for string in valid_strings:
        lowercase_valid_strings.append(string.lower())        
    choice = ''
    while choice not in lowercase_valid_strings:
        choice = input(prompt).lower()
    return choice

def get_positive_integer_input(prompt, maximum = 0):
    '''
    Gets input from user: Loops until a positive non-zero integer is input by the user.
    Optional maximum must be positive, will continue to ask user for input if beyond maximum.
    Returns: Positive non-zero integer
    '''
    while True:
        choice = input(prompt)
        if choice.isdigit():
            value = int(choice)
            if value > 0 and (maximum == 0 or (maximum > 0 and value <= maximum)):
                return value

def get_player_move(player_name):
    return get_valid_string_input(f"{player_name} - Hit or stay? (H/S): ",('h','s','q'))

def get_player_details(player_number):
    '''
    Gets input from user: Name and starting money amount
    Returns: Tuple of (str, int) for (name, money)
    '''
    name = input(f"Player {player_number}, enter your name: ")
    money = get_positive_integer_input(f"{name}, enter your starting money: ")
    return (name,money)

def play_again():
    '''
    Gets input from user: Whether player wants to continue playing
    Returns: True to continue playing, False otherwise
    '''
    choice = get_valid_string_input("Would you like to play again? (Y/N): ",('y','n'))
    return choice == 'y'

def has_money_to_play(players):
    '''
    Returns True if any of the players still has money > 0
    '''
    for player in players:
        if player.money != 0:
            return True
    return False

def display_table(dealer,players):
    '''
    Prints the entire table, with all hands
    '''
    dealer_face_up_card = dealer.hand[1]
    print(f"Dealer: " + dealer_face_up_card.face())
    for player in players:
        print(player.name_and_hand())

def display_line():
    '''
    Prints a dashed line
    '''
    print("----------------------------------------------------------------------")

def get_move():
    '''
    Gets the move from the player.
    H = hit, S = stay, Q = quit
    '''

def main():
    '''
    The main game logic.
    '''

    print("\n" * 100) # Clear screen

    while True:
        # Game setup
        dealer = Player('Dealer', 0)
        all_players = []

        # Player(s) setup
        num_players = get_positive_integer_input("Enter number of players: ")
        for player_num in range(1,num_players+1):
            (name, money) = get_player_details(player_num)
            all_players.append(Player(name,money))

        # Deck(s) setup
        num_decks = get_positive_integer_input("Enter number of decks: ")
        deck = Deck(num_decks)
        deck.shuffle()

        dealer_hit_value = 16

        print(f"Rules: Dealer must hit on or below {dealer_hit_value}.")

        # Start the main game loop
        game_on = True

        while game_on:

            display_line()

            active_players = []

            # Print players and amounts
            for player in all_players:
                print(player.name_and_money())
                if player.money != 0:
                    active_players.append(player)
                    player.bet = get_positive_integer_input(f"{player.name}, enter your bet: ",player.money)
                    player.money -= player.bet

            if len(active_players) == 0:
                break

            # Deal
            for _ in range(0,2):
                for player in active_players:
                    player.hand.append(deck.deal_card())
                dealer.hand.append(deck.deal_card())

            display_line()

            # Human player turns
            for player in active_players:
                display_table(dealer,active_players)
                while player.max_hand_value() < 21:
                    move = get_player_move(player.name)
                    if move == 'q':
                        game_on = False
                        break
                    if move == 's':
                        break
                    # Player has chosen to hit
                    player.hand.append(deck.deal_card())
                    print(player.name_and_hand())
            
            # Dealer turn
            print(dealer.name_and_hand())
            while dealer.max_hand_value() <= dealer_hit_value:
                print("Dealer hits")
                dealer.hand.append(deck.deal_card())
                print(dealer.name_and_hand())

            # Dealer busts, 
            if dealer.max_hand_value() > 21:
                # Pay 2x to everyone who didn't bust
                for player in active_players:
                    if player.max_hand_value() <= 21:
                        player.money += 2*player.bet
                        print(f"{player.name} wins ${player.bet}! They now have ${player.money}")
                    else:
                        print(f"{player.name} lost ${player.bet}. They now have ${player.money}")
                    player.bet = 0
                
            else:
                # Otherwise, check each player's hand against dealers
                for player in active_players:
                    if player.max_hand_value() > 21 or player.max_hand_value() < dealer.max_hand_value():
                        print(f"{player.name} lost ${player.bet}. They now have ${player.money}")
                    elif player.max_hand_value() == dealer.max_hand_value():
                        player.money += player.bet
                        print(f"{player.name} draw, keeps ${player.bet}. They now have ${player.money}")
                    else:
                        player.money += 2* player.bet
                        print(f"{player.name} wins ${player.bet}! They now have ${player.money}")
                    player.bet = 0

            # Move cards to the discard pile
            for player in active_players:
                deck.discard.extend(player.hand)
                player.hand = []
            deck.discard.extend(dealer.hand)
            dealer.hand = []

        # Ask to continue playing or not
        if not play_again():
            break

if __name__ == '__main__':
    main()
