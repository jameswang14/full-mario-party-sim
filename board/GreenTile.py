import random
from board.TileBase import TileType, TileBase

GREEN_STAR_PCT = 0.05
MIN_STAR_DIST = 30
MAX_STAR_DIST = 40

class GreenTile(TileBase):
    def __init__(self, _id):
        super(GreenTile, self).__init__(TileType.GREEN, _id)

    def apply(self, player, state, stats=None):
        # TODO: break these down into more specific green squares
        r = random.choice([1,2,3])

        # +Coins/Star - Coins are pretty much guaranteed, usually the question is how many. 
        # Stars are much more rare
        if r == 1:
            player.coins += random.randint(1, 20)
            if random.random() <= GREEN_STAR_PCT:
                player.stars += 1
                stats.inc("green_star")
                stats.inc("num_stars")

        # -Coins - I don't think there are any green spaces that make you lose coins in MP7, but 
        # they're usually present in other games so I've included it here
        if r == 2:
            player.coins -= random.randint(1, 10)

        # Teleport - Note: These don't contribute to the movement bonus star
        if r == 3:
            state.move_player_random(player)
            if state.player_to_tile[player] == state.star: 
                player.buy_star(self, state) # Yes it's possible to get two stars in one turn!
                stats.inc("num_stars")

        if random.random() < 0.3: state.minigame_assign[player] = 'red' # with a 50/50 chance, I noticed the number of 1v3 minigames seemed higher than it should be
        else: state.minigame_assign[player] = 'blue'
        player.green += 1