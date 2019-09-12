from items.ItemBase import ItemBase, ItemType
class SpinyItem(ItemBase):
    def __init__(self):
        self._cost = 10
        self.owner = None

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.PASS

    def apply(self, target, state):
        coins_taken = min(target.coins, 10)
        target.coins -= coins_taken
        state.stats.inc("spiny_passed")
    

