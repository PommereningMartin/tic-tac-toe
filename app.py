import flask, random

from flask_cors import CORS
from flask import request, redirect, render_template, url_for
from game_service import game_service

app = flask.Flask(__name__)
CORS(app)
"""
TODO:
- refactor users into own service
- let the service handle, add, remove, update
"""
users = []


@app.route("/")
def index():
    return render_template("index.html", users=users)


@app.route("/reset", methods=["POST"])
def reset():
    # TODO type reset request params
    # TODO: pass data into GameService to not fiddle with data here
    data = request.json
    game_id = data['gameId']
    current_player_number = data['currentPlayer']
    game_service.reset(game_id, current_player_number)
    return render_template('game.html', game=game_service.get_state(game_id))


@app.route("/makeTurn", methods=["POST"])
def make_turn():
    if request.method == 'POST':
        data = request.json
        # TODO type makeTurn request params
        game_id = data['gameId']
        field = data['field']
        game_service.make_turn(game_id, field)
        game_service.check_winner(game_id)
        return game_service.get_state(game_id)
    return {}


@app.route("/createUser", methods=["POST"])
def create_user():
    users.append({"id": random.randint(1, 1000), "name": random.randbytes(10).hex()})
    return users


@app.route("/startGame", methods=["POST"])
def start():
    """
    TODO´s
    - create user
    - put user into que
    - create new game everytime at least 2 users are in the que
      that are not already in a game
    - show list of current users
    :return:
    """
    new_game = game_service.new()
    if request.method == 'POST':
        new_game.player_1.name = users[0]['name']
        new_game.player_2.name = users[1]['name']
        current_player_start = request.json['currentPlayer']
        print('current player start', request.json['currentPlayer'])
        game_service.reset_current_player(new_game, current_player_start)
        return redirect(url_for('game', gameId=new_game.id))
    return {}


@app.route("/game")
def game():
    args = request.args
    # TODO: validate that gameId is allways an int -> throw 500 if not
    game_id = int(args['gameId'])
    return render_template('game.html', game=game_service.game(game_id).get_state())


if __name__ == "__main__":
    app.run()