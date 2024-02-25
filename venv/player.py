from typing import Tuple


class Player(object):

    def __init__(self, player_number: int, symbol: str):
        self.symbol = symbol
        self.input = None
        self.name = None
        self.id = player_number
        #self.ask_name(player_number)

    def ask_name(self, number: int) -> None:
        print("Pls add Name for Player {0}".format(number))
        self.name = input()

    def get_name(self) -> str:
        return self.name
