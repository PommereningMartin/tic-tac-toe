from random import randint

from game import Game
from board import Board
from game_state import GameState


class GameService:
    games: {str: Game} = {}

    def __int__(self):
        pass

    def new(self, room_id: str) -> Game:
        brand_new_game: Game = Game(room_id)
        self.games[brand_new_game.room_id] = brand_new_game
        return brand_new_game

    def game(self, room_id: str) -> Game:
        if room_id in self.games:
            return self.games.get(room_id)
        raise ValueError('A Game with room_id {} is not running!'.format(room_id))

    def reset_grid(self, room_id: str) -> None:
        if room_id in self.games:
            self.game(room_id).board = Board(3, 3)
        else:
            raise ValueError('Could not find a game for room_id {} reset!'.format(room_id))

    def reset_state(self, room_id: str, current_player_number: int) -> None:
        game = self.game(room_id)
        self.reset_current_player(game, current_player_number)
        game.winner = None
        game.current_turn = 0

    @staticmethod
    def reset_current_player(game: Game, current_player_number: int) -> None:
        if current_player_number == 1:
            game.current_player = game.player_1
        else:
            game.current_player = game.player_2

    def get_state(self, game_id) -> GameState:
        return self.game(game_id).get_state()

    @staticmethod
    def field_to_coordinates(field) -> tuple:
        x, y = tuple(map(int, field.replace("(", "").replace(")", "").split(",")))
        return x, y

    def player_value_to_grid_value(self, room_id: str, x: int, y: int):
        game = self.game(room_id)
        if game.current_player == game.player_1:
            # TODO: add helper function to grid to set a value
            # game.make_turn(x, y, value)
            game.board[x][y]['value'] = game.player_1.symbol
            game.current_player = game.player_2
        else:
            game.board[x][y]['value'] = game.player_2.symbol
            game.current_player = game.player_1
        game.board[x][y]['isEnabled'] = False

    def increase_turn(self, game_id):
        self.game(game_id).current_turn += 1

    def reset(self, room_id: str, current_player_number: int) -> None:
        self.reset_grid(room_id)
        self.reset_state(room_id, current_player_number)

    def make_turn(self, room_id: str, field: str) -> Game:
        x, y = self.field_to_coordinates(field)
        self.player_value_to_grid_value(room_id, x, y)
        self.increase_turn(room_id)
        return self.game(room_id)

    def check_winner(self, room_id: str):
        game = self.game(room_id)
        if game.current_turn >= 5:
            game.winner = game.board.has_winner()


game_service = GameService()
