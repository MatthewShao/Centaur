from unittest import TestCase
from Server.script import ScriptSet
from Server.run import api
from cStringIO import StringIO
import os

class TestScript(TestCase):
    def setUp(self):
        self.api = api
        self.api.config['TESTING'] = True

    def put(self):
        with self.api.test_client() as c:
            r = c.put('/api/script/test', data={
                file:StringIO("This is test file.",'test.py'),
            })
            assert "uploaded" in r.data



class TestSriptSet(TestCase):

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
