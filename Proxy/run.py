"""
Proxy for Centaur.

Usage:
    run.py [-h] [-u API_URL] [-d FILE] [-p PATTERN] [--debug] [--filter=<filter>] [--blacklist]

Options:
    -h --help  Show this screen.
    -u API_URL URL of the api on server
    -d FILE  Domain List
    -p PATTERN  Allow domain pattern
    --debug  Debug mode
    --filter=<filter>  NONE|LOW|HIGH [default: HIGH]
    --blacklist  Turn on blacklist mode
"""

from mitmproxy import controller, proxy
from mitmproxy.proxy.server import ProxyServer
from filter import FlowFilter
from handler import FlowHandler
from docopt import docopt

PORT = 8081

class Master(controller.Master):
    def __init__(self, server, flow_filter, flow_handler):
        controller.Master.__init__(self, server)
        self.filter = flow_filter
        self.handler = flow_handler

    def run(self):
        print "[*] Running proxy on port {}...".format(PORT)
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            print "[!]" + "User Stop."
            print "[!] Proxy Stop. "
            self.shutdown()
        except Exception, e:
            print "[!]" + str(e)
            print "[!] Proxy Stop. "
            self.shutdown()

    def handle_request(self, flow):
        flow.reply()

    def handle_response(self, flow):
        if self.filter.run(flow):
           self.handler.run(flow)
        flow.reply()


def start():
    arguments = docopt(__doc__, version='dev')
    if arguments['--filter'] not in ('NONE', 'LOW', 'HIGH'):
        print "--filter should set to (NONE|LOW|HIGH)"
        print __doc__
        exit()
    config = proxy.ProxyConfig(port=PORT)
    server = ProxyServer(config)

    flow_filter = FlowFilter(arguments['--filter'], arguments['-p'], arguments['-d'], arguments['--blacklist'])
    flow_handler = FlowHandler(arguments['-u'], arguments['--debug'])
    m = Master(server, flow_filter, flow_handler)
    m.run()

if __name__ == '__main__':
    start()
