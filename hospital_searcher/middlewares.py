# -*- coding: utf-8 -*-
# Created by Jin(jinzhencheng@outlook.com) at 2018/02/26.


from random import choice
from hospital_searcher.config import GenerationConfig
from hospital_searcher.util import proxy_kit


class HttpProxyMiddleware(object):

    @staticmethod
    def process_request(request, spider):
        current_proxy = proxy_kit.get_one_proxy()
        request.meta["dont_redirect"] = True
        if current_proxy is not None:
            ip = current_proxy.ip
            port = current_proxy.port
            proxy_url = "http://%s:%s" % (ip, port)
            request.meta["proxy"] = proxy_url


class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.user_agent = choice(GenerationConfig.USER_AGENTS)

    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault('User-Agent', self.user_agent)