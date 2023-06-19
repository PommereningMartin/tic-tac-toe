from grid import Grid
from player import Player
from turn import Turn


class Game(object):

    def __init__(self):
        self.turn_history = []
        self.current_player = None
        self.grid = Grid(3, 3)
        # TODO: make x and o
        self.player_1 = Player(1, 'x')
        self.player_2 = Player(2, 'o')
        self.grid.render()

    # TODO:
    #  input validation,
    #  print whole history of a game,
    #  check for win or draw,
    #  testing
    def run(self):
        current_turn = 1
        while True:
            turn = Turn()
            turn.make(self.player_1, self.grid)
            turn.update_grid(self.player_1, self.grid)
            self.grid.render()
            # turn.check_win_or_draw()
            turn.make(self.player_2, self.grid)
            turn.update_grid(self.player_2, self.grid)
            self.grid.render()
            # turn.check_win_or_draw()
            self.turn_history.append(turn)
            current_turn = current_turn + 1
            if current_turn > 9:
                exit()
            # print(self.turn_history)

    def get_state(self) -> dict:
        return dict(player1Name=self.player_1.name, player2Name=self.player_2.name,
                    grid=self.grid, currentPlayer=self.current_player)

# Game().run()
