from unittest import TestCase
from Proxy.run import Master
from Proxy.run import __doc__ as test_doc
from docopt import docopt

class TestMaster(TestCase):
    def test_run(self):
        m = Master(None, None, None)
        m.run()
        m.shutdown()

class TestCLI(TestCase):
    def test_default(self):
        # test the default value of '--filter'
        test_args = []
        arguments = docopt(test_doc, test_args)
        assert arguments['--filter'] == 'HIGH'

    def test_args(self):
        test_args = ["-p","*.abc.com", "-d", "domain.txt", "--debug", "--filter=LOW", "--blacklist"]
        arguments = docopt(test_doc, test_args)
        assert arguments['-p'] == "*.abc.com"
        assert arguments['-d'] == "domain.txt"
        assert arguments['--filter'] == 'LOW'
        assert arguments['--blacklist']

