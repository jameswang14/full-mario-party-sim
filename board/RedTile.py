from board.TileBase import TileType, TileBase
class RedTile(TileBase):
    def __init__(self, _id):
        super(RedTile, self).__init__(TileType.RED, _id)

    def apply(self, player, state, stats=None):
        player.coins -= 3
        player.coins = max(player.coins, 0)
        player.red += 1
        state.minigame_assign[player] = 'red'