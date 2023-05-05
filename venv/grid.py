from typing import List


class Grid(List):
    grid = None
    default_char = 0

    def __init__(self, height, width):
        super().__init__()
        self.height = range(height)
        self.width = range(width)
        self.init_grid(height, width)

    def init_grid(self, height, width):
        rows, cols = height + 1, width + 1
        for i in range(rows):
            col = []
            for j in range(cols):
                if i == 0:
                    col.append(j)
                else:
                    col.append(self.default_char)
                if j == 0:
                    col[0] = i
            self.append(col)

    def render(self):
        for row in self:
            print(row)

    def get_state(self):
        return self
