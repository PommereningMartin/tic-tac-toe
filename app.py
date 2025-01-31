import sqlite3

from flask import request, redirect, render_template, url_for, Flask
from flask_cors import CORS
from flask_dance.contrib.google import google
from flask_login import login_required, logout_user, login_user, current_user
from oauthlib.oauth2 import TokenExpiredError

from auth import google_blueprint
from game_service import game_service
from models import login_manager, User, db

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.register_blueprint(google_blueprint, url_prefix="/login")
CORS(app)
login_manager.init_app(app)
users = []



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
        user = User(res.json()["name"])
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS USER(username varchar(255), id int primary key);")
        sql = """INSERT INTO USER VALUES ('{0}', {1})""".format(user.username, user.id)
        cur.execute(sql)
        con.commit()
        login_user(user)
        return redirect(url_for("dashboard"))
    except TokenExpiredError as e:
        return redirect(url_for("google.login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", players=users, games=[], current_user=current_user)

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
@login_required
def main():
    if not google.authorized:
        return redirect(url_for("index"))
    return render_template("main.html", users=[])

@app.route("/reset", methods=["POST"])
@login_required
def reset():
    # TODO type reset request params
    # TODO: pass data into GameService to not fiddle with data here
    data = request.json
    game_id = data['gameId']
    current_player_number = data['currentPlayer']
    game_service.reset(game_id, current_player_number)
    return render_template('game.html', game=game_service.get_state(game_id))


@app.route("/makeTurn", methods=["POST"])
@login_required
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
@login_required
def create_user():
    # users.append({"id": random.randint(1, 1000), "name": random.randbytes(10).hex()})
    return []


@app.route("/startGame", methods=["POST"])
@login_required
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
@login_required
def game():
    args = request.args
    # TODO: validate that gameId is allways an int -> throw 500 if not
    game_id = int(args['gameId'])
    return render_template('game.html', game=game_service.game(game_id).get_state())


if __name__ == "__main__":
    app.run()
