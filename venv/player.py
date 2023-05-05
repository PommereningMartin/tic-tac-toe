class Player(object):

    def __init__(self, player_number: int):
        self.name = None
        # self.ask_name(player_number)

    def ask_name(self, number: int) -> None:
        print("Pls add Name for Player {0}".format(number))
        self.name = input()

    def get_name(self) -> str:
        return self.name
