
import os

from flask_dance.contrib.google import make_google_blueprint

google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_ID"),
    client_secret=os.getenv("GOOGLE_SECRET"),
)