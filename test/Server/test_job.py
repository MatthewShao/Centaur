from unittest import TestCase
from Server.job import JobPool
from Server.run import api
import json


class TestJobPool(TestCase):

    def setUp(self):
        self.pool = JobPool(10)

    def test_add(self):
        for i in range(10):
            self.pool.add(i)
        self.pool.add(999)
        assert self.pool[0] == 1
        assert self.pool[9] == 999

    def test_iter(self):
        for i in range(10):
            self.pool.add(i)
        for i in self.pool:
            pass

class TestListJob(TestCase):

    def setUp(self):
        f = open('scripts/test.py', 'w')
        f.write("print 'test script'")
        f.close()
        self.api = api
        self.api.config['TESTING'] = True

    def test_list(self):
        flow = {'U':'http://test.com/test'}
        with self.api.test_client() as c:
            c.get('/api/list/script')
            c.post('api/script/test', data={
                'action':'set_rule',
                'invoke_rule': None,
                'type':'U'
            })
            c.put('/api/job', data=flow)
            r = c.get('/api/list/job')

        j = json.loads(r.data)
        assert len(j) > 0


