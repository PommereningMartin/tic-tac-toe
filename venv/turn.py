from grid import Grid


class Turn(object):

    def __init__(self, number, input1, input2, grid_state: Grid):
        self.turn_number = number
        self.input1 = input1
        self.input2 = input2
        self.grid = grid_state

    def input(self, position: str):
        pass

    def is_not_valid(self):
        pass

    def make(self):
        pass