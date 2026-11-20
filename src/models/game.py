#This object models the game state of uno, and abstracts away the actions of the game so that the server can-
#-focus on network logic and translating requests into actions, instead of dealing directly with how game actions-
#-are taken.

from src.models.player import Player
from src.models.card import Card, Color, CardType, can_play_on

class Game:
    def __init__(self):
        self.players = []
        self.active_player = 0
        self.turn_step = 1
        self.active_color = None
        self.active_type = None
        self.started = False
        self.finished = False


    def add_player(self):
        if self.started:
            raise RuntimeError("Game has already started")

        if len(self.players) >= 4:
            raise ValueError("Game is full")

        player = Player(len(self.players) + 1)
        self.players.append(player)
        return player


    def remove_player(self):
        if self.started:
            raise RuntimeError("Game has already started")

        if len(self.players) <= 0:
            raise ValueError("Game is empty")

        self.players.pop()


    def get_player(self, id):
        player = next(
            (p for p in self.players if p.id == id),
            None
        )

        if player is None:
            raise ValueError("Invalid player ID")

        return player


    def draw(self, player_id, amount=1):
        if not self.started or self.finished:
            raise RuntimeError("Game is not currently active")
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise TypeError("Draw amount must be an integer")
        if amount <= 0:
            raise ValueError("Draw amount must be positive")

        self.get_player(player_id).deal(amount)


    def start(self):
        if self.started:
            raise RuntimeError("Game has already started")
        if len(self.players) <= 1:
            raise ValueError("Game has less than two players")

        self.active_color = Color.WILD
        self.active_type = CardType.WILD
        self.active_player = 1

        self.started = True


    def play_card(self, player_id, card_index, chosen_color=None):
        if not self.started or self.finished:
            raise RuntimeError("Game is not currently active")

        if not 0 <= card_index < len(self.get_player(player_id)):
                    raise ValueError("Invalid card index")

        if player_id != self.active_player:
            raise ValueError(f"It is not player {player_id}'s turn! It's player {self.active_player}'s turn!")

        if not isinstance(card_index, int) or isinstance(card_index, bool):
            raise TypeError("Card index must be an integer")

        player = self.get_player(player_id)
        card = player.hand[card_index]

        self.active_type = card.type

        if card.type in {CardType.WILD, CardType.WILD_DRAW_FOUR}:
            if not chosen_color:
                raise ValueError("Wildcards must have a selected color input! Type red, blue, yellow, or green after the card number!")
            if not can_play_on(Color(chosen_color.upper()), card.type, self.active_color, self.active_type):
                raise ValueError("This card does not match the card in play!")
            try:
                self.active_color = Color(chosen_color.upper())
            except ValueError:
                raise ValueError("Invalid chosen color")
        else:
            if not can_play_on(card.color, card.type, self.active_color, self.active_type):
                raise ValueError("This card does not match the card in play!")
            self.active_color = card.color

        self.get_player(player_id).hand.pop(card_index)
        self.apply_effect(card)

        if len(self.get_player(player_id)) == 0:
            self.finished = True
            return player_id

        return None


    def apply_effect(self, card):
        if card.type == CardType.DRAW_TWO:
            self.advance_turn(2)
        elif card.type == CardType.WILD_DRAW_FOUR:
            self.advance_turn(4)
        elif card.type == CardType.REVERSE:
            self.turn_step *= -1
            self.advance_turn()
            if len(self.players) == 2:
                self.advance_turn()
        elif card.type == CardType.SKIP:
            self.advance_turn()
            self.advance_turn()
        else:
            self.advance_turn()

    def _step(self, start_id, steps=1):
        ids = [p.id for p in self.players]
        idx = ids.index(start_id)
        return ids[(idx + steps * self.turn_step) % len(ids)]

    def advance_turn(self, draw_amount=0):
        self.active_player = self._step(self.active_player)

        if draw_amount > 0:
            player = self.get_player(self.active_player)
            player.deal(draw_amount)
            self.active_player = self._step(self.active_player)