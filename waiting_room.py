from queue import Queue

from game import Game


class WaitingRoom:
    def __init__(self):
        self.waiting_room = Queue()  # Queue to hold players waiting for a game
        self.active_games = {}  # Dictionary to hold active games

    def add_player(self, player_id):
        self.waiting_room.put(player_id)
        #print(f"Player {player_id} added to the waiting room.")
        self.check_for_game()

    def check_for_game(self):
        """Check if there are enough players to start a game."""
        if self.waiting_room.qsize() >= 2:
            player1 = self.waiting_room.get()
            player2 = self.waiting_room.get()
            game_id = f"game_{player1}_{player2}"
            #print(f"Starting a new game: {game_id} with players {player1} and {player2}")
            self.active_games[game_id] = Game(game_id, player1, player2, self)

    def game_finished(self, game_id, player1, player2):
        #print(f"Game {game_id} finished. Returning players {player1} and {player2} to the waiting room.")
        del self.active_games[game_id]  # Remove the game from active games
        self.add_player(player1)  # Return players to the waiting room
        self.add_player(player2)