from board.TileBase import TileType, TileBase
class IntersectionTile(TileBase):
    def __init__(self, _id):
        super(IntersectionTile, self).__init__(TileType.INTERSECTION, _id)