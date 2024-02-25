import http

import flask
from flask import request, redirect, render_template, url_for
from game import Game
from game_service import GameService

app = flask.Flask(__name__)
gameService = GameService()
foo_bar: Game


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/reset", methods=["POST"])
def reset():
    global foo_bar
    gameService.reset_grid(foo_bar.id)
    return redirect(url_for('game'))


@app.route("/setSomething", methods=["POST"])
def set_something():
    global foo_bar
    if request.method == 'POST':
        bar = request.json
        print('bar', bar)
        print('fooBar',type(bar['field']))
        print(bar['field'])
        x,y = tuple(map(int, bar['field'].replace("(", "").replace(")", "").split(",")))
        # x,y = tuple(map(int, bar['field']))
        print('coordinates',x,y)
        if foo_bar.current_player == foo_bar.player_1:
            foo_bar.grid[x][y]['value'] = foo_bar.player_1.symbol
            foo_bar.current_player = foo_bar.player_2
        else:
            foo_bar.grid[x][y]['value'] = foo_bar.player_2.symbol
            foo_bar.current_player = foo_bar.player_1
        foo_bar.grid[x][y]['isEnabled'] = False
        print(foo_bar.grid)
        return foo_bar.grid
    return {}


@app.route("/startGame", methods=["POST"])
def start():
    global foo_bar
    foo_bar = gameService.new_game()
    if request.method == 'POST':
        foo_bar.player_1.name = request.json['player1Name']
        foo_bar.player_2.name = request.json['player2Name']
        current_player_start = request.json['currentPlayer']
        print('GAME',game)
        if current_player_start == 1:
            foo_bar.current_player = foo_bar.player_1
        else:
            foo_bar.current_player = foo_bar.player_2
        return redirect(url_for('game'))
    return {}


@app.route("/game")
def game():
    global foo_bar
    return render_template('game.html', game=foo_bar.get_state())


if __name__ == "__main__":
    app.run(debug=True)
