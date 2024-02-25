from typing import Tuple

from board import Board
from player import Player


class Turn(object):

    def __init__(self):
        self.turn_number = None
        self.input1 = None
        self.input2 = None
        self.grid = None
        self.current_player = None

    def make(self, player: Player, state: Board):
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
        if retry is True:
            print('{0} pls enter another cords:'.format(player.name))
        print('{0} pls enter cords:'.format(player.name))
        player.input = tuple(map(int, input().split(',')))
        return player

    @staticmethod
    def update_grid(player: Player, grid: Board):
        x, y = player.input
        grid[x][y] = player.symbol

    @staticmethod
    def not_update_grid(player: Player, grid: Board) -> bool:
        x, y = player.input
        if grid[x][y] == grid.default_char:
            return False
        if grid[x][y] != 'x' or grid[x][y] != 'o':
            return False
        return True

    def check_win_or_draw(self):
        row_count_x = 0
        row_count_o = 0
        for row in self.grid[1:]:
            print(row)
            row_count_x = row.count("x")
            row_count_o = row.count('o')
        print(row_count_x)
        print(row_count_o)
        if row_count_x == 3:
            print("Player 1 wins")
        if row_count_o == 3:
            print("Player 2 wins")

