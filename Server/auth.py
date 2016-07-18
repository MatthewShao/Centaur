from flask import Blueprint, jsonify, request, g, make_response, current_app
from flask.ext.restful import Api, Resource
from config import SECRET_KEY
from lib.model import User
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from mongoengine import SaveConditionError, ValidationError, NotUniqueError
import jwt


auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)


class Auth(Resource):

    def post(self):
        data = request.get_json(force=True)
        current_app.logger.info(str(data))
        user = User.objects(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            token = create_token(user)
            return {'token': token}
        else:
            response = make_response(
                jsonify({"msg": "Invalid username/password."})
            )
            response.status_code = 401
            return response


class Register(Resource):

    def post(self):
        data = request.get_json(force=True)
        current_app.logger.info(str(data))
        try:
            password = data['password']
            encrypted_pw = generate_password_hash(password)
            user = User(username=data['username'], password=encrypted_pw, email=data['email'])
            user.save()
        except SaveConditionError:
            return make_response(jsonify({"msg":"Register failed."}))
        except ValidationError:
            return make_response(jsonify({"msg":"Email address invalid."}))
        except KeyError:
            return make_response(jsonify({"msg":"Missing field."}))
        except NotUniqueError:
            return make_response(jsonify({"msg":"User existed."}))

        return make_response(jsonify({"objectid":str(user.id)}))


def create_token(user):
    obj = {
        'sub': str(user.id),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(obj, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split(' ')[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header.')
            response.status_code = 401
            return response
        try:
            obj = parse_token(request)
        except jwt.DecodeError:
            response = jsonify(message='Token is invalid.')
            response.status_code = 401
            return response
        g.user_id = obj['sub']
        return func(*args, **kwargs)
    return decorated_function

auth_api.add_resource(Auth, '/login')
auth_api.add_resource(Register, '/register')
