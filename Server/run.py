from flask import Flask
from auth import auth_bp
from db import init_db
import os

api = Flask(__name__)
api.config.from_object('Server.config')
api.register_blueprint(auth_bp, url_prifix='/api')


def main():
    init_db()
    api.run(debug=True)

if __name__ == '__main__':
    main()
