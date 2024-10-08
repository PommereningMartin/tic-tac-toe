import random
from typing import List, NotRequired
from typing import TypedDict
from board import Board
from player import Player
from game_state import GameState


class Game(object):

    def __init__(self):
        self.player_1 = Player(1, 'X')
        self.player_2 = Player(2, 'O')
        self.id: int = random.randint(1, 100)
        # TODO: decided to use board or grid and use it all over the place
        self.grid = Board(3, 3, 2)
        self.current_turn = 0
        self.current_player: Player | None = None
        self.winner: str | None = None

    def get_state(self) -> GameState:
        current_player_name = ''
        if self.current_player is not None:
            current_player_name = self.current_player.name
        result: GameState = {'id': self.id, 'player1Name': self.player_1.name, 'player2Name': self.player_2.name,
                             'grid': self.grid, 'currentPlayerName': current_player_name,
                             'player1Symbol': self.player_1.symbol, 'player2Symbol': self.player_2.symbol}
        if self.winner is not None:
            self.grid.disable_all_fields()
            result['winner'] = self.winner_value_to_player(self.winner)
        return result

    def winner_value_to_player(self, winner) -> str:
        if self.player_1.symbol == winner:
            return self.player_1.name
        return self.player_2.name

# Game().run()
