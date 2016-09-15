from unittest import TestCase
from Server.lib.model import ScriptBase


class TestScriptBase(TestCase):
    def setUp(self):
        self.r1 = ['-', 'U', '://[^?]+\\?']
        self.r2 = ['-', 'M', 'POST']
        self.r3 = ['|', self.r1, self.r2]
        self.script = ScriptBase(name='test', desc="This is test Description.",  rules=self.r3, is_enable=True)
        pattern = self.script.compile_rules(self.script.rules)
        setattr(self.script, 'pattern', pattern)
        self.script.save()

    def test_toggle_enable(self):
        e = self.script.is_enable
        assert e != self.script.toggle_enable()

    def test_validate_rules(self):

        r4 = ['*', self.r1, self.r2]
        r5 = ['&', 'r1', self.r2]
        assert self.script.validate_rules(self.r1)
        assert self.script.validate_rules(self.r2)
        assert self.script.validate_rules(self.r3)
        assert not self.script.validate_rules(r4)
        assert not self.script.validate_rules(r5)

    def test_invoke_check(self):
        flow1 = {'U': 'http://baidu.com/1.php?abc=123', 'M': 'GET'}  # True
        flow2 = {'U': 'http://baidu.com/2.php', 'M': 'POST'}  # True
        flow3 = {'U': 'http://baidu.com/3.php', 'M': 'GET'}  # False
        assert self.script.invoke_check(flow1)
        assert self.script.invoke_check(flow2)
        assert not self.script.invoke_check(flow3)

    def test_send_task(self):
        pass

    def tearDown(self):
        self.script.delete()
