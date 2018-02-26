# -*- coding:utf-8 -*-
# Created by Jin(jinzhencheng@outlook.com) 2018/02/26.

from hospital_searcher.entity import proxy
from hospital_searcher.util import db_helper
from hospital_searcher.util import logger

mysql_helper = db_helper.MySQLHelper("autoSpider")
the_logger = logger.get_logger()


def get_proxy_list():
    """
    Fetch some proxy from MySQL.
    :param quantity: The quantity.
    :return: A list of proxy.
    """
    result = None
    mysql_helper.open_driver()
    session = mysql_helper.session
    try:
        result = session.query(proxy.Proxy).filter(proxy.Proxy.delay != "").order_by(proxy.Proxy.delay).all()
    except Exception, e:
        the_logger.error("An exception happened, details: %s" % e.message)
    finally:
        mysql_helper.close_driver()
    return result
pass
