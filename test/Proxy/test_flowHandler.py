from unittest import TestCase
from Proxy.handler import FlowHandler
from netlib.odict import ODict


class TestFlowHandler(TestCase):
    def test_run(self):
        pass

    def test_odict2dict(self):
        odict = ODict([('k1', 'v1'), ('k2', 'v2'), ('k1', 'v10')])
        d1 = FlowHandler.odict2dict(odict)
        assert d1 == {'k1': ['v1', 'v10'], 'k2': ['v2']}
        d2 = FlowHandler.odict2dict(odict, False)
        assert d2 == {'k1': 'v10', 'k2': 'v2'}
