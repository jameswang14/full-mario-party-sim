from board.TileBase import TileType, TileBase
class BlueTile(TileBase):
    def __init__(self, _id):
        super(BlueTile, self).__init__(TileType.BLUE, _id)

    def apply(self, player, state, stats=None):
        player.coins += 3
        state.minigame_assign[player] = 'blue'