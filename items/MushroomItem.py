from items.ItemBase import ItemBase, ItemType
class MushroomItem(ItemBase):
    def __init__(self):
        self._cost = 10

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.SELF

    def apply(self, player, state, target=None):
        player.roll(state)

