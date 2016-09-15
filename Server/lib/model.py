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


class ScriptBase(Document):
    name = StringField(unique=True)
    desc = StringField()
    rules = ListField()
    is_enable = BooleanField()

    def toggle_enable(self):
        self.is_enable = not self.is_enable
        self.save()
        return self.is_enable

    def set_invoke_rule(self, rule):
        """
        :param rules: a list in form of
         ['operator', rule1, rule2]
         where basic rule in form of, operator is considered as binary operator
         ['-', 'type', 'regex']
         e.g.: ['&', ['-', 'U', 'abc'], ['-', 'M', 'POST']]
         means to accept the flow which url contains url and the method is POST
        """
        if self.validate_rules(rule):
            self.rules = rule
            self.save()
        else:
            raise Exception, "Invalid rules"


    def compile_rules(self, rule):
        """
        Use re.complie to complie the rules in list,
        should be called like "self.pattern = self.compile_rules(self.rules)"
        and later we can use self.pattern() to filter the flow
        :param rule:  a list
        :return: a function that accept a flow and return filtered or not
        """
        operator = rule[0]
        if operator in ('&', '|'):
            p1 = self.compile_rules(rule[1])
            p2 = self.compile_rules(rule[2])
            if operator == '&':
                return  lambda s: p1(s) and p2(s)
            elif operator == '|':
                return lambda s: p1(s) or p2(s)
        elif operator == '-':
            rule_type = rule[1]
            regex = rule[2]
            pattern = re.compile(r'{}'.format(regex))
            return lambda flow:bool(pattern.search(flow[rule_type]))

    def validate_rules(self, rule):
        if len(rule) == 3:
            operator = rule[0]
            if operator in ('&', '|'):
                return self.validate_rules(rule[1]) and self.validate_rules(rule[2])
            elif operator == '-':
                if rule[1] in (METHOD, URL, FORM, REFERER, COOKIE, OTHER) and rule[2]:
                    return True
                else:
                    return False
            else:
                return False

    def invoke_check(self, flow):
        if not hasattr(self, 'pattern'):
            return True
        else:
            return self.pattern(flow)

    def send_task(self, flow):
        job = celery.send_task('task.' + self.name, [flow,])
        return job
