from player import Player


class Bot(Player):

    def __init__(self, player_number: int, symbol: str):
        super().__init__(player_number, symbol)
