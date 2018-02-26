# -*- coding: utf-8 -*-
# Created by Jin(jinzhencheng@outlook.com) at 2018/02/26.

from scrapy.pipelines.images import ImagesPipeline
from hospital_searcher.items import ImageItem
from hospital_searcher.items import HospitalItem
from hospital_searcher.items import SectionItem
from scrapy import Request

class HospitalImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, ImageItem):
            yield Request(item["image_url"], meta={"image_code": item["image_code"], "image_url": item["image_url"]})

    def file_path(self, request, response=None, info=None):
        image_url = response.meta["image_url"]
        image_code = response.meta["image_code"]
        start_index = image_url.rfind('.')
        ext = image_url[start_index:]
        image_name = "%s%s" % (image_code, ext)
        return image_name


class HospitalSearcherPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, HospitalItem):
            pass
        elif isinstance(item, SectionItem):
            pass
        return item
