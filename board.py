import random
from typing import List
from typing import TypedDict


class Cell(TypedDict):
    value: str
    isEnabled: bool


class Board(List[List[Cell]]):
    default_char = ''

    def __init__(self, height:int, width:int):
        super().__init__()
        self.rows, self.cols = height, width
        self.moves = []
        self.init_grid()
        self.id = random.randint(0, 1000)

    def init_grid(self):
        # print('running init grid')
        for i in range(self.rows):
            col: List[Cell] = []
            for j in range(self.cols):
                cell: Cell = dict(
                    value=self.default_char,
                    isEnabled=True)
                col.append(cell)
            self.append(col)

    def render(self):
        for row in self:
            print(row)

    def get_state(self):
        return self

    def get_legal_moves(self):
        choices = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_space_empty(row, col):
                    choices.append([row, col])
        print('get_legal_moves', choices)
        return choices

    def is_space_empty(self, row_index, col_index):
        return self[row_index][col_index]['value'] is None

    def make_move(self, row_index, col_index, player):
        if self.is_space_empty(row_index, col_index):
            self.set_value(row_index, col_index, player.symbol)
            self.moves.append([(row_index, col_index, player.symbol)])

    def set_value(self, row_index, col_index, value):
        self[row_index][col_index]['value'] = value

    def get_value(self, row_index, col_index):
        return self[row_index][col_index]['value']

    def min_moves_for_win(self):
        return len(self.moves) < 5

    def has_winner(self):
        return self.check_winner()

    def disable_all_fields(self):
        for row in self:
            for field in row:
                field['isEnabled'] = False

    def check_rows_for_winner(self, x_count, o_count):
        for row in range(self.rows):
            for col in range(self.cols):
                return

    def check_winner(self):
        n = len(self)  # board size

        # Check rows
        for row in range(self.rows):
            if all(self[row][col] == self[row][0] and self[row][0] != ' ' for col in range(self.rows)):
                return self[row][0]
    
        # Check columns
        for col in range(self.rows):
            if all(self[row][col] == self[0][col] and self[0][col] != ' ' for row in range(self.rows)):
                return self[0][col]
    
        # Check main diagonal (top-left to bottom-right)
        if all(self[i][i] == self[0][0] and self[0][0] != ' ' for i in range(self.rows)):
            return self[0][0]
    
        # Check anti-diagonal (top-right to bottom-left)
        if all(self[i][n-1-i] == self[0][n-1] and self[0][n-1] != ' ' for i in range(self.rows)):
            return self[0][n-1]
    
        # Check for draw
        if all(self[i][j] != ' ' for i in range(self.rows) for j in range(self.rows)):
            return 'Draw'
    
        # Game is still ongoing
        return None