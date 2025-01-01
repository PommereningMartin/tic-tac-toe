from game import Game
from board import Board
from game_state import GameState


class GameService:
    games: {int: Game} = {}

    def __int__(self):
        pass

    def new(self) -> Game:
        brand_new_game: Game = Game()
        self.games[brand_new_game.id] = brand_new_game
        return brand_new_game

    def game(self, game_id: int) -> Game:
        if self.games.__contains__(game_id):
            return self.games.get(game_id)
        raise ValueError('A Game with id {} is not running!'.format(game_id))

    def reset_grid(self, game_id):
        int_game_id = int(game_id)
        if self.games.__contains__(int_game_id):
            self.game(int_game_id).board = Board(3, 3)
        else:
            raise ValueError('Could not find a game for reset!')

    def reset_state(self, game_id: int, current_player_number: int) -> None:
        game = self.game(game_id)
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

    def player_value_to_grid_value(self, game_id: int, x: int, y: int):
        game = self.game(game_id)
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

    def reset(self, game_id: int, current_player_number: int) -> None:
        self.reset_grid(game_id)
        self.reset_state(game_id, current_player_number)

    def make_turn(self, game_id: int, field: str):
        x, y = self.field_to_coordinates(field)
        self.player_value_to_grid_value(game_id, x, y)
        self.increase_turn(game_id)

    def check_winner(self, game_id: int):
        game = self.game(game_id)
        if game.current_turn >= 5:
            print(00000, game.board.check_winner())
            game.winner = game.board.has_winner()


game_service = GameService()
