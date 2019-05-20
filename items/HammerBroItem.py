from items.ItemBase import ItemBase, ItemType
class HammerBroItem(ItemBase):
    def __init__(self):
        self._cost = 20

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.LAND

    def apply(self, player, state, target=None):
        coins_taken = min(target.coins, 10)
        player.coins += coins_taken

