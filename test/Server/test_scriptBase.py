from unittest import TestCase
from Server.lib.model import ScriptBase


class TestScriptBase(TestCase):
    def setUp(self):
        self.script = ScriptBase('test')

    def test_toggle_enable(self):
        assert self.script.is_enable
        assert not self.script.toggle_enable()

    def test_set_invoke_rule(self):
        self.script.set_invoke_rule('://[^?]+\?')

    def test_invoke_check(self):
        self.script.set_invoke_rule('://[^?]+\?')
        assert self.script.invoke_check("http://abc.com/1.php?a=123")
        assert not self.script.invoke_check("http://abc.com/123.html/123")

    def test_send_task(self):
        pass
