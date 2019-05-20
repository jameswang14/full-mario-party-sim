from board.Board import Board
from Player import Player

class State:
    def move_star(self, exclude=[]):
        self.star = self.board.random_tile(exclude)

    def __init__(self, players, max_turns, board, stats):
        self.players = [Player(x[0], x[1]) for i,x in enumerate(players)]
        self.standings = []
        self.minigame_assign = {}
        self.turn_num = 0
        self.max_turns = max_turns
        self.turns_remaining = max_turns
        self.total_skill = sum([x[0] for x in players])

        self.current_roll = 0

        self.player_to_tile = {}
        self.tiles_with_items = {}
        self.board = board
        self.stats = stats
        
        self.move_star()
        