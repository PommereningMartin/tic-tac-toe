import flask
from flask import request, redirect, render_template, url_for
from game_service import game_service

app = flask.Flask(__name__)
test = []
turn = 0


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    game_id = data['gameId']
    current_player = data['currentPlayer']
    game_service.reset_grid(game_id)
    game = game_service.game(game_id)
    game.reset_state(current_player)
    game_state = game.get_state()
    print('reset game state', game_state)
    return render_template('game.html', game=game_state)


@app.route("/setSomething", methods=["POST"])
def set_something():
    print('222222', game_service.games)
    if request.method == 'POST':
        data = request.json
        current_game = game_service.game(data['gameId'])
        print(current_game)
        x, y = tuple(map(int, data['field'].replace("(", "").replace(")", "").split(",")))
        # x,y = tuple(map(int, bar['field']))
        print('coordinates', x, y)
        if current_game.current_player == current_game.player_1:
            current_game.grid[x][y]['value'] = current_game.player_1.symbol
            current_game.current_player = current_game.player_2
        else:
            current_game.grid[x][y]['value'] = current_game.player_2.symbol
            current_game.current_player = current_game.player_1
        current_game.grid[x][y]['isEnabled'] = False
        current_game.current_turn += 1
        if current_game.current_turn >= 5:
            print('Winner: ',current_game.grid.has_winner())
            current_game.winner = current_game.grid.has_winner()
        return current_game.get_state()
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
