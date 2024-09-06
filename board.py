import random
from typing import List
from typing import TypedDict


class Cell(TypedDict):
    value: str
    isEnabled: bool


class Board(List[List[Cell]]):
    default_char = None

    def __init__(self, height, width):
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
        winner = None
        # need at least 5 moves before x hits three in a row
        if not self.min_moves_for_win():
            print('moves', self.moves)
            #return None
        
        winner = self.check_rows_for_winner()
        
        # check rows for win
        for row in range(self.dimension):
            print('has_winner', self[row])
            foo = self[row]
            unique_rows = set()
            for i in foo:
                unique_rows.add(i['value'])
            if len(unique_rows) == 1:
                value = unique_rows.pop()
                if value is not None:
                    return value

        # check columns for win
        for col in range(self.cols):
            unique_cols = set()
            for row in range(self.rows):
                unique_cols.add(self[row][col]['value'])

            if len(unique_cols) == 1:
                value = unique_cols.pop()
                if value is not None:
                    return value

        # check backwards diagonal (top left to bottom right) for win
        backwards_diag = set()
        backwards_diag.add(self[0][0]['value'])
        backwards_diag.add(self[1][1]['value'])
        backwards_diag.add(self[2][2]['value'])

        if len(backwards_diag) == 1:
            value = backwards_diag.pop()
            if value is not None:
                return value

        # check forwards diagonal (bottom left to top right) for win
        forwards_diag = set()
        forwards_diag.add(self[2][0]['value'])
        forwards_diag.add(self[1][1]['value'])
        forwards_diag.add(self[0][2]['value'])

        if len(forwards_diag) == 1:
            value = forwards_diag.pop()
            if value is not None:
                return value

        # found no winner, return None
        return winner

    def disable_all_fields(self):
        for row in self:
            for field in row:
                field['isEnabled'] = False

    def check_rows_for_winner(self):
        for row in range(self.rows):
            for col in range(self.cols):
                return