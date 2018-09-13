# -*- coding: utf-8 -*-
from copy import deepcopy
import re
from scrapy.spiders import Spider
from admincode.items import AdmincodeItem


class StatsSpider(Spider):
    name = 'stats'
    allowed_domains = ['stats.gov.cn']
    start_urls = [
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/{}/index.html'.format(year) for year in range(2009, 2018)]
    # http://www.mca.gov.cn/article/sj/tjbz/a/2018/201803131439.html

    def parse(self, response):
        year_pattern = re.compile(
            '(tjyqhdmhcxhfdm/)([0-9][0-9][0-9][0-9])')
        year = year_pattern.search(response.url).group(2)
        for item in response.css(".provincetr a"):
            name = item.xpath("./text()").extract_first().strip()
            link = item.xpath("./@href").extract_first().strip()
            yield response.follow(link, callback=self.parse_province,
                                  meta={'item': {'prov_name': name, 'year': year}})

    def parse_province(self, response):
        meta = response.meta['item']

        for cityrow in response.css(".citytr"):
            city_link = cityrow.xpath("./td[2]/a/@href").extract_first()
            city_name = cityrow.xpath("./td[2]/a/text()").extract_first()
            city_code = cityrow.xpath("./td[1]/a/text()").extract_first()

            meta_new = deepcopy(meta)
            meta_new['city_name'] = city_name
            if city_code:
                meta_new['city_code'] = city_code[0:4]
            else:
                meta_new['city_code'] = ""
            yield response.follow(city_link, callback=self.parse_city, meta={'item': meta_new})

    def parse_city(self, response):

        meta = response.meta['item']
        if response.css(".countytr"):
            for countyrow in response.css(".countytr"):
                county_link = countyrow.xpath(
                    "./td[2]/a/@href").extract_first()
                county_name = countyrow.xpath(
                    "./td[2]/a/text()").extract_first()
                county_code = countyrow.xpath(
                    "./td[1]/a/text()").extract_first()
                meta_new = deepcopy(meta)
                meta_new['county_name'] = county_name
                if county_code:
                    meta_new['county_code'] = county_code[0:6]
                else:
                    meta_new['county_code'] = ""
                yield response.follow(county_link, callback=self.parse_county, meta={"item": meta_new})
        elif response.css(".towntr"):
            for townrow in response.css(".towntr"):
                # town_link = townrow.xpath("./td[2]/a/@href").extract_first()
                town_name = townrow.xpath("./td[2]/a/text()").extract_first()
                town_code = townrow.xpath("./td[1]/a/text()").extract_first()
                meta_new = deepcopy(meta)
                meta_new['county_name'] = ""
                meta_new['county_code'] = ""
                meta_new['town_name'] = town_name
                if town_code:
                    meta_new['town_code'] = town_code[0:9]
                else:
                    meta_new['town_code'] = ""
                item = AdmincodeItem()
                item['year'] = meta_new['year']
                item['prov_name'] = meta_new['prov_name']
                item['city_name'] = meta_new['city_name']
                item['city_code'] = meta_new['city_code']
                item['county_name'] = meta_new['county_name']
                item['county_code'] = meta_new['county_code']
                item['town_name'] = meta_new['town_name']
                item['town_code'] = meta_new['town_code']

                yield item

    def parse_county(self, response):

        meta = response.meta['item']
        if response.css(".towntr"):
            for townrow in response.css(".towntr"):
                # town_link = townrow.xpath("./td[2]/a/@href").extract_first()
                town_name = townrow.xpath("./td[2]/a/text()").extract_first()
                town_code = townrow.xpath("./td[1]/a/text()").extract_first()
                meta_new = deepcopy(meta)
                meta_new['town_name'] = town_name
                if town_code:
                    meta_new['town_code'] = town_code[0:9]
                else:
                    meta_new['town_code'] = ""
                item = AdmincodeItem()
                item['year'] = meta_new['year']
                item['prov_name'] = meta_new['prov_name']
                item['city_name'] = meta_new['city_name']
                item['city_code'] = meta_new['city_code']
                item['county_name'] = meta_new['county_name']
                item['county_code'] = meta_new['county_code']
                item['town_name'] = meta_new['town_name']
                item['town_code'] = meta_new['town_code']
                yield item
        else:
            meta_new = deepcopy(meta)
            item = AdmincodeItem()
            item['year'] = meta_new['year']
            item['prov_name'] = meta_new['prov_name']
            item['city_name'] = meta_new['city_name']
            item['city_code'] = meta_new['city_code']
            item['county_name'] = meta_new['county_name']
            item['county_code'] = meta_new['county_code']
            item['town_name'] = ""
            item['town_code'] = ""
            yield item
