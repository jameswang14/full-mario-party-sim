import random
from board.TileBase import TileType, TileBase
from board.ItemTile import ALL_ITEMS
class ShopTile(TileBase):
    def __init__(self, _id):
        super(ShopTile, self).__init__(TileType.SHOP, _id)

    def apply(self, player, state, stats=None):
        possible_items = [x for x in ALL_ITEMS if x.cost < player.coins]
        choices = random.choices(possible_items, k=3)
        