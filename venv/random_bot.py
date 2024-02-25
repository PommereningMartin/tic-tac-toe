import random

from board import Board
from player import Player


class RandomBot(Player):

    def __init__(self, player_number: int, symbol: str):
        super().__init__(player_number, symbol)

    def select_move(self, grid: Board):
        print('select_move', grid)
        candidates = grid.get_legal_moves()
        if len(candidates) > 0:
            print('select_move:candidates',candidates)
            return random.choice(candidates)
        return None
