# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from admincode import settings


def write_to_csv(item):
    writer = csv.writer(
        open(settings.CSV_FILE_PATH, 'a'), lineterminator='\n')
    writer.writerow([item[key] for key in item.keys()])


class CsvExportPipeline(object):

    def process_item(self, item, spider):
        write_to_csv(item)
        return item


class AdmincodePipeline(object):

    def process_item(self, item, spider):
        return item
