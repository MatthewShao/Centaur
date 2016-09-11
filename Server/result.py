from flask import Blueprint, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse
from Server.db import client
from Server.config import ITEM_EACH_PAGE
from Server.auth import login_required
from bson.objectid import ObjectId
import json

MARK_LIST = ('success', 'fail')
item_each_page = ITEM_EACH_PAGE


def init_parse():
    parser = reqparse.RequestParser()
    parser.add_argument('mark', type=str)
    parser.add_argument('item_each_page', type=int)
    parser.add_argument('key', type=str)
    parser.add_argument('regex', type= str)
    parser.add_argument('code', type=int)
    return parser

result_bp = Blueprint('result', __name__)
parser = init_parse()
result_api = Api(result_bp)
result_db = client.centaur


class UpdateResult(Resource):
    method_decorators = [login_required]

    def post(self):
        celery_stored = result_db.celery_taskmeta.find()
        for item in celery_stored:
            result = json.loads(item["result"])
            result_dict = {
                "url": result[0],
                "poc": result[1],
                "code": result[2][0],
                "msg": result[2][1],
                "endtime": result[3],
                "return": result[4]
            }
            try:
                result_db.results.insert_one(result_dict)
                result_db.celery_taskmeta.delete_one({"_id":item["_id"]})
            except Exception,e:
                return make_response(jsonify({"msg":e}), 500)
        return make_response(jsonify({"msg":"success"}))

    def get(self):
        args = parser.parse_args()
        if args['item_each_page']:
            global item_each_page
            item_each_page = args['item_each_page']
            return make_response(jsonify({"item_each_page": item_each_page}))
        else:
            return make_response(jsonify({"item_each_page": item_each_page}))


class Result(Resource):
    method_decorators = [login_required]

    def get(self, id):
        result = result_db.results.find_one({'_id': ObjectId(id)})
        result['_id'] = str(result['_id'])
        return result

    def delete(self, id):
        response = result_db.results.delete_one({'_id': ObjectId(id)})
        return jsonify({"delete_count":response.deleted_count})

    def post(self, id):
        args = parser.parse_args()
        if args['mark']:
            if args['mark'] in MARK_LIST:
                result = result_db.results.update_one(
                    {"_id": ObjectId(id)},
                    {"$set":{
                        "mark": args['mark']
                    }}
                )
                return make_response(jsonify({"modified_count": result.modified_count}))

            else:
                response = make_response(jsonify({
                    "msg": "Invalid mark."
                }), 400)
                return response
        else:
            response = make_response(jsonify({
                "msg": "Invalid action."
            }), 400)
            return response


class ListResult(Resource):
    method_decorators = [login_required]

    def get(self, page):
        result = []
        args = parser.parse_args()
        key = args['key']
        regex = args['regex']
        code = args['code']

        if key and regex:
            if key in ("url", "poc", "msg", "endtime", "return"):
                cursor = result_db.results.find({key: {'$regex': regex}}).sort([('endtime', -1)])\
                    .skip((page-1)*item_each_page).limit(item_each_page)
            else:
                response = make_response(jsonify({"msg": "Invalid request."}), 400)
                return response
        elif code:
            cursor = result_db.results.find({'code': code}).sort([('endtime', -1)])\
                .skip((page-1)*item_each_page).limit(item_each_page)
        else:
            cursor = result_db.results.find().sort([('endtime', -1)])\
                .skip((page-1)*item_each_page).limit(item_each_page)

        for i in cursor:
            i['_id'] = str(i['_id'])
            result.append(i)

        return result


result_api.add_resource(UpdateResult, '/update/result')
result_api.add_resource(Result, '/result/<string:id>')
result_api.add_resource(ListResult, '/list/result/<int:page>')


