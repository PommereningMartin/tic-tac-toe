import random
from typing import List


class Board(List):
    default_char = ' '

    def __init__(self, height, width, dimension):
        super().__init__()
        self.height = range(height)
        self.width = range(width)
        self.dimension = dimension
        self.moves = []
        self.init_grid(height, width)
        self.id = random.randint(0, 1000)

    def init_grid(self, height, width):
        print('running init grid')
        rows, cols = height, width
        for i in range(rows):
            col = []
            for j in range(cols):
                cell = dict(
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
        for row in range(self.dimension):
            for col in range(self.dimension):
                if self.is_space_empty(row, col):
                    choices.append([row, col])
        print('get_legal_moves', choices)
        return choices

    def is_space_empty(self, row, col):
        return self[row][col]['value'] == self.default_char

    def make_move(self, row, col, player):
        if self.is_space_empty(row, col):
            self[row][col]['value'] = player.symbol
            self.moves.append([row, col])

    def has_winner(self):
        # need at least 5 moves before x hits three in a row
        if len(self.moves) < 5:
            print('moves', self.moves)
            #return None

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
        for col in range(self.dimension):
            unique_cols = set()
            for row in range(self.dimension):
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
        return None

    def disable_all_fields(self):
        for row in self:
            for field in row:
                field['isEnabled'] = False
