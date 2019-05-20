import random
from board.TileBase import TileType, TileBase
class DKTile(TileBase):
    def __init__(self, _id):
        super(DKTile, self).__init__(TileType.DK, _id)

    def apply(self, player, state, stats=None):
        # Single-Player DK
        if random.random() < 0.5:
            if random.random() < player.skill/100.0: # Wins
                r_dk = random.choice([1,2,3,4])
                if r_dk == 4:
                    player.stars += 1
                else:
                    player.coins += 10 * r_dk
        # Multi-Player DK
        else:
            r_dk = random.choice([1,2,3])
            total_bananas = 35
            for x in state.players:
                x.coins += int(x.skill/state.total_skill * total_bananas) * r_dk

        state.minigame_assign[player] = 'blue'