# -*- coding:utf-8 -*-
# Created by Jin (jinzhencheng@outlook.com) at 2018/02/26.

from hospital_searcher.config import GenerationConfig
from hospital_searcher.dal import proxy_dal
from hospital_searcher.util import logger
import random
import requests

the_logger = logger.get_logger()

def get_one_proxy():
    """
    Get one item from proxy list.
    :return: A dictionary of proxy info.
    """
    proxy_list = proxy_dal.get_proxy_list()
    while True:
        proxy = random.choice(proxy_list)
        if __check(proxy):
            valid_proxy = proxy
            break
    return valid_proxy


def __check(proxy):
    proxies = {"http": "http://%s:%s" % (proxy.ip, proxy.port)}
    resp = None
    try:
        resp = requests.get(url=GenerationConfig.REQUEST_SITE_URL,
                            headers=GenerationConfig.HEADER,
                            timeout=GenerationConfig.REQUEST_TIME_OUT,
                            proxies=proxies)
    except Exception, e:
        the_logger.error("An exception happened,details: %s" % e.message)
    finally:
        result = resp is not None and resp.ok
    return result
