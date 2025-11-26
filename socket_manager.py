from flask_socketio import SocketIO
from events import GameEvents

class SocketManager(object):
    def __init__(self, app, active_game_rooms, game_service, logger):
        self.socketio = SocketIO(app)
        self.events = GameEvents(active_game_rooms, game_service, logger)
        self.register_handlers()
        self.logger = logger

    def register_handlers(self):
        @self.socketio.on("connect")
        def connect():
            return self.events.handle_connect()

        @self.socketio.on("disconnect")
        def disconnect():
            return self.events.handle_disconnect()

        @self.socketio.on("join_game")
        def join_game(data):
            return self.events.handle_join_game(data)

        @self.socketio.on("leave_game")
        def leave_game(data):
            return self.events.handle_leave_game(data)

        @self.socketio.on("game_event")
        def game_event(data):
            return self.events.handle_game_event(data)

        @self.socketio.on("make_turn")
        def make_turn(data):
            return self.events.make_turn(data)

    def run(self, app, **kwargs):
            self.socketio.run(app,**kwargs)