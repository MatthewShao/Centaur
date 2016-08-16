from mongoengine import connect
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS
from pymongo import MongoClient


def init_db():
    connect(DB_NAME, host=DB_HOST, username=DB_USER, password=DB_PASS)

client = MongoClient("mongodb://{}:{}@{}/{}".format(DB_USER, DB_PASS, DB_HOST, DB_NAME))