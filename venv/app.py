import flask
from flask import request, redirect, render_template, url_for
from game_service import game_service

app = flask.Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


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


@app.route("/startGame", methods=["POST"])
def start():
    foo_bar = game_service.new_game()
    if request.method == 'POST':
        foo_bar.player_1.name = request.json['player1Name']
        foo_bar.player_2.name = request.json['player2Name']
        current_player_start = request.json['currentPlayer']
        print('current player start',request.json['currentPlayer'])
        if current_player_start == 1:
            foo_bar.current_player = foo_bar.player_1
        else:
            foo_bar.current_player = foo_bar.player_2
        return redirect(url_for('game', gameId=foo_bar.id))
    return {}


@app.route("/game")
def game():
    args = request.args
    gameId = int(args['gameId'])
    return render_template('game.html', game=game_service.game(gameId).get_state())


if __name__ == "__main__":
    app.run()
