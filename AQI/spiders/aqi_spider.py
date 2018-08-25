#coding:utf-8

import scrapy

from ..items import AqiItem


class AqiSpider(scrapy.Spider):
    name = "aqi_spider"
    allowed_domains = ["aqistudy.cn"]
    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    def parse(self, response):
        """
            接收首页的响应，提取所有城市的链接和城市名，并发送每个城市的请求，响应交给parse_month解析
        """
        city_link_list = response.xpath("//div[@class='all']//li/a/@href").extract()
        city_name_list = response.xpath("//div[@class='all']//li/a/text()").extract()

        #for n, city_link in enumerate(city_link_list):
        for city_link, city_name in list(zip(city_link_list, city_name_list))[10:13]:
        #for city_link in city_link_list:
            #city_name = city_name_list[n]
            yield scrapy.Request(self.base_url + city_link, meta={"city" : city_name}, callback=self.parse_month)


    def parse_month(self, response):
        """
            解析每个城市的响应，提取该城市所有月的链接，并发送请求，响应交给parse_day解析
        """
        month_link_list = response.xpath("//tbody//td/a/@href").extract()

        for month_link in month_link_list[10:13]:
            yield scrapy.Request(self.base_url + month_link, meta = response.meta, callback=self.parse_day)


    def parse_day(self, response):
        """
            解析每个月份的响应，提取每一天的数据，并保存到item中
        """
        tr_list = response.xpath("//tbody//tr")
        # 删除第一个表头的tr
        tr_list.pop(0)

        # if six.PY2:
        #     import urllib
        # else:
        #     import urllib.parse as urllib

        # try:
        #     import urllib.parse as urllib
        # except:
        #     import urllib

        # url = response.url
        # city_name = urllib.unqoute(url[url.find("=")+1:url.find("&")]).decode("utf-8")

        city_name = response.meta['city']

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





