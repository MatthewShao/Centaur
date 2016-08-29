from unittest import TestCase
from Server.run import api
from Server.db import client
from Server.config import ITEM_EACH_PAGE
import json


class TestUpdateResult(TestCase):

    def setUp(self):
        self.api = api

    def test_update(self):
        with self.api.test_client() as c:
            r = c.post("/api/update/result")
            assert r.status_code == 200

    def test_set_item_each_page(self):
        with self.api.test_client() as c:
            r = c.get("/api/update/result")
            assert json.loads(r.data)['item_each_page'] == 30

            r = c.get("/api/update/result?item_each_page=100")
            assert json.loads(r.data)['item_each_page'] == 100


class TestResult(TestCase):

    def setUp(self):
        self.db = client.centaur
        self.api = api
        self.test_obj = {
            "url": "http://test.com/test.php",
            "poc": "test_poc",
            "code": 1,
            "msg": "This is a test result obj.",
            "endtime": "2000-01-01 00:00:00",
            "return": "success"
        }
        self.test_objid = self.db.results.insert_one(self.test_obj).inserted_id

    def test_get(self):
        with self.api.test_client() as c:
            r = c.get('/api/result/' + str(self.test_objid))
            j = json.loads(r.data)
            assert j['url'] == self.test_obj["url"] and j['msg'] == self.test_obj["msg"]

    def test_post(self):
        with self.api.test_client() as c:
            r = c.post('/api/result/' + str(self.test_objid), data={
                "mark" : "suc"
            })
            assert r.status_code == 400
            assert json.loads(r.data)["msg"] == "Invalid mark."

            r = c.post('/api/result/' + str(self.test_objid), data={
                "ma" : "success"
            })
            assert r.status_code == 400
            assert json.loads(r.data)["msg"] == "Invalid action."

            r = c.post('/api/result/' + str(self.test_objid), data={
                "mark" : "success"
            })
            assert r.status_code == 200
            assert json.loads(r.data)["modified_count"] == 1

            r = c.get('/api/result/' + str(self.test_objid))
            j = json.loads(r.data)
            assert j['mark'] == 'success'

    def test_detele(self):
        with self.api.test_client() as c:
            r = c.delete('/api/result/' + str(self.test_objid))
            assert json.loads(r.data) == 1

    def tearDown(self):
        self.db.results.delete_one({'_id': self.test_objid})


class TestListResult(TestCase):

    def setUp(self):
        self.db = client.centaur
        self.api = api
        self.test_obj = {
            "url": "http://test.com/test.php",
            "poc": "test_poc",
            "code": 1,
            "msg": "This is a test result obj.",
            "endtime": "2100-01-01 00:00:00",
            "return": "success"
        }
        self.test_objid = self.db.results.insert_one(self.test_obj).inserted_id

    def get(self):
        with self.api.test_client() as c:
            # general list
            r = c.get('/api/list/result/1')
            j = json.loads(r)
            assert len(j) == ITEM_EACH_PAGE
            # list by key
            r = c.get('/api/list/result/1?key=url&regex=test.com')
            assert json.loads(r.data)[0]['url'] == 'http://test.com/test.php'
            # list by code
            r = c.get('/api/list/result/1?code=1')
            assert json.loads(r.data)[0]['code'] == 1
            # error key
            r = c.get('/api/list/result/1?key=abc&regex=test')
            assert json.loads(r.data)["msg"] == "Invalid request."

    def tearDown(self):
        self.db.results.delete_one({'_id': self.test_objid})