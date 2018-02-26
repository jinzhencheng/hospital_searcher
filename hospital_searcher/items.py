# -*- coding: utf-8 -*-
# Created by Jin(jinzhencheng@outlook.com) at 2018/02/26.

import scrapy


class HospitalItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    img_path = scrapy.Field()
    phone = scrapy.Field()
    description = scrapy.Field()
    hospital_code = scrapy.Field()
    pass

class SectionItem(scrapy.Item):
    name = scrapy.Field()
    section_code = scrapy.Field()
    hospital_code = scrapy.Field()
    doctor_number = scrapy.Field()

class ImageItem(scrapy.Item):
    image_url = scrapy.Field()
    image_code = scrapy.Field()