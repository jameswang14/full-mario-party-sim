from items.ItemBase import ItemBase, ItemType
class ZapItem(ItemBase):
    def __init__(self):
        self._cost = 15
        self.owner = None

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.PASS

    # we can't compute how many coins the player will lose since they could get stopped,
    # so instead we attach a "zapped" status and deduct coins on each move
    def apply(self, target, state):
        target.status["zapped"] = 1
        state.stats.inc("zap_passed")
    

