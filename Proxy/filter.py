import re
from urlparse import urlparse, parse_qsl


class FlowFilter(object):

    def __init__(self, level=None, domain_pattern=None, domain_file=None, use_blacklist=False):
        # type: (object, object, object, object) -> object
        self.level = level
        self.use_blacklist = use_blacklist
        self.type_pattern = re.compile("(\.gif|\.jpg|\.jpeg|\.png|\.js|\.css|\.ico|\.mp3|\.mp4|\.swf|\.woff)", re.I)
        if domain_pattern:
            self.domain_pattern = re.compile(domain_pattern, re.I)
        else:
            self.domain_pattern = None
        if domain_file:
            try:
                f = open(domain_file, 'r')
                self.domain_list = f.readlines()
                for i in range(len(self.domain_list)):
                    self.domain_list[i] = self.domain_list[i].strip()
            except IOError:
                self.domain_list = None
        else:
            self.domain_list = None

    def type_filter(self, url_path):
        """Filter the unwanted filetype,
        return True if it is NOT filtered"""

        return not self.type_pattern.search(url_path)

    def domain_filter(self, parsed):
        """Filter the specified domains, in black or white list,
        return True if it is NOT filtered"""

        result = True
        if self.domain_list:
            result = (parsed.netloc in self.domain_list) ^ self.use_blacklist
            # use xor trick to get the determine the condition
        if result and self.domain_pattern:
            if not self.domain_pattern.search(parsed.netloc):
                result = False
        return result

    def detail_filter(self, parsed):
        """Filter according to the url length and parameter number,
        return True if it is NOT filtered"""

        query_len = len(parsed.query)
        params_num = len(parse_qsl(parsed.query))
        if self.level == 'HIGH':
            return query_len < 50 and params_num < 5
        elif self.level == 'LOW':
            return query_len < 80 and params_num < 8

    def run(self, flow):
        parsed = urlparse(flow.request.url)
        url_path = flow.request.url.split('?')[0]
        if self.level == 'NONE':
            return True
        else:
            return self.type_filter(url_path) and self.domain_filter(parsed) and self.detail_filter(parsed)



