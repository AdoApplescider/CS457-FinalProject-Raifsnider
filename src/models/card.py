# This model represents a card. It is only responsible for checking it's own validity,-
#-and checking if it can be played on top of another card

from dataclasses import dataclass
from enum import StrEnum

class Color(StrEnum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    WILD = "WILD"


class CardType(StrEnum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    SKIP = "SKIP"
    REVERSE = "REVERSE"
    DRAW_TWO = "DRAW_TWO"
    WILD = "WILD"
    WILD_DRAW_FOUR = "WILD_DRAW_FOUR"

def can_play_on(new_color, new_type, active_color, active_type) -> bool:
    return (
        new_type == CardType.WILD
        or new_color == active_color
        or new_type == active_type
        or active_color == Color.WILD
    )

@dataclass(frozen=True)
class Card:
    color: Color
    type: CardType

    def to_dict(self):
        return {"color": self.color, "type": self.type}

    def __post_init__(self):

        if not isinstance(self.color, Color):
            raise TypeError("color must be a Color enum")

        if not isinstance(self.type, CardType):
            raise TypeError("value must be a CardType enum")

        if self.color != Color.WILD and self.type in {
            CardType.WILD,
            CardType.WILD_DRAW_FOUR
        }:
            raise TypeError("wildcards cannot have a non-wild color")

        if self.color == Color.WILD and self.type not in {
            CardType.WILD,
            CardType.WILD_DRAW_FOUR
        }:
            raise TypeError("non-wild cards cannot have a wild color")