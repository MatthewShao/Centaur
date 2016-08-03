from unittest import TestCase
from Server.lib.model import ScriptBase


class TestScriptBase(TestCase):
    def setUp(self):
        self.script = ScriptBase('test')

    def test_toggle_enable(self):
        e = self.script.rule.is_enable
        assert e != self.script.toggle_enable()

    def test_set_invoke_rule(self):
        self.script.set_invoke_rule('://[^?]+\?', 'U')

    def test_invoke_check(self):
        self.script.set_invoke_rule('://[^?]+\?', 'U')
        t1 = {'U': "http://abc.com/1.php?a=123"}
        t2 = {'U': "http://abc.com/123.html/123"}
        assert self.script.invoke_check(t1)
        assert not self.script.invoke_check(t2)

    def test_send_task(self):
        pass
