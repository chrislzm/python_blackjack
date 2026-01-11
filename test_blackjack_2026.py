'''
Unit tests for blackjack_2026.py
By Chris Leung
January 9, 2026
'''

import unittest
from blackjack_2026 import Card
from blackjack_2026 import Hand
from blackjack_2026 import Dealer

class TestBlackjack2026(unittest.TestCase):

    '''
    String tests
    '''

    def test_card_str(self):
        card = Card("2", "Spades")
        self.assertEqual(str(card), "[  ]")
        card.face_up = True
        self.assertEqual(str(card), "[2♠]")

    def test_hand_str(self):
        hand = Hand()
        hand.cards.append(Card('10', 'Spades'))
        hand.cards.append(Card('10', 'Hearts'))
        hand.cards.append(Card('3', 'Clubs'))
        self.assertEqual(str(hand), "[  ] [  ] [  ] ")
        hand.cards[1].face_up = True
        hand.cards[2].face_up = True
        self.assertEqual(str(hand), "[  ] [10♥] [3♣] ")

    '''
    Hand Value tests
    '''

    def test_hand_value_and_bust_false(self):
        hand = Hand()
        hand.cards.append(Card('10', 'Spades'))
        hand.cards.append(Card('5', 'Diamonds'))
        self.assertEqual(hand.value(), 15)
        self.assertEqual(hand.bust(), False)

    def test_hand_value_and_bust_true(self):
        hand = Hand()
        hand.cards.append(Card('10', 'Spades'))
        hand.cards.append(Card('10', 'Hearts'))
        hand.cards.append(Card('3', 'Clubs'))
        self.assertEqual(hand.value(), 23)
        self.assertEqual(hand.bust(), True)

    def test_hand_value_one_ace(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('10', 'Hearts'))
        self.assertEqual(hand.value(), 21)
        self.assertEqual(hand.bust(), False)

    def test_hand_value_multiple_aces(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('A', 'Diamonds'))
        hand.cards.append(Card('A', 'Clubs'))
        hand.cards.append(Card('5', 'Hearts'))
        self.assertEqual(hand.value(), 18)
        self.assertEqual(hand.bust(), False)

    '''
    Dealer tests
    '''

    def test_deal_one(self):
        dealer = Dealer(2, 52)
        self.assertIsInstance(dealer.deal_one(), Card)

    def test_reshuffle_flag(self):
        dealer = Dealer(2, 52)
        self.assertFalse(dealer.drew_cut_card)
        for _ in range(60):
            dealer.deal_one()
        self.assertTrue(dealer.drew_cut_card)

    def test_empty_shoe_special_case(self):
        dealer = Dealer(1, 52)
        for _ in range(52):
            dealer.discard.append(dealer.deal_one())
        self.assertEqual(len(dealer.shoe), 0)
        dealer.deal_one()
        self.assertEqual(len(dealer.shoe), 51)


if __name__ == '__main__':
    unittest.main()
