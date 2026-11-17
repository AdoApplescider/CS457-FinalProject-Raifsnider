import unittest
from unittest.mock import patch

from src.models.game import Game
from src.models.player import Player
from src.models.card import Card, Color, CardType


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.add_player()
        self.game.add_player()

    def start_game(self):
        self.game.start()

    def set_hand(self, player_id, cards):
        self.game.get_player(player_id).hand = cards

    def test_initialization(self):
        game = Game()

        self.assertEqual(len(game.players), 0)
        self.assertEqual(game.active_player, 0)
        self.assertFalse(game.started)
        self.assertFalse(game.finished)


    def test_add_player(self):
        game = Game()

        game.add_player()

        self.assertEqual(len(game.players), 1)
        self.assertEqual(game.players[0].id, 1)


    def test_add_four_players(self):
        game = Game()

        for _ in range(4):
            game.add_player()

        self.assertEqual(len(game.players), 4)


    def test_add_fifth_player(self):
        game = Game()

        for _ in range(4):
            game.add_player()

        with self.assertRaises(ValueError):
            game.add_player()


    def test_remove_player(self):
        game = Game()
        game.add_player()

        removed = game.remove_player()

        self.assertEqual(len(game.players), 0)


    def test_remove_from_empty_game(self):
        game = Game()

        with self.assertRaises(ValueError):
            game.remove_player()


    def test_get_player(self):
        player = self.game.get_player(1)

        self.assertEqual(player.id, 1)


    def test_get_invalid_player(self):
        with self.assertRaises(ValueError):
            self.game.get_player(5)

    def test_start_game(self):
        self.game.start()

        self.assertTrue(self.game.started)
        self.assertEqual(self.game.active_color, Color.WILD)
        self.assertEqual(self.game.active_type, CardType.WILD)


    def test_start_game_with_one_player(self):
        game = Game()
        game.add_player()

        with self.assertRaises(ValueError):
            game.start()


    def test_start_game_twice(self):
        self.game.start()

        with self.assertRaises(RuntimeError):
            self.game.start()


    def test_add_player_after_start(self):
        self.game.start()

        with self.assertRaises(RuntimeError):
            self.game.add_player()


    def test_remove_player_after_start(self):
        self.game.start()

        with self.assertRaises(RuntimeError):
            self.game.remove_player()


    def test_draw_cards(self):
        self.game.start()

        player = self.game.get_player(1)
        original_count = len(player)

        self.game.draw(1, 3)

        self.assertEqual(len(player), original_count + 3)


    def test_draw_invalid_amount(self):
        self.game.start()

        with self.assertRaises(ValueError):
            self.game.draw(1, -1)


    def test_draw_non_integer_amount(self):
        self.game.start()

        with self.assertRaises(TypeError):
            self.game.draw(1, 1.5)


    def test_draw_before_game_starts(self):
        with self.assertRaises(RuntimeError):
            self.game.draw(1)

    def test_advance_turn(self):
        self.game.start()

        self.game.advance_turn()

        self.assertEqual(self.game.active_player, 1)


    def test_advance_turn_wraparound(self):
        for _ in range(2):
            self.game.add_player()

        self.game.start()

        self.game.active_player = 3
        self.game.advance_turn()

        self.assertEqual(self.game.active_player, 0)


    def test_reverse_turn_direction(self):
        self.game.turn_step = -1

        self.game.advance_turn()

        self.assertEqual(self.game.active_player, 1)

    def test_draw_two(self):
        self.game.start()

        player = self.game.get_player(2)
        original_count = len(player)

        self.game.apply_effect(
            Card(Color.RED, CardType.DRAW_TWO)
        )

        self.assertEqual(len(player), original_count + 2)
        self.assertEqual(self.game.active_player, 0)

    def test_wild_draw_four(self):
        self.game.start()

        player = self.game.get_player(2)
        original_count = len(player)

        self.game.apply_effect(
            Card(Color.WILD, CardType.WILD_DRAW_FOUR)
        )

        self.assertEqual(len(player), original_count + 4)
        self.assertEqual(self.game.active_player, 0)

    def test_skip(self):
        self.game.add_player()
        self.game.start()

        self.game.apply_effect(
            Card(Color.RED, CardType.SKIP)
        )

        self.assertEqual(self.game.active_player, 2)

    def test_reverse_two_players(self):
        self.game.start()

        self.game.apply_effect(
            Card(Color.RED, CardType.REVERSE)
        )

        self.assertEqual(self.game.turn_step, -1)
        self.assertEqual(self.game.active_player, 0)

    def test_reverse_three_players(self):
        self.game.add_player()
        self.game.start()

        self.game.apply_effect(
            Card(Color.RED, CardType.REVERSE)
        )

        self.assertEqual(self.game.turn_step, -1)
        self.assertEqual(self.game.active_player, 2)

    def prepare_play(self, card):
        self.game.start()

        player = self.game.get_player(1)
        player.hand = [
            card,
            Card(Color.BLUE, CardType.FIVE)
        ]

        self.game.active_color = Color.RED
        self.game.active_type = CardType.THREE

    def test_play_matching_color(self):
        self.prepare_play(Card(Color.RED, CardType.EIGHT))

        result = self.game.play_card(1, 0)

        self.assertIsNone(result)
        self.assertEqual(len(self.game.get_player(1)), 1)
        self.assertEqual(self.game.active_color, Color.RED)
        self.assertEqual(self.game.active_type, CardType.EIGHT)


    def test_play_matching_type(self):
        self.prepare_play(Card(Color.BLUE, CardType.THREE))

        result = self.game.play_card(1, 0)

        self.assertIsNone(result)
        self.assertEqual(self.game.active_color, Color.BLUE)


    def test_play_nonmatching_card(self):
        self.prepare_play(Card(Color.BLUE, CardType.EIGHT))

        with self.assertRaises(ValueError):
            self.game.play_card(1, 0)


    def test_play_out_of_turn(self):
        self.prepare_play(Card(Color.RED, CardType.EIGHT))

        with self.assertRaises(ValueError):
            self.game.play_card(2, 0)


    def test_play_invalid_card_index(self):
        self.prepare_play(Card(Color.RED, CardType.EIGHT))

        with self.assertRaises(ValueError):
            self.game.play_card(1, 100)


    def test_play_invalid_player(self):
        self.prepare_play(Card(Color.RED, CardType.EIGHT))

        with self.assertRaises(ValueError):
            self.game.play_card(5, 0)

    def test_play_wild_card(self):
        self.prepare_play(Card(Color.WILD, CardType.WILD))

        self.game.play_card(1, 0, Color.BLUE)

        self.assertEqual(self.game.active_color, Color.BLUE)


    def test_play_wild_without_chosen_color(self):
        self.prepare_play(Card(Color.WILD, CardType.WILD))

        with self.assertRaises(ValueError):
            self.game.play_card(1, 0)


    def test_play_wild_with_invalid_color(self):
        self.prepare_play(Card(Color.WILD, CardType.WILD))

        with self.assertRaises(ValueError):
            self.game.play_card(1, 0, Color.WILD)

    def test_player_wins(self):
        self.game.start()

        self.game.get_player(1).hand = [
            Card(Color.RED, CardType.EIGHT)
        ]

        self.game.active_color = Color.RED
        self.game.active_type = CardType.THREE

        result = self.game.play_card(1, 0)

        self.assertEqual(result, 1)
        self.assertTrue(self.game.finished)


    def test_game_not_finished_when_cards_remain(self):
        self.prepare_play(Card(Color.RED, CardType.EIGHT))

        result = self.game.play_card(1, 0)

        self.assertIsNone(result)
        self.assertFalse(self.game.finished)