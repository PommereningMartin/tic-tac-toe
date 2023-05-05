import http

from flask import Flask, render_template
from game import Game


app = Flask(__name__)
foo = Game()


@app.route("/")
def hello_world():
    return render_template('index.html', grid=foo.grid.get_state())


@app.route("/start", methods=["POST"])
def start():
    foo.run()
    return {}

if __name__ == "__main__":
    app.run(debug=True)
