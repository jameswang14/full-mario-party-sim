import random
from items.ItemBase import ItemType
class Player(object):
    def __init__(self, skill, ident=0):
        self.reset()
        self.skill = skill
        self.wins = 0
        self._id = ident
        self.items = []
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
        if self.items[0].type == ItemType.SELF:
            self.items[0].apply(player=self, state=state)
        elif self.items[0].type == ItemType.LAND \
            or self.items[0].type == ItemType.PASS:
            print("Here")
            print(len(state.board.adjacent_tiles(state.player_to_tile[self]) ))
        del self.items[0]
        state.stats.inc("items_used")

    def roll(self, state):
        state.current_roll += random.randint(1, 10)
