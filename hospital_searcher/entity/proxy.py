# -*- coding:utf-8 -*-
# Created by Jin(jinzhencheng@outlook.com) at 2018/02/26.

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Proxy(Base):
    """
    proxy model entity
    """
    __tablename__ = "proxyinfo"

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    port = Column(Integer)
    add_time = Column(DateTime)
    update_time = Column(DateTime)
    from_site = Column(String)
    delay = Column(Integer)
