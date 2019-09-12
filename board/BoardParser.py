from board.Board import Board
from board.BlueTile import BlueTile
from board.RedTile import RedTile
from board.GreenTile import GreenTile
from board.BowserTile import BowserTile
from board.DKTile import DKTile
from board.DuelTile import DuelTile
from board.IntersectionTile import IntersectionTile
from board.ItemTile import ItemTile
from board.ShopTile import ShopTile

LETTER_TO_TILE = {
    'B': BlueTile,
    'R': RedTile,
    'G': GreenTile,
    'W': BowserTile,
    'K': DKTile,
    'D': DuelTile,
    'I': IntersectionTile,
    'T': ItemTile,
    'S': ShopTile,
}


BOARD_CACHE = {}

def parse_board_from_file(filename):
    if filename in BOARD_CACHE:
        return BOARD_CACHE[filename]
    board = Board()
    f = open(filename, "r")

    for i, line in enumerate(f): 
        last_tile = None
        _id = None
        tiles = line.split()
        for t in tiles:
            parsed_tile, _id = _parse_tile(t, board)
            if int(t[0]) == 0:
                board.start = parsed_tile
            if last_tile:
                last_tile.append(parsed_tile)
                parsed_tile.prepend(last_tile)
            last_tile = parsed_tile
            if _id in board.id_to_tile:
                    continue
            board.id_to_tile[_id] = parsed_tile
        if i == 0:
            board.id_to_tile[_id].next = [board.start]
    BOARD_CACHE[filename] = board
    return board


def _parse_tile(t, board):
    if t[-1] not in LETTER_TO_TILE: 
        raise Exception("Invalid Serialization: {} is not a valid type".format(t[1]))
    _id = int(t[0:-1])
    if _id in board.id_to_tile:
        return board.id_to_tile[_id], _id
    return LETTER_TO_TILE[t[-1]](_id), _id
