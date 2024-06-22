import unittest
from game_service import game_service as gs


class GameServiceTest(unittest.TestCase):
    """
    gs.games datastructure

    games = {1: Game, 2: Game}
    """
    def test_create_game(self):
        game_1 = gs.new()
        game_2 = gs.new()

        self.assertNotEqual(gs.games, {})
        self.assertEqual(len(gs.games), 2)
        self.assertNotEqual(game_1, game_2)
        self.assertNotEqual(game_1.id, game_2.id)
        self.assertTrue(gs.games.__contains__(game_1.id))
        self.assertTrue(gs.games.__contains__(game_2.id))
        self.assertTrue(gs.games.get(game_1.id) == game_1)
        self.assertTrue(gs.games.get(game_2.id) == game_2)
        self.assertFalse(gs.games.get(game_1.id) == game_2)


if __name__ == '__main__':
    unittest.main()
