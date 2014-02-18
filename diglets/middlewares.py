import time
import telnetlib

from scrapy import log
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.utils.request import request_fingerprint
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware

from diglets.items import Visited

class SkipVisitedMiddleWare(object):
    """Middleware to ignore re-visiting item pages if they were already visited
    before. The requests to be filtered by have a meta['filter_visited'] flag
    enabled and optionally define an id to use for identifying them, which
    defaults the request fingerprint, although you'd want to use the item id,
    if you already have it beforehand to make it more robust.
    Reference: http://snipplr.com/view/67018/middleware-to-avoid-revisiting-already-visited-items/
    """
    FILTERED_VISITED = 'filtered_visited'
    VISITED_ID = 'visited_id'
    CONTEXT_KEY = 'visited_ids'
    
    def process_spider_output(self, response, result, spider):
        context = getattr(spider, 'context', {})
        visited_ids = context.setdefault(self.CONTEXT_KEY, {})
        ret = []
        for r in result:
            visited = False
            if isinstance(r, Request):
                if self.FILTERED_VISITED in r.meta:
                    visit_id = self._visited_id(r)
                    log.msg("Ignoring already visited: %s" % r.url,
                            level=log.INFO, spider=spider)
                    visited =True
            elif isinstance(r, BaseItem):
                visit_id = self._visited_id(response.request)
                if visit_id:
                    visited_ids[visit_id] = True
                    r['visit_id'] = visit_id
                    r['visit_status'] = u'new'

            if visited:
                ret.append(Visited(visit_id=visit_id,
                                   visit_status=u'old'))
            else:
                ret.append(r)
        return ret
            

    def _visited_id(self, request):
        return request.meta.get(self.VISITED_ID) or request_fingerprint(request)

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