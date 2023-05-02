from venv.grid import Grid
from player import Player
from turn import Turn


class Game(object):

    def __init__(self):
        self.turns = []
        self.current_player = None
        self.grid = Grid(3, 3)
        self.player_1 = Player(1)
        self.player_2 = Player(2)
        self.grid.render()
        self.run()

    def run(self):
        current_turn = 1
        while True:
            print('{0} pls enter cords:'.format(self.player_1.get_name()))
            p1_input = tuple(map(int, input().split(',')))
            print('{0} pls enter cords:'.format(self.player_2.get_name()))
            p2_input = tuple(map(int, input().split(',')))
            if self.not_valid_input(p1_input, p2_input):
                exit()
            turn = Turn(current_turn,p1_input, p2_input, self.grid.get_state())
            if turn.is_not_valid():
                exit()
            turn.make()
            self.turns.append(turn)
            print(self.turns)

    def not_three_in_row(self):
        pass

    @staticmethod
    def not_valid_input(p1_input, p2_input):
        if p1_input.__eq__(p2_input):
            print('p1 input and p2 input are the same')
            return True
