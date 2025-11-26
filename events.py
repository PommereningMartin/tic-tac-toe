# events.py
from datetime import datetime

from flask import session
from flask_socketio import emit, join_room, leave_room


class GameEvents:
    def __init__(self, active_game_rooms, game_service, logger):
        self.active_game_rooms = active_game_rooms
        self.game_service = game_service
        self.logger = logger
        # Configure logging

    def get_user_from_session(self):
        return session.get("user")

    def is_user_logged_in(self):
        return "user" in session

    def handle_connect(self):
        if not self.is_user_logged_in():
            return False

        user = self.get_user_from_session()
        self.logger.info(f"Socket connected: {user['email']}")

    def handle_disconnect(self):
        """Handle client disconnection."""
        if self.is_user_logged_in():
            user = self.get_user_from_session()
            self.logger.info(f"Socket disconnected: {user['email']}")

    def handle_join_game(self, data):
        if not self.is_user_logged_in():
            return

        user = self.get_user_from_session()
        room_id = data.get("room_id")

        if not room_id or room_id not in self.active_game_rooms:
            emit("error", {"data": "Room not found!"})
            return

        join_room(room_id)

        if user["email"] not in self.active_game_rooms[room_id]["players"]:
            self.active_game_rooms[room_id]["players"].append(user["email"])

        emit("message", {
            "data": f"{user['name']} joined the game!",
            "user": user["email"],
            "timestamp": datetime.now().isoformat()
        }, room=room_id)

        emit("game_state", {
            "room_id": room_id,
            "players": self.active_game_rooms[room_id]["players"],
            "game_state": self.active_game_rooms[room_id]["game_state"],
            "timestamp": datetime.now().isoformat()
        })

        self.logger.info(f"User {user['email']} joined game room {room_id}")

    def handle_leave_game(self, data):
        if not self.is_user_logged_in():
            return

        user = self.get_user_from_session()
        room_id = data.get("room_id")

        if not room_id or room_id not in self.active_game_rooms:
            emit("error", {"data": "Room not found!"})
            return

        leave_room(room_id)

        if user["email"] in self.active_game_rooms[room_id]["players"]:
            self.active_game_rooms[room_id]["players"].remove(user["email"])

        emit("message", {
            "data": f"{user['name']} left the game!",
            "user": user["email"],
            "timestamp": datetime.now().isoformat()
        }, room=room_id)

        if not self.active_game_rooms[room_id]["players"]:
            self.logger.info(f"Game room {room_id} is now empty")

        self.logger.info(f"User {user['email']} left game room {room_id}")

    def handle_game_event(self, data):
        """Handle game events within a room."""
        if not self.is_user_logged_in():
            return

        user = self.get_user_from_session()
        room_id = data.get("room_id")
        event_data = data.get("event")

        if not room_id or room_id not in self.active_game_rooms:
            emit("error", {"data": "Room not found!"})
            return

        if user["email"] not in self.active_game_rooms[room_id]["players"]:
            emit("error", {"data": "You are not in this game room!"})
            return

        emit("text_update", {
            "data": event_data,
            "user": user["email"],
            "user_name": user["name"],
            "timestamp": datetime.now().isoformat()
        }, room=room_id)

        self.logger.info(f"Game event in room {room_id} by {user['email']}: {event_data}")

    def make_turn(self, data):
        game_id = data['game_id']
        room_id = data['room_id']
        field_id = data['field_id']
        foo = self.game_service.make_turn(game_id, field_id)
        print(foo)
        user = self.get_user_from_session()

        # Render the template fragment
        from flask import render_template
        html = render_template(
            "foo.html",
            game=foo.get_state(),
            user=session["user"]
        )

        # Send the rendered HTML back to the client
        emit("game_update", {"html": html}, room=room_id)