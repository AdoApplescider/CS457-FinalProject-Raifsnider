# This model represents a card. It is only responsible for checking it's own validity,-
#-and checking if it can be played on top of another card

from dataclasses import dataclass
from enum import Enum

class Color(Enum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    WILD = "WILD"


class CardType(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    SKIP = "SKIP"
    REVERSE = "REVERSE"
    DRAW_TWO = "DRAW_TWO"
    WILD = "WILD"
    WILD_DRAW_FOUR = "WILD_DRAW_FOUR"


@dataclass(frozen=True)
class Card:
    color: Color
    type: CardType

    #Direction matters here, be sure you're calling new_card.can_play_on(card_in_play) and not the other way.
    def can_play_on(self, active_color, active_type) -> bool:
        return (
            active_color == self.color
            or active_type == self.type
            or self.type == CardType.WILD
            or active_color == CardType.WILD
        )

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