'''
Unit tests for blackjack_2026.py
By Chris Leung
January 9, 2026
'''

import unittest
from blackjack_2026 import Card
from blackjack_2026 import Deck
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
        self.assertEqual(str(hand), "[  ] [  ] [  ]")
        hand.cards[1].face_up = True
        hand.cards[2].face_up = True
        self.assertEqual(str(hand), "[  ] [10♥] [3♣]")

    '''
    Card Value tests
    '''

    def test_card_value_number(self):
        card = Card('7', 'Hearts')
        self.assertEqual(card.value(), 7)

    def test_card_value_face(self):
        for rank in ('J', 'Q', 'K'):
            card = Card(rank, 'Spades')
            self.assertEqual(card.value(), 10)

    def test_card_value_ace(self):
        card = Card('A', 'Diamonds')
        self.assertEqual(card.value(), 1)

    '''
    Hand Value tests
    '''

    def test_hand_value_empty(self):
        hand = Hand()
        self.assertEqual(hand.value(), 0)

    def test_hand_value_and_bust_false(self):
        hand = Hand()
        hand.cards.append(Card('10', 'Spades'))
        hand.cards.append(Card('5', 'Diamonds'))
        self.assertEqual(hand.value(), 15)
        self.assertEqual(hand.is_bust(), False)

    def test_hand_value_and_bust_true(self):
        hand = Hand()
        hand.cards.append(Card('10', 'Spades'))
        hand.cards.append(Card('10', 'Hearts'))
        hand.cards.append(Card('3', 'Clubs'))
        self.assertEqual(hand.value(), 23)
        self.assertEqual(hand.is_bust(), True)

    def test_hand_value_one_ace(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('10', 'Hearts'))
        self.assertEqual(hand.value(), 21)
        self.assertTrue(hand.is_blackjack())
        self.assertEqual(hand.is_bust(), False)

    def test_hand_value_multiple_aces(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('A', 'Diamonds'))
        hand.cards.append(Card('A', 'Clubs'))
        hand.cards.append(Card('5', 'Hearts'))
        self.assertEqual(hand.value(), 18)
        self.assertFalse(hand.is_blackjack())
        self.assertEqual(hand.is_bust(), False)

    def test_hand_value_two_aces(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('A', 'Hearts'))
        self.assertEqual(hand.value(), 12)

    def test_hand_value_21_not_blackjack(self):
        hand = Hand()
        hand.cards.append(Card('7', 'Spades'))
        hand.cards.append(Card('7', 'Hearts'))
        hand.cards.append(Card('7', 'Clubs'))
        self.assertEqual(hand.value(), 21)
        self.assertFalse(hand.is_blackjack())

    def test_hand_ace_becomes_hard_after_hit(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('5', 'Hearts'))
        self.assertEqual(hand.value(), 16)
        self.assertTrue(hand.is_soft())
        hand.cards.append(Card('K', 'Clubs'))
        self.assertEqual(hand.value(), 16)
        self.assertFalse(hand.is_soft())

    '''
    Hand is_blackjack tests
    '''

    def test_blackjack_two_face_cards_not_blackjack(self):
        hand = Hand()
        hand.cards.append(Card('K', 'Spades'))
        hand.cards.append(Card('Q', 'Hearts'))
        self.assertEqual(hand.value(), 20)
        self.assertFalse(hand.is_blackjack())

    def test_blackjack_single_card_not_blackjack(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        self.assertFalse(hand.is_blackjack())

    '''
    Hand is_soft tests
    '''

    def test_is_soft_ace_and_six(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('6', 'Hearts'))
        self.assertEqual(hand.value(), 17)
        self.assertTrue(hand.is_soft())

    def test_is_hard_ace_six_king(self):
        hand = Hand()
        hand.cards.append(Card('A', 'Spades'))
        hand.cards.append(Card('6', 'Hearts'))
        hand.cards.append(Card('K', 'Clubs'))
        self.assertEqual(hand.value(), 17)
        self.assertFalse(hand.is_soft())

    def test_is_hard_no_aces(self):
        hand = Hand()
        hand.cards.append(Card('10', 'Spades'))
        hand.cards.append(Card('7', 'Hearts'))
        self.assertEqual(hand.value(), 17)
        self.assertFalse(hand.is_soft())

    '''
    Deck tests
    '''

    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_has_all_suits_and_ranks(self):
        deck = Deck()
        suits = set(card.suit for card in deck.cards)
        ranks = set(card.rank for card in deck.cards)
        self.assertEqual(suits, {'Hearts', 'Clubs', 'Diamonds', 'Spades'})
        self.assertEqual(len(ranks), 13)

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

    def test_deal_one_face_up(self):
        dealer = Dealer(1, 52)
        card = dealer.deal_one(True)
        self.assertTrue(card.face_up)

    def test_deal_one_face_down(self):
        dealer = Dealer(1, 52)
        card = dealer.deal_one(False)
        self.assertFalse(card.face_up)

    def test_deal_one_decrements_shoe(self):
        dealer = Dealer(1, 52)
        initial_size = len(dealer.shoe)
        dealer.deal_one()
        self.assertEqual(len(dealer.shoe), initial_size - 1)

    def test_reshuffle_shoe_if_needed(self):
        dealer = Dealer(1, 40)
        self.assertFalse(dealer.drew_cut_card)
        for _ in range(30):
            dealer.discard.append(dealer.deal_one())
        self.assertTrue(dealer.drew_cut_card)
        dealer.reshuffle_shoe_if_needed()
        self.assertEqual(len(dealer.discard), 0)
        self.assertEqual(len(dealer.shoe), 52)
        self.assertFalse(dealer.drew_cut_card)

    def test_reveal_blackjack_flips_hole_card(self):
        dealer = Dealer(1, 52)
        dealer.hand.cards.append(Card('A', 'Spades'))
        dealer.hand.cards.append(Card('K', 'Hearts', face_up=True))
        self.assertFalse(dealer.hand.cards[0].face_up)
        dealer.reveal_blackjack()
        self.assertTrue(dealer.hand.cards[0].face_up)


if __name__ == '__main__':
    unittest.main()
