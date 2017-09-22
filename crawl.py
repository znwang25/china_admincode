#!/usr/bin/env python3
# This script is helpful for debugging a spider inside an IDE.
import time
import logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

# Switch to Scrapy project folder

# Settings
log_file = True

spiders = ['stats']

if log_file:
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log/crawl_{}.log'.format(
            time.strftime('%Y-%m-%d--%H-%M')),
        filemode='w'
    )
else:
    configure_logging()

# spider_schedule_message = (
#     'The following spiders are scheduled to start crawling in 30 seconds:\n' +
#     '\n(list view)\n' + '\n'.join(sorted(spiders)) + '\n\n(compact view)\n' +
#     ', '.join(sorted(spiders)))
# print(spider_schedule_message)

# logging.info(spider_schedule_message)
# time.sleep(30)

runner = CrawlerRunner(get_project_settings())

for spider in spiders:
    runner.crawl('{}'.format(spider))

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
