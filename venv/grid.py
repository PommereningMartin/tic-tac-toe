class Grid(object):

    grid = None

    def __init__(self, height, width):
        self.height = range(height)
        self.width = range(width)
        self.init_grid(height, width)

    def init_grid(self, height, width):
        init_char = 0
        self.grid=[]
        rows, cols=height+1,width+1
        for i in range(rows):
            col = []
            for j in range(cols):
                if i == 0:
                    col.append(j)
                else:
                    col.append(0)
                if j == 0:
                    col[0] = i
            self.grid.append(col)

    def render(self):
        for row in self.grid:
            print(row)

    def get_state(self):
        return self.grid

