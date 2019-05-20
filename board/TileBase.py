from abc import ABC, abstractmethod
from enum import Enum
class TileType(Enum):
    UNKNOWN = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    DK = 4
    BOWSER = 5
    DUEL = 6
    STAR = 7

    # These tiles aren't really tiles in the game, as crossing these tiles
    # doesn't consume a roll unit, but it's easiest to code these spaces
    # as tiles.
    ITEM = 8
    SHOP = 9
    INTERSECTION = 10
    START = 11

class TileBase(object):
    def __init__(self, tile_type, _id):
        self._id = _id
        self.type = tile_type
        self.next = []
        self.previous = []

    def __eq__(self, other):
        return self._id == other._id

    def append(self, t):
        self.next.append(t)
    def prepend(self, t):
        self.previous.append(t)

    @abstractmethod
    def apply(self, player, state, stats=None):
        return

