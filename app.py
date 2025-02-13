import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import request, redirect, render_template, url_for, Flask, flash, session
from flask_dance.contrib.google import google
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from auth import google_blueprint
from game_service import game_service

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# OAuth 2.0 client setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
    },
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=None,
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.Enum('user', 'admin'), default='user')

# Create all database tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Store the next parameter in session
    if 'next' in request.args:
        session['next'] = request.args['next']

    try:
        redirect_uri = url_for('callback', _external=True)
        logger.debug(f"Redirect URI: {redirect_uri}")
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        flash('An error occurred during login. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/callback')
def callback():
    try:
        # Get token
        token = google.authorize_access_token()

        # Get user info using the correct endpoint
        resp = google.get('https://openidconnect.googleapis.com/v1/userinfo')
        user_info = resp.json()
        logger.debug(f"User info received: {json.dumps(user_info, indent=2)}")

        # Find or create user
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                google_id=user_info['sub'],
                email=user_info['email'],
                name=user_info.get('name'),
                picture=user_info.get('picture')
            )
            db.session.add(user)
        else:
            user.name = user_info.get('name')
            user.picture = user_info.get('picture')
            user.last_login = datetime.utcnow()

        db.session.commit()
        login_user(user)

        # Redirect to next URL if stored in session
        next_url = session.pop('next', None)
        return redirect(next_url or url_for('dashboard'))

    except Exception as e:
        logger.error(f"Error during callback: {str(e)}")
        flash('Authentication failed. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", players=[], games=[], current_user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
@login_required
def main():
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

# Debug route
@app.route('/debug')
def debug():
    if app.debug:
        return {
            'client_id_set': bool(os.getenv('GOOGLE_CLIENT_ID')),
            'client_secret_set': bool(os.getenv('GOOGLE_CLIENT_SECRET')),
            'redirect_uri': url_for('callback', _external=True),
            'routes': [str(rule) for rule in app.url_map.iter_rules()]
        }
    return 'Debug information not available in production'

if __name__ == "__main__":
    app.run(debug=os.getenv('DEBUG'), host=os.getenv('HOST'), port=os.getenv('PORT'))
