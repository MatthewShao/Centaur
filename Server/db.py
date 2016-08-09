from mongoengine import connect
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS


def init_db():
    connect(DB_NAME, host=DB_HOST, username=DB_USER, password=DB_PASS)