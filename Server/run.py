from flask import Flask
from auth import auth_bp
from job import job_bp
from script import script_bp
from result import result_bp

api = Flask(__name__)
api.config.from_object('Server.config')
api.register_blueprint(auth_bp, url_prefix='/api')
api.register_blueprint(job_bp, url_prefix='/api')
api.register_blueprint(script_bp, url_prefix='/api')
api.register_blueprint(result_bp, url_prefix='/api')


def main():
    api.run(debug=True)

if __name__ == '__main__':
    main()
