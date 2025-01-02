
import os

from sqlalchemy.exc import NoResultFound

from models import OAuth, db, User
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user, current_user

google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_ID"),
    client_secret=os.getenv("GOOGLE_SECRET"),
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    info = google.get("/oauth2/v2/userinfo")
    if info.ok:
        account_info = info.json()
        username = account_info["name"]

        query = User.query.filter_by(username=username)
        print('DEBUG QUERY', query)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            print('USER_THINGY:', user)
            db.session.add(user)
            db.session.commit()
        login_user(user)