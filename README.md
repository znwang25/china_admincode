# Scraping Chinese Administrative Code （2009-2017）
(爬虫扒取中国乡镇区划代码历史数据 2009 - 2017)

All chinese administrative units have a unique identifier, aka *gbcode*. Those identifiers are widely used in almost all chinese applications. However, each year some of the gbcode will be changed due to changes in administrative units (name change, boundary change, jurisdiction change etc.). This project aims to preserve the historical record of the gbcode by scraping gbcode for all township and above units from National Bureau of Statistics of the PRC website. The default setting is to scrape all the information from year 2009 to 2017. You can change this range in `stats.py`.

The resulting output will have following variables:
+ year
+ prov_name
+ city_name
+ city_code
+ county_name
+ county_code
+ town_name
+ town_code

### Usage 
The only required package is `scrapy`. In the project folder, run following command: 
```python
python crawl.py
```
Default csv output path is `CSV_FILE_PATH = "./admin_code.csv"`.
You can change this in the `settings.py`