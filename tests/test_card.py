import unittest

from src.models.card import Card, CardType, Color

class TestCard(unittest.TestCase):
    def test_construction_normal(self):
        card = Card(Color.RED, CardType.EIGHT)
        self.assertEqual(card.color, Color.RED)
        self.assertEqual(card.type, CardType.EIGHT)

    def test_can_play_on_matchingcolor(self):
        card = Card(Color.RED, CardType.EIGHT)
        result = card.can_play_on(Color.RED, CardType.ZERO)
        self.assertEqual(result, True)

    def test_can_play_on_matchingtype(self):
        card = Card(Color.YELLOW, CardType.TWO)
        result = card.can_play_on(Color.BLUE, CardType.TWO)
        self.assertEqual(result, True)

    def test_can_play_on_wildcard(self):
        card = Card(Color.WILD, CardType.WILD)
        result = card.can_play_on(Color.BLUE, CardType.SEVEN)
        self.assertEqual(result, True)

    def test_can_play_on_nonmatchingtype(self):
        card = Card(Color.YELLOW, CardType.THREE)
        result = card.can_play_on(Color.BLUE, CardType.TWO)
        self.assertEqual(result, False)

if __name__ == "__main__":
    unittest.main()