from unittest import TestCase
from Server.script import ScriptSet
from Server.run import api
from cStringIO import StringIO
import os
import json


class TestScript(TestCase):
    def setUp(self):
        f = open('scripts/test.py', 'w')
        f.write("This is test file.")
        f.close()
        self.api = api
        self.api.config['TESTING'] = True

    def test_post(self):
        with self.api.test_client() as c:
            r = c.get('/api/list/script') # update script_set

            j = json.loads(r.data)
            origin_state = j['test']['is_enable']

            # test toggle
            c.post('/api/script/test', data={
                'action': 'toggle'
            })
            r = c.get('/api/script/test')
            j = json.loads(r.data)
            assert origin_state != j['test'['is_enable']

            # test set_rule
            rule  = ['&', ['-', 'U', 'abc'], ['-', 'F', 'efg']]
            r = c.post('/api/script/test', data={
                'action': 'set_rule',
                'invoke_rule': rule
            })
            assert r.data == 'Success'
            r = c.get('/api/list/script')
            j = json.loads(r.data)
            assert j['test']['invoke_rule'] == rule

    def test_put(self):
        with self.api.test_client() as c:
            r = c.put('/api/script/test_put', data={
                'file': (StringIO("This is test file."), 'test1.txt')
            })
            assert "uploaded" in r.data
            os.remove('scripts/test_put.py')

class TestScriptSet(TestCase):

    def setUp(self):
        f = open('scripts/test.py', 'w')
        f.write("test" * 50)
        f.close()
        self.s = ScriptSet()

    def test_get_names(self):
        assert 'test' in self.s.get_names()

    def test_update(self):
        assert 'test' in self.s.get_names()
        f = open('scripts/test1.py', 'w')
        f.write("test" * 50)
        f.close()
        self.s.update()
        assert 'test1' in self.s.get_names()
        os.remove('scripts/test1.py')

    def test_iter(self):
        for s in self.s:
            continue

    def tearDown(self):
        os.remove('scripts/test.py')


class TestDownload(TestCase):
        pass
