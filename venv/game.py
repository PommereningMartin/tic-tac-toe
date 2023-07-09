from board import Board
from player import Player
from turn import Turn
import uuid

from random_bot import RandomBot


class Game(object):

    def __init__(self, id: uuid):
        self.id = id
        self.turn_history = []
        self.current_player: Player = None
        self.board = Board(3, 3, 3)
        self.player_1 = Player(1, 'x')
        self.bot = RandomBot(2, 'o')
        self.winner = None
        #self.grid.render()

    # TODO:
    #  input validation,
    #  print whole history of a game,
    #  check for win or draw,
    #  testing
    def run(self):
        current_turn = 1
        while True:
            turn = Turn()
            turn.make(self.player_1, self.board)
            turn.update_grid(self.player_1, self.board)
            self.board.render()
            # turn.check_win_or_draw()
            turn.make(self.bot, self.board)
            turn.update_grid(self.bot, self.board)
            self.board.render()
            # turn.check_win_or_draw()
            self.turn_history.append(turn)
            current_turn = current_turn + 1
            if current_turn > 9:
                exit()
            # print(self.turn_history)

    def get_state(self) -> dict:
        #print('get_state',self.current_player.name)
        return dict(player1Name=self.player_1.name, player2Name=self.bot.name,
                    grid=self.board, currentPlayer=self.current_player, gameId=self.id)

# Game().run()
