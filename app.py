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
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy


import auth
from game_service import game_service, GameService
from socket_manager import SocketManager
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


# OAuth 2.0 client setup
google = auth.register(app)
waiting_room = WaitingRoom()
logged_in_users = {}
active_game_rooms = {}
socket_manager = SocketManager(app, active_game_rooms, game_service, logger)

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

@app.route("/")
def index():
    return render_template("index.html", user=session.get('user'))

@app.route("/login")
def login():
    if is_user_logged_in():
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
            logged_in_users[foo] = session["user"]
        else:
            user.name = user_info.get('name')
            user.picture = user_info.get('picture')
            user.last_login = datetime.utcnow()
        db.session.commit()
        #login_user(user)
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
def dashboard():
    return render_template("dashboard.html", players=[], rooms=active_game_rooms, user=session.get('user'), games=[])

@app.route("/logout")
def logout():
    if not is_user_logged_in():
        return
    return redirect(url_for("index"))

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
    return redirect(url_for("game_room", room_id=room_id))


@app.route("/game/<room_id>")
def game_room(room_id):
    if not is_user_logged_in():
        return redirect(url_for("login"))

    user = get_user_from_session()

    if room_id not in active_game_rooms:
        return render_template("error.html", message="Game room not found!"), 404

    if user["email"] not in active_game_rooms[room_id]["players"]:
        active_game_rooms[room_id]["players"].append(user["email"])

    game = game_service.new()
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


if __name__ == "__main__":
    socket_manager.run(app, debug=True, host=os.getenv('HOST)'), port=os.getenv('PORT'))
