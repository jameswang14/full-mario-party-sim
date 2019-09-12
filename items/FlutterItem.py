from items.ItemBase import ItemBase, ItemType
class FlutterItem(ItemBase):
    def __init__(self):
        self._cost = 30

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.SELF

    def apply(self, player, state, target=None):
        state.player_to_tile[player] = state.star
        if player.coins >= 20:
            state.stats.inc("stars_from_flutter")
        else:
            state.stats.inc("flutter_used_but_no_star")
        player.buy_star(state.star, state)


