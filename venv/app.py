import flask
from flask import request, redirect, render_template, url_for

from game import Game
from game_service import GameService

app = flask.Flask(__name__)
game_service = GameService()


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/setSomething", methods=["POST"])
def setSometing():
    if request.method == 'POST':
        data = request.json
        print('data', data)
        game = game_service.game(data['gameId'])
        x, y = tuple(map(int, data['field'].replace("(", "").replace(")", "").split(",")))
        print('coordinates', x, y)
        game.board[x][y]['value'] = game.player_1.symbol
        foo = game.bot.select_move(game.board)
        if foo is not None:
            game.board.make_move(foo[0], foo[1], game.bot)
            game.current_player = game.player_1
            game.board[foo[0]][foo[1]]['isEnabled'] = False
        game.board[x][y]['isEnabled'] = False
        game.board.moves.append([x, y])
        winner = game.board.has_winner()
        print('winner', winner)
        return dict(board=game.board, winner=winner)
    return {}


@app.route("/startGame", methods=["POST"])
def start():
    game = game_service.game(None)
    if request.method == 'POST':
        return redirect(url_for('game', gameId=game.id))
    return {}


@app.route("/game", methods=["GET"])
def game():
    gameId = request.args['gameId']  # counterpart for url_for()
    return render_template('game.html', game=game_service.game(gameId).get_state())


if __name__ == "__main__":
    app.run(debug=True)
