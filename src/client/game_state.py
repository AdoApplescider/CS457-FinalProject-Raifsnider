#A simplified model of the gamestate for the client to update and reference

from dataclasses import dataclass
from src.models.card import Card, Color, CardType

def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)

@dataclass
class GameState:
    active_color: Color
    active_type: CardType
    active_player_id: int
    turn_order: list[int]
    hand_sizes: dict[int, int]
    my_hand: list[Card]

    @classmethod
    def from_msg(cls, msg):
        try:
            active_player_id = msg["active_player_id"]
            if not _is_int(active_player_id):
                raise ValueError("active_player_id must be an int")

            turn_order = msg["turn_order"]
            if not isinstance(turn_order, list) or not all(_is_int(i) for i in turn_order):
                raise ValueError("turn_order must be a list of ints")

            hand_sizes = {}
            for p in msg["player_hand_sizes"]:
                if not (_is_int(p["id"]) and _is_int(p["hand_size"])):
                    raise ValueError("bad entry in player_hand_sizes")
                hand_sizes[p["id"]] = p["hand_size"]

            my_hand = [Card(Color(c["color"]), CardType(c["type"])) for c in msg["my_hand"]]

            return cls(
                active_color=Color(msg["active_color"]),
                active_type=CardType(msg["active_type"]),
                active_player_id=active_player_id,
                turn_order=turn_order,
                hand_sizes=hand_sizes,
                my_hand=my_hand,
            )
        except (KeyError, TypeError) as e:
            raise ValueError(f"Malformed STATE_UPDATE: {e!r}") from e