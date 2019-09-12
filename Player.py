import random
from items.ItemBase import ItemType
from items.MushroomItem import MushroomItem
from items.SuperMushroomItem import SuperMushroomItem
class Player(object):
    def __init__(self, skill, ident=0):
        self.reset()
        self.skill = skill
        self.wins = 0
        self._id = ident
        self.items = []
        # a map of statuses to number of turns they're active for
        self.status = {}
    def __str__(self):
        return "ID: {}, Stars: {}, Coins: {}, Skill: {}".format(self._id, self.stars, self.coins, self.skill)
    def reset(self):
        self.coins = 10 
        self.spaces_moved = 0
        self.items_used = 0
        self.green = 0
        self.red = 0
        self.coins_spent = 0
        self.spaces_from_star = 0
        self.stars = 0
        self.items = []
        self.minigames_won = 0

    def buy_star(self, t, state):      
        if self.coins >= 20:
            self.stars += 1
            self.coins -= 20
            state.stats.inc("num_stars")
            state.move_star([t])  

    def use_item(self, state):
        if len(self.items) == 0:
            return
        # TODO - replace naive logic
        item_to_use = self.items[0]
        if item_to_use.type == ItemType.SELF:
            item_to_use.apply(player=self, state=state)
        elif item_to_use.type == ItemType.LAND \
            or item_to_use.type == ItemType.PASS:
            current_tile = state.player_to_tile[self]
            # TODO - replace naive logic
            target_tile = random.choice(state.board.adjacent_tiles(current_tile, walkable_only=True))
            state.tiles_with_items[target_tile._id] = item_to_use
            item_to_use.owner = self
        del self.items[0]
        state.stats.inc("items_used")

    def roll(self, state):
        roll = random.randint(1, 10)
        state.current_roll += roll
        return roll

    def buy_item(self, items, state):
        # 1. only buy an item if it keeps the player with 20 or more coins
        # 2. prefer buying mushrooms first, otherwise randomly choose 
        for c in items:
            if isinstance(c, MushroomItem) or isinstance(c, SuperMushroomItem) and self.coins - c.cost >= 20:
                self.items.append(c())
                self.coins -= c().cost
                return
        for c in items:
            if self.coins - c().cost >= 20:
                self.items.append(c())
                self.coins -= c().cost

    def update_status(self):
        self.status = {s: t-1 for s, t in self.status.items() if t-1 > 0}

