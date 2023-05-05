from typing import Tuple

from grid import Grid
from player import Player


class Turn(object):

    def __init__(self):
        self.turn_number = None
        self.input1 = None
        self.input2 = None
        self.grid = None
        self.current_player = None

    def input(self, position: str):
        pass

    def is_not_valid(self):
        pass

    def make(self, player: Player, state: Grid):
        if self.turn_number is None:
            self.turn_number = 1
        else:
            self.turn_number += 1
        self.player_input(player)
        if self.not_update_grid(player, state):
            self.player_input(player, True)
        self.update_grid(player, state)

    @staticmethod
    def player_input(player: Player, *retry: bool) -> Player:
        if retry:
            print('{0} pls enter another cords:'.format(player.name))
        print('{0} pls enter cords:'.format(player.name))
        player.input = tuple(map(int, input().split(',')))
        return player

    @staticmethod
    def update_grid(player, state):
        x, y = player.input
        state[x][y] = player.symbol

    @staticmethod
    def not_update_grid(player: Player, state: Grid) -> bool:
        x, y = player.input
        if state[x][y] == state.default_char:
            return False
        if state[x][y] != 'x' or state[x][y] != 'o':
            return False
        return True
