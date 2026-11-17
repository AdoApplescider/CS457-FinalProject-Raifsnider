import unittest

from src.models.player import Player
from src.models.card import Card

class TestPlayer(unittest.TestCase):
    def test_constructor(self):
        player = Player(1)
        self.assertEqual(player.id, 1)
        self.assertEqual(len(player), 7)

    def test_invalid_id_too_low(self):
        with self.assertRaises(ValueError):
            Player(0)

    def test_invalid_id_too_high(self):
        with self.assertRaises(ValueError):
            Player(5)

    def test_invalid_id_type(self):
        with self.assertRaises(TypeError):
            Player("1")

    def test_discard(self):
        player = Player(1)

        original_size = len(player)
        discarded_card = player.discard(0)

        self.assertIsInstance(discarded_card, Card)
        self.assertEqual(len(player), original_size - 1)