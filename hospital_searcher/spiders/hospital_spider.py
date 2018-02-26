# -*- coding:utf-8 -*-
# Created by Jin(jinzhencheng@outlook.com) at 2018/02/26.

from scrapy import Spider
from scrapy import Request
from hospital_searcher.items import SectionItem
from hospital_searcher.items import ImageItem
from hospital_searcher.items import HospitalItem
from hospital_searcher.config import GenerationConfig
import json

class HospitalSpider(Spider):

    name = "hospital_spider"

    def start_requests(self):
        start_url = GenerationConfig.START_URL
        yield Request(url=start_url)

    def parse(self, response):
        is_first = True
        for sel in response.xpath("//div[@class='hospital-more__nav']/ul"):
            href = sel.xpath("./li/a/@href").extract()[0]
            province = sel.xpath("./li/a/text()").extract()[0]
            next_url = "%s%s" % (GenerationConfig.HOME_URL, href)
            if is_first:
                next_url = response.url
                is_first = False
            yield Request(url=next_url, meta={"province": province}, callback=self.parse_hospital)

    def parse_hospital(self, response):
        province = response.meta["province"]
        for sel in response.xpath("//div[contains(@class, 'content-region')]/li"):
            city = sel.xpath("./h4/a/text()").extract()[0]
            for hospital_sel in sel.xpath("./ul/li"):
                hospital_href = hospital_sel.xpath("./a/@href").extract()[0]
                hospital_name = hospital_sel.xpath("./a/text()").extract()[0]
                hospital_code = hospital_href[hospital_href.rfind('/') + 1:]
                next_url = "%s%s" % (GenerationConfig.HOME_URL, hospital_href)
                yield Request(url=next_url, meta={"province":province, "city": city,
                                                  "hospital_name": hospital_name,
                                                  "hospital_code": hospital_code}, callback=self.parse_section)

    def parse_section(self, response):
        hospital_code = response.meta["hospital_code"]
        net_img_path = response.xpath("//div[@class='hospital-basic-box__img']/span/img/@src").extract()[0]
        address = response.xpath("//div[@class='hospital-basic']/div[1]/span/text()").extract()[0]
        phone = response.xpath("//div[@class='hospital-basic']/div[2]/span/text()").extract()[0]
        description = response.xpath("//div[@class='toggle-content']/p/text()").extract()[0]

        hospital_item = HospitalItem()
        hospital_item["hospital_code"] = hospital_code
        hospital_item["province"] = response.meta["province"]
        hospital_item["city"] = response.meta["city"]
        hospital_item["address"] = address
        hospital_item["name"] = response.meta["hospital_name"]
        hospital_item["description"] = description
        hospital_item["phone"] = phone
        img_name = "%s%s" % (hospital_code, net_img_path[net_img_path.rfind('.'):])
        hospital_item["img_path"] = "%s\%s" % (GenerationConfig.IMG_DOWNLOAD_PATH, img_name)

        yield  hospital_item

        image_item = ImageItem()
        image_item["image_url"] = net_img_path
        image_item["image_code"] = hospital_code

        yield  image_item

        section_url = "https://dxy.com/view/i/hospital/section/list?page_index=1&items_per_page=20&id=%s" % hospital_code
        yield Request(url=section_url, meta={"hospital_code": hospital_code, "is_first": True}, callback=self.parse_detail)
        pass

    def parse_detail(self, response):
        hospital_code = response.meta["hospital_code"]
        is_first = response.meta["is_first"]
        data = response.body
        section_data = json.loads(data)
        items = section_data["data"]["items"]
        for item in items:
            section_item = SectionItem()
            section_item["section_code"] = item["section_id"]
            section_item["hospital_code"] = hospital_code
            section_item["name"] = item["name"]
            section_item["doctor_number"] = item["doctor_number"]
            yield section_item
        if is_first:
            total_pages = section_data["data"]["total_pages"]
            page_index = section_data["data"]["page_index"]
            for page_index in range(page_index + 1, total_pages + 1):
                next_url = "https://dxy.com/view/i/hospital/section/list?page_index=%d&items_per_page=20&id=%s" \
                           % (page_index, hospital_code)
                yield Request(url=next_url, meta={"hospital_code": hospital_code, "is_first": False}, callback=self.parse_detail)


