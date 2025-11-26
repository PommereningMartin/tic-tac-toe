
import os
from authlib.integrations.flask_client import OAuth

def register(app):
    oauth = OAuth(app)
    return oauth.register(
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