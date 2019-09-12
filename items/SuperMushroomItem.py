from items.ItemBase import ItemBase, ItemType
class SuperMushroomItem(ItemBase):
    def __init__(self):
        self._cost = 20

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.SELF

    def apply(self, player, state, target=None):
        r = player.roll(state)
        r2 = player.roll(state)
        if player.roll(state) == r and r == r2:
            player.coins += 30
            # rolling three 7s gets you 100 coins
            if r == 7:
                player.coins += 70
        state.stats.inc("super_shroom_used")


