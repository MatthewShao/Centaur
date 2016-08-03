from mongoengine import *
from celery_ import celery
from Server.db import init_db
import re

METHOD = 'M'
URL = 'U'
FORM = 'F'
REFERER = 'R'
COOKIE = 'C'
OTHER = 'O'

init_db()


class User(Document):

    username = StringField(unique=True)
    password = StringField()
    email = EmailField()


class Rule(Document):
    name = StringField(unique=True)
    string = StringField()
    type = StringField()
    is_enable = BooleanField()


class ScriptBase(object):

    def __init__(self, name, params=None, headers=None):
        """

        :param name: script name
        :param params: Dict()
        :param headers: Dict()
        """
        self.rule = Rule.objects(name=name).first()
        if not self.rule:
            self.rule = Rule(name=name, string=None, is_enable=True, type=None)
            self.rule.save()
        self.name = name
        self.params = params
        self.headers = headers
        self._rule_regax = None

    def toggle_enable(self):
        self.rule.is_enable = not self.rule.is_enable
        self.rule.save()
        return self.rule.is_enable

    def set_invoke_rule(self, re_exp, type):
        self.rule.string = re_exp
        if type not in (METHOD, URL, FORM, REFERER, COOKIE, OTHER):
            return False
        self.rule.type = type
        if re_exp:
            self._rule_regax = re.compile(self.rule.string, re.I)
        else:
            self._rule_regax = None
        self.rule.save()

    def invoke_check(self, flow):
        if not self.rule.string or not self.rule.type \
              or self._rule_regax.search(flow[self.rule.type]):
            return True
        else:
            return False

    def send_task(self, **kwargs):
        job = celery.send_task('task.' + self.name, kwargs=kwargs)
        return job
