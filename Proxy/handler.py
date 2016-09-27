import json
import requests
from requests.exceptions import ConnectionError, ConnectTimeout

POST_HEADER = {'content-type': 'application/json'}
API_URL = 'http://127.0.0.1:5000/api/job'

METHOD = 'M'
URL = 'U'
FORM = 'F'
REFERER = 'R'
COOKIE = 'C'
OTHER = 'O'


RED = '\x1b[91m'
RED1 = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
ENDC = '\033[0m'


class FlowHandler(object):

    def __init__(self, api_url=None, is_debug=False):
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = API_URL
        # Test the connection to api first.
        try:
            r = requests.get("http://127.0.0.1:5000/api/list/script")
        except ConnectionError:
            print "Fail to connect to the api! Exit..."
            exit()
        if r.status_code != 200:
            print "Fail to connect to the api! Exit..."
            exit()

        self.is_debug = is_debug

    def run(self, flow):
        try:
            referer = flow.request.headers['Referer']
        except KeyError:
            referer = None
        form = self.odict2dict(flow.request.urlencoded_form, True)
        cookie = self.odict2dict(flow.request.cookies, False)

        http_flow = {
            METHOD: flow.request.method,
            URL: flow.request.url,
        }
        if form:
            http_flow[FORM] = form
        if cookie:
            http_flow[COOKIE] = cookie
        if referer:
            http_flow[REFERER] = referer
        try:
            j = json.dumps(http_flow)
        except UnicodeDecodeError:
            j = json.dumps(http_flow, encoding='GB2312')

        is_success = self.send(j)
        self.display(http_flow, is_success)

    def send(self, json_data):
        try:
            r = requests.put(self.api_url, data=json_data, headers=POST_HEADER)
            if r.status_code == 200:
                return True
        except ConnectionError, ConnectTimeout:
            return False

    def display(self, http_flow, is_success):
        if is_success:
            if self.is_debug:

                if http_flow[METHOD] == 'GET':
                    print GREEN + BOLD + http_flow[URL] + ENDC
                    for key in (REFERER, COOKIE, OTHER):
                        if http_flow.has_key(key):
                            print GREEN + str(http_flow[key]) + ENDC

                elif http_flow[METHOD] == 'POST':
                    print BLUE + BOLD + http_flow[URL] + ENDC
                    for key in (FORM, REFERER, COOKIE, OTHER):
                        if http_flow.has_key(key):
                            print BLUE + str(http_flow[key]) + ENDC
                else:
                    print BOLD + http_flow[METHOD] + ENDC + http_flow[URL]

            else:
                if http_flow[METHOD] == 'GET':
                    print GREEN + http_flow[URL] + ENDC
                elif http_flow[METHOD] == 'POST':
                    print BLUE + http_flow[URL] + ENDC
                else:
                    print BOLD + http_flow[METHOD] + ENDC + ":" +http_flow[URL]
        else:
            print RED + BOLD + http_flow[METHOD] + ENDC + \
                RED + " : " + http_flow[URL] + ENDC

    @staticmethod
    def odict2dict(odict, dupulicated=True):
        # if duplicated is True, the value will save in a list in case the duplicated situation
        if odict is None or len(odict) == 0:
            return None
        d = {}
        if dupulicated:
            for (k, v) in odict:
                if k in d:
                    d[k].append(v)
                else:
                    d[k] = [v]
        else:
            for (k, v) in odict:
                d[k] = v
        return d



