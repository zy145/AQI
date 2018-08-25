# -*- coding: utf-8 -*-

import time

from retrying import retry
from selenium import webdriver

from scrapy.http import HtmlResponse


class SeleniumMiddleware(object):
    def __init__(self):
        # 构建有界面的Chrome
        self.driver = webdriver.Chrome()

        # 构建无界面的Chrome
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # self.driver = webdriver.Chrome(chrome_options = options)


    # retry是一个装饰器，装饰retry_load_page()方法，如果该方法执行时候没有异常，则retry不工作
    # 如果方法执行时抛出了异常，异常将会被retry捕获，并按参数进行重试（总共重试20次，每次间隔200毫秒）
    # 如果在20次内找到需要的数据，那么程序正常执行，并返回最后的响应给spider解析
    # 如果在20次内都没有找打需要的数据，那么retry不再捕获异常，那么异常将会交给上一级方法的try捕获并写入日志中
    @retry(stop_max_attempt_number=20, wait_fixed=200)
    def retry_load_page(self, reqeust, spider):
        try:
            # 如果这里出现异常则交给try捕获，那么retry则不会工作，所以在except需要主动raise 一个异常
            self.driver.find_element_by_xpath("//tbody/tr[2]/td[1]")
        except:
            spider.logger.info("Retry <{}> page ({} times)".format(reqeust.url, self.count))
            self.count += 1
            # 手动抛出异常交给retry捕获，如果retry重试20次后，则该异常交到上一级方法的try捕获
            raise Exception("<{}> page load failed".format(reqeust.url))

    def process_request(self, request, spider):
        #if "php" in reqeust.url:
        if "monthdata" in request.url or "daydata" in request.url:
            self.count = 1
            #driver = webdriver.Chrome()
            self.driver.get(request.url)

            try:
                #time.sleep(5)
                self.retry_load_page(request, spider)
                html = self.driver.page_source
                # 返回自定义的响应对象给引擎，引擎判断是一个response对象，交给spider解析处理。则request不再交给下载器。
                return HtmlResponse(url=self.driver.current_url, body=html.encode("utf-8"), encoding="utf-8", request=request)
            except Exception as e:
                spider.logger.error(e)




    def __del__(self):
        self.driver.quit()
