from lib2to3.pgen2 import driver
import scrapy
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector


class FoodsSpider(scrapy.Spider):
    name = 'foods'
    
    # start_urls = ['http://www.family.co.jp/goods.html/']
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://www.family.co.jp/goods/omusubi.html',
            wait_time=3,
            screenshot=False,
            callback=self.parse,
        )


    def parse(self, response):
        driver = response.meta['driver']

        # もっとみるをクリックする
        driver.find_element_by_xpath('//a[contains(@class, "js-btn-more")]').send_keys(Keys.ENTER)
        sleep(3)

        html = driver.page_source
        selector = Selector(text=html) # htmlをセレクターオブジェクトに変換

        article_details = selector.xpath('//a[contains(@class, "ly-mod-infoset4-link")]/@href')
        for article_detail in article_details:
            yield response.follow(url=article_detail, callback=self.parse_item)
            
            
            # html = driver.page_source
            # selector = Selector(text=html) # htmlをセレクターオブジェクトに変換
            # title = selector.xpath('.//h1/text()').get()
            # print(title)
            # print('-----------')
            # w = driver.execute_script('return document.body.scrollWidth')
            # h = driver.execute_script('return document.body.scrollHeight')
            # driver.set_window_size(w, h)
            # driver.save_screenshot('famima{}.png'.format(title))
        def parse_item(self, response):
            return {
                'title': response.xpath('.//h1/text()').get(),
                'description': response.xpath('.//p[@class="ly-goods-lead"]/text()').get(),
            }    

        # スクショ撮る
        # cat = selector.xpath('.//h1/text()').get()
        # print(cat)
        # print('-----------')
        # w = driver.execute_script('return document.body.scrollWidth')
        # h = driver.execute_script('return document.body.scrollHeight')
        # driver.set_window_size(w, h)
        # driver.save_screenshot('famima{}.png'.format(cat))

        
