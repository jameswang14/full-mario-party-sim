from items.ItemBase import ItemBase, ItemType
class HammerBroItem(ItemBase):
    def __init__(self):
        self._cost = 20
        self.owner = None

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.LAND

    def apply(self, target, state):
        coins_taken = min(target.coins, 10)
        self.owner.coins += coins_taken
        target.coins -= coins_taken
        state.stats.inc("hammer_bro_landed")
    

