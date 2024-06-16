from game import Game
from game import Game
from board import Board


class GameService:
    games: {int: Game} = {}

    def __int__(self):
        pass

    def new_game(self) -> Game:
        brand_new_game: Game = Game()
        self.games[brand_new_game.id] = brand_new_game
        return brand_new_game

    def game(self, game_id: str) -> Game:
        int_game_id = int(game_id)
        if self.games.__contains__(int_game_id):
            return self.games.get(int_game_id)
        assert 'No Game running!'

    def reset_grid(self, game_id):
        int_game_id = int(game_id)
        if self.games.__contains__(int_game_id):
            print('boardId',self.games.get(int_game_id).grid.id)
            self.games.get(int_game_id).grid = Board(3, 3, 2)
            print('boardId',self.games.get(int_game_id).grid.id)
        assert 'Could not find a game for reset!'


game_service = GameService()
