from game import Game
from game import Game
from grid import Grid


class GameService:
    games: {int: Game} = {}

    def __int__(self):
        pass

    def new_game(self) -> Game:
        brand_new_game: Game = Game()
        self.games[brand_new_game.id] = brand_new_game
        return brand_new_game

    def game(self, game_id: int) -> Game:
        return self.games[game_id]

    def reset_grid(self, game_id):
        self.games[game_id].grid = Grid(3, 3)
