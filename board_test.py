import unittest

from parameterized import parameterized

from board import Board


class TestBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.is_space_empty_board = Board(2, 2)
        cls.is_space_empty_board.set_value(0, 0, 'foo')
        cls.is_space_empty_board.set_value(1, 1, 'bar')

    def test_init(self):
        board = Board(3, 3)
        self.assertEqual(board, [
            [{'value': None, 'isEnabled': True}, {'value': None, 'isEnabled': True}, {'value': None, 'isEnabled': True}],
            [{'value': None, 'isEnabled': True}, {'value': None, 'isEnabled': True}, {'value': None, 'isEnabled': True}],
            [{'value': None, 'isEnabled': True}, {'value': None, 'isEnabled': True}, {'value': None, 'isEnabled': True}]])




    @parameterized.expand([
        ((0,0), False),
        ((1,1), False),
        ((0,1), True),
        ((1,0), True),
    ])
    def test_is_space_empty(self, coordinate, expected):
        row_index, col_index = coordinate
        self.assertEqual(self.is_space_empty_board.is_space_empty(row_index, col_index), expected)

    def test_has_winner_false(self):
        board = Board(3, 3)
        self.assertFalse(board.has_winner())

if __name__ == '__main__':
    unittest.main()
