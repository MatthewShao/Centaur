from mongoengine import connect
from config import db_host, db_name, db_user, db_pass


def init_db():
    connect(db_name, host=db_host, username=db_user, password=db_pass)