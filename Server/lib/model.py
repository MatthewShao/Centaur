from mongoengine import *
from celery_ import celery
import re


class User(Document):

    username = StringField(unique=True)
    password = StringField()
    email = EmailField()


class ScriptBase(object):

    def __init__(self, name, params=None, headers=None):
        """

        :param name: script name
        :param params: Dict()
        :param headers: Dict()
        """
        self.name = name
        self.params = params
        self.headers = headers
        self.invoke_rule = None
        self.is_enable = True
        self._rule_regax = None

    def toggle_enable(self):
        self.is_enable = not self.is_enable
        return self.is_enable

    def set_invoke_rule(self, re_exp):
        self.invoke_rule = re_exp
        if re_exp:
            self._rule_regax = re.compile(self.invoke_rule, re.I)
        else:
            self._rule_regax = None

    def invoke_check(self, s):
        if not self.invoke_rule or self._rule_regax.search(s):
            return True
        else:
            return False

    def send_task(self):
        tid = celery.send_task('task.' + self.name)
        return tid
