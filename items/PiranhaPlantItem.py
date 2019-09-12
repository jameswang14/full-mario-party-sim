from items.ItemBase import ItemBase, ItemType
class PiranhaPlantItem(ItemBase):
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
        coins_taken = target.coins // 2
        target.coins -= coins_taken
        self.owner.coins += coins_taken
        state.stats.inc("piranha_landed")
    

