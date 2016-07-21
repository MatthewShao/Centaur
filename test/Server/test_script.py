from unittest import TestCase
from Server.script import ScriptSet
import os

class TestScript(TestCase):
    pass

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
