import random
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

    def adjacent_tiles(self, tile, n=4):
        tiles = []
        self._get_adjacent_tiles(tile, n, tiles, False)
        self._get_adjacent_tiles(tile, n, tiles, True)
        tiles.remove(tile)
        return tiles

    def _get_adjacent_tiles(self, tile, n, tiles, reverse):
        if n == 0:
            return
        tiles.append(tile)
        next_tiles = tile.next if reverse else tile.previous
        for t in next_tiles:
            self._get_adjacent_tiles(t, n-1, tiles, reverse)






    

