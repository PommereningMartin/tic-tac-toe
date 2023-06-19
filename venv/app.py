import http

import flask
from flask import request, redirect, render_template, url_for
from game import Game

app = flask.Flask(__name__)
global game


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/setSomething", methods=["POST"])
def setSometing():
    if request.method == 'POST':
        bar = request.json
        print('bar', bar)
        print('fooBar',type(bar['field']))
        print(bar['field'])
        x,y = tuple(map(int, bar['field'].replace("(", "").replace(")", "").split(",")))
        # x,y = tuple(map(int, bar['field']))
        print('coordinates',x,y)
        if game.current_player == 1:
            game.grid[x][y]['value'] = game.player_1.symbol
            game.current_player = 2
        else:
            game.grid[x][y]['value'] = game.player_2.symbol
            game.current_player = 1
        game.grid[x][y]['isEnabled'] = False
        print(game.grid)
        return game.grid
    return {}

@app.route("/startGame", methods=["POST"])
def start():
    global game
    game = Game()
    if request.method == 'POST':
        game.player_1.name = request.json['player1Name']
        game.player_2.name = request.json['player2Name']
        game.current_player = request.json['currentPlayer']
        return redirect(url_for('game'))
    return {}


@app.route("/game")
def game():
    return render_template('game.html', game=game.get_state())


if __name__ == "__main__":
    app.run(debug=True)
