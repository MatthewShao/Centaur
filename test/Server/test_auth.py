from unittest import TestCase
from Server.auth import create_token, parse_token
from Server.lib.datatype import AttribDict
from Server.run import api, init_db
import json


class TestAuth(TestCase):

    def setUp(self):
        init_db()
        self.fail_test = {
            'username': 'test',
            'password': '123',
            'email': 'test@test.com'
        }
        self.success_test = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com'
        }

    def test_token(self):
        test_user = AttribDict()
        test_user.id = 123
        token = create_token(test_user)

        test_req = AttribDict()
        test_req.headers = {'Authorization': ' ' + token}
        parsed = parse_token(test_req)
        assert parsed['sub'] == '123'

    def test_auth(self):
        api.testing = True
        with api.test_client() as c:
            rv = c.post('/api/login', data=json.dumps(self.fail_test), content_type='application/json')
            j = json.loads(rv.data)
            assert j['msg'] == 'Invalid username/password.'
            rv = c.post('/api/login', data=json.dumps(self.success_test), content_type='application/json')
            j = json.loads(rv.data)
            assert 'token' in j


class TestRegister(TestCase):

    def setUp(self):
        self.t1 = {
            'username': 'test',
            'password': '123',
            'email': 'test@test.com'
        }

        self.t2 = {
            'username': 'abc',
            'password': '123'
        }

        self.t3 = {
            'username': 'abc',
            'password': '123',
            'email': '123123123123123'
        }

    def test_register(self):
        api.testing = True
        with api.test_client() as c:
            rv = c.post('/api/register', data=json.dumps(self.t1), content_type='application/json')
            j = json.loads(rv.data)
            assert j['msg'] == 'User existed.'

            rv = c.post('/api/register', data=json.dumps(self.t2), content_type='application/json')
            j = json.loads(rv.data)
            assert j['msg'] == 'Missing field.'

            rv = c.post('/api/register', data=json.dumps(self.t3), content_type='application/json')
            j = json.loads(rv.data)
            assert j['msg'] == 'Email address invalid.'

