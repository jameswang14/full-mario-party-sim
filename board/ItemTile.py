import random
from board.TileBase import TileType, TileBase
from items.MushroomItem import MushroomItem
from items.SuperMushroomItem import SuperMushroomItem
from items.HammerBroItem import HammerBroItem

ALL_ITEMS = [MushroomItem, SuperMushroomItem, HammerBroItem]


class ItemTile(TileBase):
    def __init__(self, _id):
        super(ItemTile, self).__init__(TileType.ITEM, _id)

    def apply(self, player, state, stats=None):
        player.items.append(random.choice(ALL_ITEMS)())
