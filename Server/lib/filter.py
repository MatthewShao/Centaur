from pybloomfilter import BloomFilter

METHOD = 'M'
URL = 'U'


class DuplicatedFlowFilter(object):

    def __init__(self):
        self.bf = BloomFilter(10000000, 0.01, 'filter.bloom')

    def add(self, flow):
        """
        :param flow: the flow dict received from Proxy.
        :return: if the flow already in the filter.
        """
        f = (flow[METHOD], flow[URL])
        return self.bf.add(f)

    def __contains__(self, flow):
        f = (flow[METHOD], flow[URL])
        return self.bf.__contains__(f)
