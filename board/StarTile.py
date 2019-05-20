from board.TileBase import TileType, TileBase
class StarTile(BaseTile):
    def __init__(self, _id, old_tile):
        super(StarTile, self).__init__(TileType.STAR, _id)
        self.old_tile = old_tile

    def apply(self, player, state, stats=None):
        if player.coins >= 20:
            player.stars += 1
            player.coins -= 20
