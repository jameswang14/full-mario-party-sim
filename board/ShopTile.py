import random
from board.TileBase import TileType, TileBase
from board.ItemTile import ALL_ITEMS
class ShopTile(TileBase):
    def __init__(self, _id):
        super(ShopTile, self).__init__(TileType.SHOP, _id)

    def apply(self, player, state, stats=None):
        possible_items = [x for x in ALL_ITEMS if x().cost < player.coins]
        choices = []
        if len(possible_items) == 0:
            return 
        if len(possible_items) == 1:
            choices = possible_items * 3
        if len(possible_items) == 2:
            chocies = [possible_items[0], possible_items[0], possible_items[1]]
        else:
            choices = random.choices(possible_items, k=3)
        player.buy_item(choices, state)
        stats.inc("items_bought")
        