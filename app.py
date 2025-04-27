import json
import logging
import os
import random
import string
import uuid
from datetime import datetime

from dotenv import load_dotenv
from flask import request, redirect, render_template, url_for, Flask, flash, session, jsonify
from flask_cors import CORS
from flask_dance.contrib.google import google
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from auth import google_blueprint
from game_service import game_service, GameService
from waiting_room import WaitingRoom

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
CORS(app)
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

users = []
waiting_room = WaitingRoom()

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

    def to_dict(self):
        return {
            'id': self.id,
            'google_id': self.google_id,
            'email': self.email,
            'name': self.name,
            'picture': self.picture,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'role': self.role
        }

# Create all database tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

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
            session["user"] = {
                "email": user_info["email"],
                "name": user_info.get("name", "User"),
                "picture": user_info.get("picture", ""),
                "sub": user_info["sub"]  # Unique Google ID
            }
            db.session.add(user)
            # Add to logged in users
            foo = user_info.get('email')
            print(session.__dir__())
            logged_in_users[foo] = session["user"]
        else:
            user.name = user_info.get('name')
            user.picture = user_info.get('picture')
            user.last_login = datetime.utcnow()
        db.session.commit()
        login_user(user)
        session["user"] = {
            "email": user_info["email"],
            "name": user_info.get("name", "User"),
            "picture": user_info.get("picture", ""),
            "sub": user_info["sub"]  # Unique Google ID
        }
        logged_in_users[user_info["email"]] = session["user"]
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
    return render_template("dashboard.html", players=users, rooms=active_game_rooms, user=None, games=[], current_user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
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
    foo = create_random_user()
    users.append(foo)
    return foo.to_dict()

@app.route("/clearPlayers", methods=["POST"])
@login_required
def clear_players():
    users.clear()
    return []

@app.route("/startGame", methods=["POST"])
@login_required
def start():
    new_game = game_service.new()
    if len(users) > 0:
        new_game.player_1.name = users[0].name
        new_game.player_2.name = users[1].name
        users.pop(0)
        users.pop(0)
    if request.method == 'POST':
        current_player_start = request.json['currentPlayer']
        print('current player start', request.json['currentPlayer'])
        game_service.reset_current_player(new_game, current_player_start)
        return redirect(url_for('game', gameId=new_game.id))
    return {}

@app.route("/game")
@login_required
def game():
    args = request.args
    game_id = int(args['gameId'])
    return render_template('game.html', game=game_service.game(game_id).get_state())

def create_random_user():
    random_google_id = ''.join(random.choices(string.digits, k=21))

    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    random_email = f"{random_string}@example.com"

    random_name = ''.join(random.choices(string.ascii_lowercase, k=6)).capitalize()

    new_user = User(
        google_id=random_google_id,
        email=random_email,
        name=random_name,
        picture="https://example.com/default-avatar.png",
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow(),
        is_active=True,
        role='user'
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        return None

from flask_socketio import SocketIO, emit, join_room, leave_room

socketio = SocketIO(app)

logged_in_users = {}
active_game_rooms = {}


def get_user_from_session():
    return session.get("user")


def is_user_logged_in():
    return "user" in session


def create_game_room(creator_email):
    room_id = str(uuid.uuid4())
    active_game_rooms[room_id] = {
        "created_at": datetime.now().isoformat(),
        "players": [creator_email],
        "game_state": "waiting",  # waiting, in_progress, completed
        "creator": creator_email
    }
    return room_id


def clean_inactive_rooms():
    to_remove = []
    for room_id, room_data in active_game_rooms.items():
        if not room_data["players"]:
            to_remove.append(room_id)

    for room_id in to_remove:
        del active_game_rooms[room_id]

    if to_remove:
        logger.info(f"Cleaned {len(to_remove)} inactive game rooms")


@app.route("/start_game")
def start_game():
    if not is_user_logged_in():
        return redirect(url_for("login"))

    user = get_user_from_session()
    room_id = create_game_room(user["email"])
    logger.info(f"New game room created: {room_id} by {user['email']}")
    return redirect(url_for("game_room", room_id=room_id, user=user))


@app.route("/game/<room_id>")
def game_room(room_id):
    if not is_user_logged_in():
        return redirect(url_for("login"))

    user = get_user_from_session()

    if room_id not in active_game_rooms:
        return render_template("error.html", message="Game room not found!"), 404

    if user["email"] not in active_game_rooms[room_id]["players"]:
        active_game_rooms[room_id]["players"].append(user["email"])

    # create a new game for the room
    game = game_service.new(room_id)
    return render_template("gameV2.html", room_id=room_id, user=user,game=game.get_state(), room_data=active_game_rooms[room_id])


@app.route("/api/rooms")
def list_rooms():
    if not is_user_logged_in():
        return jsonify({"error": "Not logged in"}), 401

    clean_inactive_rooms()
    return jsonify({"rooms": active_game_rooms})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="Server error. Please try again later."), 500


@socketio.on("connect")
def handle_connect():
    if not is_user_logged_in():
        return False

    user = get_user_from_session()
    logger.info(f"Socket connected: {user['email']}")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection."""
    if is_user_logged_in():
        user = get_user_from_session()
        logger.info(f"Socket disconnected: {user['email']}")


@socketio.on("join_game")
def handle_join_game(data):
    if not is_user_logged_in():
        return

    user = get_user_from_session()
    room_id = data.get("room_id")

    if not room_id or room_id not in active_game_rooms:
        emit("error", {"data": "Room not found!"})
        return

    join_room(room_id)

    if user["email"] not in active_game_rooms[room_id]["players"]:
        active_game_rooms[room_id]["players"].append(user["email"])

    emit("message", {
        "data": f"{user['name']} joined the game!",
        "user": user["email"],
        "timestamp": datetime.now().isoformat()
    }, room=room_id)

    emit("game_state", {
        "room_id": room_id,
        "players": active_game_rooms[room_id]["players"],
        "game_state": active_game_rooms[room_id]["game_state"],
        "timestamp": datetime.now().isoformat()
    })

    logger.info(f"User {user['email']} joined game room {room_id}")


@socketio.on("leave_game")
def handle_leave_game(data):
    if not is_user_logged_in():
        return

    user = get_user_from_session()
    room_id = data.get("room_id")

    if not room_id or room_id not in active_game_rooms:
        emit("error", {"data": "Room not found!"})
        return

    leave_room(room_id)

    if user["email"] in active_game_rooms[room_id]["players"]:
        active_game_rooms[room_id]["players"].remove(user["email"])

    emit("message", {
        "data": f"{user['name']} left the game!",
        "user": user["email"],
        "timestamp": datetime.now().isoformat()
    }, room=room_id)

    if not active_game_rooms[room_id]["players"]:
        logger.info(f"Game room {room_id} is now empty")
        clean_inactive_rooms()

    logger.info(f"User {user['email']} left game room {room_id}")


@socketio.on("game_event")
def handle_game_event(data):
    if not is_user_logged_in():
        return

    user = get_user_from_session()
    room_id = data.get("room_id")
    event_data = data.get("event")

    if not room_id or room_id not in active_game_rooms:
        emit("error", {"data": "Room not found!"})
        return

    # Check if user is in the room
    if user["email"] not in active_game_rooms[room_id]["players"]:
        emit("error", {"data": "You are not in this game room!"})
        return

    # Broadcast the event to all users in the room
    emit("game_update", {
        "data": event_data,
        "user": user["email"],
        "user_name": user["name"],
        "timestamp": datetime.now().isoformat()
    }, room=room_id)

    logger.info(f"Game event in room {room_id} by {user['email']}: {event_data}")

@socketio.on("make_turn")
def make_turn(data):
    room_id = data['room_id']
    field_id = data['field_id']
    foo = game_service.make_turn(room_id, field_id).get_state()

    # Render the template fragment
    html = render_template(
        "foo.html",
        game=foo,
        user=session["user"]
    )
    emit("game_update", {"html": html}, room=room_id)


if __name__ == "__main__":
    socketio.run(app, debug=True, host=os.getenv('HOST)'), port=os.getenv('PORT'))
