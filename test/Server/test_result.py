from unittest import TestCase
from Server.run import api


class TestUpdateResult(TestCase):

    def setUp(self):
        self.api = api

    def test_update(self):
        with self.api.test_client() as c:
            r = c.post("/api/result")
            assert r.status_code == 200
