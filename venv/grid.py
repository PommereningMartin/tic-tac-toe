class Grid(object):
    grid = None

    def __init__(self, height, width):
        self.height = range(height)
        self.width = range(width)
        self.init_grid(height, width)

    def init_grid(self, height, width):
        init_char = 0
        self.grid = []
        rows, cols = height, width
        for i in range(height):
            col = []
            for j in range(width):
                col.append(0)
            self.grid.append(col)

    def render(self):
        for row in self.grid:
            print(row)

    def get_state(self):
        return self.grid
