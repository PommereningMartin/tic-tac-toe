from typing import List


class Grid(List):
    default_char = ' '

    def __init__(self, height, width):
        super().__init__()
        self.height = range(height)
        self.width = range(width)
        self.init_grid(height, width)

    def init_grid(self, height, width):
        rows, cols = height, width
        for i in range(rows):
            col = []
            for j in range(cols):
                col.append(dict(value=self.default_char, isEnabled=True))
            self.append(col)

    def render(self):
        for row in self:
            print(row)

    def get_state(self):
        return self
