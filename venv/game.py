from grid import Grid
from player import Player
from turn import Turn


class Game(object):

    def __init__(self):
        self.turn_history = []
        self.current_player = None
        self.grid = Grid(3, 3)
        self.player_1 = Player(1, 'x')
        self.player_2 = Player(2, 'o')
        self.grid.render()

    """
    - new turn
    - player1 input
    - player2 input
    -validate input
    -update grid with player input
    -print grid
    """
    def run(self):
        current_turn = 1
        while True:
            turn = Turn()
            turn.make(self.player_1, self.grid.get_state())
            turn.make(self.player_2, self.grid.get_state())
            if turn.is_not_valid():
                exit()
            self.turn_history.append(turn)
            self.grid.render()
            print(current_turn)
            current_turn += 1
            if current_turn > 9:
                exit()
            # print(self.turn_history)

    def not_three_in_row(self):
        pass

    @staticmethod
    def not_valid_input(p1_input, p2_input):
        if p1_input.__eq__(p2_input):
            print('p1 input and p2 input are the same')
            return True


Game().run()
