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

    def test_get(self):
        with self.api.test_client() as c:
            r = c.get('/api/list/script') # update script_set
            r = c.get('/api/script/test')
            j = json.loads(r.data)
            assert j['name'] == 'test'

    def test_post(self):
        with self.api.test_client() as c:
            c.get('/api/list/script') # update script_set

            # test toggle
            c.post('/api/script/test', data={
                'action': 'toggle'
            })
            r = c.get('/api/script/test')
            j = json.loads(r.data)
            assert not j['is_enable']

            # test set_rule
            r = c.post('/api/script/test', data={
                'action': 'set_rule',
                'invoke_rule': 'test abc'
            })
            assert r.data == 'Success'
            r = c.get('/api/script/test')
            j = json.loads(r.data)
            assert j['invoke_rule'] == 'test abc'

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

    def test_get_script(self):
        script = self.s.get_script('test')
        assert script.name == 'test'
        script = self.s.get_script('junk')
        assert not script

    def tearDown(self):
        os.remove('scripts/test.py')


class TestDownload(TestCase):
        pass
