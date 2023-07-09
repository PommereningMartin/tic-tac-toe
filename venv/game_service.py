import uuid

from game import Game

foo = dict[uuid, Game]


class GameService(object):

    def __init__(self):
        self.games = {}

    def game(self, id) -> Game:
        print('id', id)
        if id is None:
            foo = uuid.uuid4().__str__()
            game = Game(foo)
            self.games[foo] = game
            return game
        print(self.games.get(id))
        return self.games.get(id)
