# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import Spider
from admincode.items import AdmincodeItem


class StatsSpider(Spider):
    name = 'stats'
    allowed_domains = ['stats.gov.cn']
    start_urls = [
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/{}/index.html'.format(year) for year in range(2009, 2010)]

    def parse(self, response):
        for item in self.parse_provincetr(response, response.selector.css(".provincetr")):
            yield item

    def get_text_href(self, td):
        if not td.xpath('a'):
            return td.xpath('text()').extract()[0], None
        else:
            return td.xpath('a/text()').extract()[0], td.xpath('a/@href').extract()[0]

    def parse_provincetr(self, response, trs):
        year_pattern = re.compile(
            '(tjyqhdmhcxhfdm/)([0-9][0-9][0-9][0-9])')
        year = year_pattern.search(response.url).group(2)
        for td in trs.xpath('td'):
            scraped = {}
            scraped['year'] = year
            scraped['prov_name'], href = self.get_text_href(td)
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_citytr,
                                 meta={'scraped': scraped})

    def parse_2td(self, response, trs, var_name, nextparse):
        for tr in trs:
            scraped = response.meta['scraped']
            scraped[var_name], href = self.get_text_href(tr.xpath('td')[1])
            if nextparse:
                url = response.urljoin(href)
                yield scrapy.Request(url, callback=nextparse, meta={'scraped': scraped})
            else:
                item = AdmincodeItem()
                item['year'] = scraped['year']
                item['prov_name'] = scraped['prov_name']
                item['city_name'] = scraped['city_name']
                item['county_name'] = scraped['county_name']
                item['town_name'] = scraped['town_name']
                item['gbcode'], href = self.get_text_href(
                    tr.xpath('td')[0])
                yield item

    def parse_citytr(self, response):
        for city in self.parse_2td(response, response.selector.css(".citytr"), 'city_name', self.parse_countytr):
            yield city

    def parse_countytr(self, response):
        for county in self.parse_2td(response, response.selector.css(".countytr"), 'county_name', self.parse_towntr):
            yield county

    def parse_towntr(self, response):
        for town in self.parse_2td(response, response.selector.css(".towntr"), 'town_name', None):
            yield town
