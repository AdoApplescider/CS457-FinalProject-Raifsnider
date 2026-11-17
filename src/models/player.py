#This model represents a player
#It is responsible for storing the player's thread communication buffer, the player's hand, and their ID number.
#It is also responsible for drawing, playing, and discarding cards from that player's hand.

import random
from dataclasses import dataclass, field

from src.models.card import Card, CardType, Color

@dataclass
class Player:
    id: int
    hand: list[Card] = field(default_factory=list)

    def __len__(self):
        return len(self.hand)

    def deal(self, this_many):
        if this_many < 0:
            raise ValueError("Amount cannot be negative")

        for _ in range(this_many):
            color = random.choice(list(Color))
            card_type = random.choice(list(CardType))

            if color == Color.WILD and card_type not in {
                        CardType.WILD,
                        CardType.WILD_DRAW_FOUR
                    }:
                card_type = random.choice([CardType.WILD, CardType.WILD_DRAW_FOUR])
            elif color != Color.WILD and card_type in {
                        CardType.WILD,
                        CardType.WILD_DRAW_FOUR
                    }:
                color = Color.WILD

            self.hand.append(Card(color, card_type))

    def discard(self, index):
        try:
            return self.hand.pop(index)
        except IndexError:
            return None

    def __post_init__(self):
        if not isinstance(self.id, int) or isinstance(self.id, bool):
            raise TypeError("player id must be an integer")

        if not 1 <= self.id <= 4:
            raise ValueError("player id must be between 1 and 4")

        self.deal(7)