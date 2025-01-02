import flask, random

from flask_cors import CORS
from flask import request, redirect, render_template, url_for, session
from flask_dance.contrib.google import google
from flask_login import login_required, logout_user, LoginManager
from oauthlib.oauth2 import TokenExpiredError

from auth import google_blueprint
from game_service import game_service
from models import login_manager, db

app = flask.Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./users.db"
app.register_blueprint(google_blueprint, url_prefix="/login")
CORS(app)
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

"""
TODO:
- refactor users into own service
- let the service handle, add, remove, update
"""


@app.route("/google")
def login():
    try:
        if not google.authorized:
            return redirect(url_for("google.login"))
        res = google.get("/oauth2/v2/userinfo")
        username = res.json()["name"]
    except TokenExpiredError as e:
        return redirect(url_for("google.login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/main")
def main():
    if not google.authorized:
        return redirect(url_for("index"))
    return render_template("main.html", users=[])

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
    # users.append({"id": random.randint(1, 1000), "name": random.randbytes(10).hex()})
    return []


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
        #new_game.player_1.name = users[get_random_element_from_dict()]['name']
        #new_game.player_2.name = users[get_random_element_from_dict()]['name']
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
