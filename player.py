import random


class Player(object):

    def __init__(self, player_number: int, symbol: str):
        self.symbol: str = symbol
        self.input = None
        self.name: str | None = None
        self.id = random.randint(0, 1000)
        self.player_number = player_number

    def name(self) -> str:
        return self.name
