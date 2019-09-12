from items.ItemBase import ItemBase, ItemType
class TweesterItem(ItemBase):
    def __init__(self):
        self._cost = 15
        self.owner = None

    @property   
    def cost(self):
        return self._cost

    @property
    def type(self):
        return ItemType.PASS

    def apply(self, target, state):
        state.move_player_random(target)
        state.stats.inc("tweester_passed")
    

