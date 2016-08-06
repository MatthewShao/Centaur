from celery import Celery, Task
from celery.utils.log import get_task_logger
from config import SERVER, TASK_TIMEOUT
import time
import json
import socket
import requests
from requests import ConnectionError

from pocsuite.lib.core.data import kb, conf
from pocsuite.lib.core.common import filepathParser, multipleReplace, StringImporter, delModule
from pocsuite.lib.core.settings import POC_IMPORTDICT, HTTP_DEFAULT_HEADER

METHOD = 'M'
URL = 'U'
FORM = 'F'
REFERER = 'R'
COOKIE = 'C'
OTHER = 'O'

celery = Celery('task')
celery.config_from_object('config')
logger = get_task_logger(__name__)


def load_scripts():
    scripts_set = {}
    try:
        r = requests.get(SERVER + '/api/list/script')
        scripts = json.loads(r.content)
        for s in scripts:
            if s[1]:
                scripts_set[str(s[0])] = None
        for s in scripts_set.iterkeys():
            r = requests.get(SERVER + '/api/download/script/' + s)
            scripts_set[s] = r.content

        return scripts_set

    except ConnectionError:
        logger.error("Fail to connect to the Server.")
        exit()

script_set = load_scripts()


def _init(self):
    super(self.__class__, self).__init__()
    conf.isPycFile = False
    conf.httpHeaders = HTTP_DEFAULT_HEADER
    try:
        kb.registeredPocs
    except Exception:
        kb.registeredPocs = {}
    # _setHTTPtimeout
    timeout = float(TASK_TIMEOUT)
    socket.setdefaulttimeout(timeout)

    # registerPoc
    pocString = multipleReplace(self.pocString, POC_IMPORTDICT)
    _, self.moduleName = filepathParser(self.pocName)
    try:
        importer = StringImporter(self.moduleName, pocString)
        importer.load_module(self.moduleName)
    except ImportError, ex:
        logger.error(ex)


def run(self, flow):
    try:
        poc = kb.registeredPocs[self.moduleName]
        url = flow.pop(URL)
        result = poc.execute(url, mode='verify', params=flow)
        output = (url, self.pocName, (1, "success") if result.is_success() else (0, str(result.error[1])), time.strftime("%Y-%m-%d %X", time.localtime()), str(result.result))
        print output
        return output
    except Exception, ex:
        logger.error(ex)
        return None

ScriptTaskSet = {}
for name in script_set.iterkeys():
    ScriptTaskSet[name] = type(name, (Task,), {
        # data field
        'name':'task.'+ name,
        'pocString': script_set[name],
        'pocName': name,
        #method
        '__init__': _init,
        'run': run,
    })
