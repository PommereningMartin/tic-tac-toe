from flask_socketio import SocketIO, emit, join_room, leave_room

bar = None


def init_io(app):
    bar = app


socketio = SocketIO(bar)


@socketio.on("connect")
def handle_connect(self):
    print('This thingy works!')
    #if not is_user_logged_in():
    #    return False

    #user = get_user_from_session()
    # logger.info(f"Socket connected: {user['email']}")

    # @socketio.on("disconnect")
    # def handle_disconnect():
    #     """Handle client disconnection."""
    #     if is_user_logged_in():
    #         user = get_user_from_session()
    #         logger.info(f"Socket disconnected: {user['email']}")
    #
    #
    # @socketio.on("join_game")
    # def handle_join_game(data):
    #     if not is_user_logged_in():
    #         return
    #
    #     user = get_user_from_session()
    #     room_id = data.get("room_id")
    #
    #     if not room_id or room_id not in active_game_rooms:
    #         emit("error", {"data": "Room not found!"})
    #         return
    #
    #     join_room(room_id)
    #
    #     if user["email"] not in active_game_rooms[room_id]["players"]:
    #         active_game_rooms[room_id]["players"].append(user["email"])
    #
    #     emit("message", {
    #         "data": f"{user['name']} joined the game!",
    #         "user": user["email"],
    #         "timestamp": datetime.now().isoformat()
    #     }, room=room_id)
    #
    #     emit("game_state", {
    #         "room_id": room_id,
    #         "players": active_game_rooms[room_id]["players"],
    #         "game_state": active_game_rooms[room_id]["game_state"],
    #         "timestamp": datetime.now().isoformat()
    #     })
    #
    #     logger.info(f"User {user['email']} joined game room {room_id}")
    #
    #
    # @socketio.on("leave_game")
    # def handle_leave_game(data):
    #     if not is_user_logged_in():
    #         return
    #
    #     user = get_user_from_session()
    #     room_id = data.get("room_id")
    #
    #     if not room_id or room_id not in active_game_rooms:
    #         emit("error", {"data": "Room not found!"})
    #         return
    #
    #     leave_room(room_id)
    #
    #     if user["email"] in active_game_rooms[room_id]["players"]:
    #         active_game_rooms[room_id]["players"].remove(user["email"])
    #
    #     emit("message", {
    #         "data": f"{user['name']} left the game!",
    #         "user": user["email"],
    #         "timestamp": datetime.now().isoformat()
    #     }, room=room_id)
    #
    #     if not active_game_rooms[room_id]["players"]:
    #         logger.info(f"Game room {room_id} is now empty")
    #
    #     logger.info(f"User {user['email']} left game room {room_id}")
    #
    #
    # @socketio.on("game_event")
    # def handle_game_event(data):
    #     """Handle game events within a room."""
    #     if not is_user_logged_in():
    #         return
    #
    #     user = get_user_from_session()
    #     room_id = data.get("room_id")
    #     event_data = data.get("event")
    #
    #     if not room_id or room_id not in active_game_rooms:
    #         emit("error", {"data": "Room not found!"})
    #         return
    #
    #     # Check if user is in the room
    #     if user["email"] not in active_game_rooms[room_id]["players"]:
    #         emit("error", {"data": "You are not in this game room!"})
    #         return
    #
    #     # Broadcast the event to all users in the room
    #     emit("game_update", {
    #         "data": event_data,
    #         "user": user["email"],
    #         "user_name": user["name"],
    #         "timestamp": datetime.now().isoformat()
    #     }, room=room_id)
    #
    #     logger.info(f"Game event in room {room_id} by {user['email']}: {event_data}")
    #
    # @socketio.on("make_turn")
    # def make_turn(data):
    #     game_id = data['game_id']
    #     room_id = data['room_id']
    #     field_id = data['field_id']
    #     foo = game_service.make_turn(game_id, field_id)
    #     print(foo)
    #     user = get_user_from_session()
    #     # Render the template fragment
    #     html = render_template(
    #         "foo.html",
    #         game=foo.get_state(),
    #         user=session["user"]
    #     )
    #
    #     # Send the rendered HTML back to the client
    #     emit("game_update", {"html": html}, room=room_id)
