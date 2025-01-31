import random
import sqlite3

from flask_login import LoginManager, UserMixin
from tinydb import Query, TinyDB, where

users = []
db = TinyDB('./db.json')

class User(UserMixin):
    # TODO:
    #  expand user fields
    #  add more helper function for read/write
    id: int
    name: str

    def __init__(self, name, id=None):
        self.id = random.randint(1, 10000000) if id is None else id
        self.name = name
        self.username = name

    def get_id(self):
        return str(self.id)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    results = cur.execute("""SELECT * FROM USER WHERE id = {0}""".format(user_id)).fetchall()
    name, id = results[0]
    return User(name, id=id)
