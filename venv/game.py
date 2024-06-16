import json
import random

from board import Board
from player import Player
from turn import Turn


class Game(object):

    current_player: Player | None = None
    player_1 = Player(1, 'x')
    player_2 = Player(2, 'o')
    id = None
    current_turn = None
    winner = None

    def __init__(self):
        self.id: int = random.randint(1, 100)
        self.turn_history = []
        self.grid = Board(3, 3,2)
        self.current_turn = 0

    # TODO:
    #  input validation,
    #  print whole history of a game,
    #  check for win or draw,
    #  testing
    # def run(self):
    #     current_turn = 1
    #     while True:
    #         turn = Turn()
    #         turn.make(self.player_1, self.grid)
    #         turn.update_grid(self.player_1, self.grid)
    #         self.grid.render()
    #         turn.check_win_or_draw(self.grid)
    #         turn.make(self.player_2, self.grid)
    #         turn.update_grid(self.player_2, self.grid)
    #         self.grid.render()
    #         turn.check_win_or_draw(self.grid)
    #         self.turn_history.append(turn)
    #         current_turn = current_turn + 1
    #         if current_turn > 9:
    #             exit()
    #         # print(self.turn_history)

    def get_state(self) -> dict:
        current_player_name = ''
        if self.current_player is not None:
            current_player_name = self.current_player.name
        result = {'id': self.id, 'player1Name': self.player_1.name, 'player2Name': self.player_2.name, 'grid': self.grid, 'currentPlayerName': current_player_name,
                  'player1Symbol': self.player_1.symbol, 'player2Symbol': self.player_2.symbol}
        if self.winner is not None:
            self.grid.disable_all_fields()
            result["winner"] = self.winner_value_to_player(self.winner)
        return result

    def winner_value_to_player(self, winner):
        if self.player_1.symbol == winner:
            return self.player_1.name
        return self.player_2.name

    def reset_state(self, current_player_number) -> None:
        if current_player_number == 1:
            self.current_player = self.player_1
        else:
            self.current_player = self.player_2
        self.winner = None
        self.current_turn = 0

# Game().run()
