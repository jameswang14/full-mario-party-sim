import random
from board.TileBase import NON_WALKABLE_TILES
class Board:
    start = None
    id_to_tile = {}
    def random_tile(self, exclude=[]):
        a = random.choice(list(self.id_to_tile.values()))
        while a in exclude:
            a = random.choice(list(self.id_to_tile.values()))
        return a

    def distance(self, a, b):
        s = [(a,0)]
        while len(s) > 0:
            x = s.pop()
            curr, d = x[0], x[1]
            if curr == b:
                return d
            for t in s.next():
                s.append(t, d+1)
        return -1

    def adjacent_tiles(self, tile, n=4, walkable_only=False):
        tiles = []
        self._get_adjacent_tiles(tile, n, tiles, False, walkable_only)
        self._get_adjacent_tiles(tile, n, tiles, True, walkable_only)
        if tile in tiles: 
            tiles.remove(tile)
        return tiles

    def _get_adjacent_tiles(self, tile, n, tiles, reverse, walkable_only):
        if n == 0:
            return
        if not walkable_only or (walkable_only and tile.type not in NON_WALKABLE_TILES):
            tiles.append(tile)
        next_tiles = tile.next if reverse else tile.previous
        for t in next_tiles:
            if walkable_only and t.type in NON_WALKABLE_TILES:
                self._get_adjacent_tiles(t, n, tiles, reverse, walkable_only)
            else:
                self._get_adjacent_tiles(t, n-1, tiles, reverse, walkable_only)







    

