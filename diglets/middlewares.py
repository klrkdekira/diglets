import time
import telnetlib
from scrapy import log
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware

class RetryChangeProxyMiddleware(RetryMiddleware):
    """
    Reference: How to use scrapy with tor
    https://groups.google.com/forum/#!msg/scrapy-users/WqMLnKbA43I/B3N1ysvoy-4J
    """
    def _retry(self, request, reason, spider):
        log.msg('Changing proxy')
        tn = telnetlib.Telnet('127.0.0.1', 9151)
        tn.read_until("Escape character is '^]'.", 2)
        tn.write('AUTHENTICATE "jinglebell"\r\n')
        tn.read_until("250 OK", 2)
        tn.write("signal NEWNYM\r\n")
        tn.read_until("250 OK", 2)
        tn.write("quit\r\n")
        tn.close()
        time.sleep(3)
        log.msg('Proxy changed')
        return RetryMiddleware._retry(self, request, reason, spider)

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://127.0.0.1:8118"
        request.headers['Proxy-Authorization'] = 'Basic'