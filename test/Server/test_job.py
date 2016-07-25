from unittest import TestCase
from Server.job import JobPool


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
