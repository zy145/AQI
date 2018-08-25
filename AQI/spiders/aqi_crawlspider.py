# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from AQI.items import AqiItem


class AqiCrawlspiderSpider(CrawlSpider):
    name = 'aqi_crawlspider'
    allowed_domains = ['aqistudy.cn']
    # global base_url
    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    rules = [
        Rule(LinkExtractor(allow=r'monthdata')),
        Rule(LinkExtractor(allow=r'daydata'), callback='parse_day')
    ]

    def parse_day(self, response):

        tr_list = response.xpath("//tbody//tr")
        # 删除第一个表头的tr
        tr_list.pop(0)

        try:
            import urllib.parse as urllib
        except:
            import urllib

        url = response.url
        city_name = urllib.unquote(url[url.find("=")+1:url.find("&")]).decode("utf-8")

        for tr in tr_list:
            item = AqiItem()
            item['city'] = city_name
            item['date'] = tr.xpath("./td[1]/text()").extract_first()
            item['aqi'] = tr.xpath("./td[2]/text()").extract_first()
            item['level'] = tr.xpath("./td[3]/span/text()").extract_first()
            item['pm2_5'] = tr.xpath("./td[4]/text()").extract_first()
            item['pm_10'] = tr.xpath("./td[5]/text()").extract_first()
            item['so2'] = tr.xpath("./td[6]/text()").extract_first()
            item['co'] = tr.xpath("./td[7]/text()").extract_first()
            item['no2'] = tr.xpath("./td[8]/text()").extract_first()
            item['o3'] = tr.xpath("./td[9]/text()").extract_first()

            yield item



