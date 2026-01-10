'''
Unit tests for blackjack_2026.py
By Chris Leung
January 9, 2026
'''

import unittest
from blackjack_2026 import Card
from blackjack_2026 import Hand


class TestBlackjack2026(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
