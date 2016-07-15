from unittest import TestCase
from Proxy.filter import FlowFilter
from urlparse import urlparse


class TestFlowFilter(TestCase):

    def test_type_filter(self):
        f = FlowFilter()
        assert f.type_filter("abc.jpg") is False
        assert f.type_filter("abc/abc.js") is False
        assert f.type_filter("abc/css/css.Js") is False
        assert f.type_filter("abc/js.JS") is False
        assert f.type_filter("js/css/1.php") is True

    def test_domain_filter(self):
        # black list test
        f = FlowFilter(domain_file="domain_example.txt", use_blacklist=False)
        parsed = urlparse("http://www.baidu.com/abc.php")
        assert f.domain_filter(parsed) is True
        parsed = urlparse("http://www.google.com/")
        assert f.domain_filter(parsed) is True
        parsed = urlparse("http://www.bing.com/")
        assert f.domain_filter(parsed) is False

        # white list test
        f = FlowFilter(domain_file="domain_example.txt", use_blacklist=True)
        parsed = urlparse("http://www.baidu.com/abc.php")
        assert f.domain_filter(parsed) is False
        parsed = urlparse("http://www.google.com/")
        assert f.domain_filter(parsed) is False
        parsed = urlparse("http://www.bing.com/")
        assert f.domain_filter(parsed) is True

        # pattern test
        f = FlowFilter(domain_pattern=".*\.baidu\.com")
        test_list = ["http://www.baidu.com/123.php",
                     "http://c.baidu.com/",
                     "https://a.b.c.baidu.com"]
        for url in test_list:
            parsed = urlparse(url)
            assert f.domain_filter(parsed) is True

        parsed = urlparse("www.google.com")
        assert  f.domain_filter(parsed) is False

    def test_detail_filter(self):
        f = FlowFilter(level='HIGH')
        u1 = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=123&rsv_pq=f4e54353000e8d1"
        parsed = urlparse(u1)
        assert f.detail_filter(parsed) is False
        u2 = "http://music.baidu.com/search?fr=ps&ie=utf-8&key=123"
        parsed = urlparse(u2)
        assert f.detail_filter(parsed) is True

        f = FlowFilter(level='LOW')
        parsed = urlparse(u1)
        assert f.detail_filter(parsed) is True

    def test_run(self):
        pass
