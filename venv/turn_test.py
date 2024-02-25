from turn import Turn
from grid import Grid

import unittest

foo = Turn()
grid = Grid(3, 3)
foo.grid = grid


class TestSum(unittest.TestCase):

    def test_foo(self):
        foo.check_win_or_draw()

        foo.grid[1][1] = "x"
        foo.check_win_or_draw()


if __name__ == '__main__':
    unittest.main()
