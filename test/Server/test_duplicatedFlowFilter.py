from unittest import TestCase
from Server.lib.filter import DuplicatedFlowFilter


class TestDuplicatedFlowFilter(TestCase):

    def setUp(self):
        self.df = DuplicatedFlowFilter()
        self.flow = {'M': 'GET', 'U': 'http://www.baidu.com'}

    def test_add_contains(self):
        assert self.flow not in self.df
        self.df.add(self.flow)
        assert self.flow in self.df
