#A simplified model of the gamestate for the client to update and reference

from src.models.card import Card, Color, CardType

class GameState:
    active_color: Color
    active_type: CardType
    my_player_id: int
    active_player_id: int
    next_turns: list[int]
    my_hand: list[Card]
    opponent_hand_sizes: dict[int, int]

    def update_state(msg):
        #unpacks the message, validates it, and updates the state