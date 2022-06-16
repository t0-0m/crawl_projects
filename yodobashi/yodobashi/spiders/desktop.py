import scrapy
import logging


class DesktopSpider(scrapy.Spider):
    name = 'desktop'
    allowed_domains = ['www.yodobashi.com']
    start_urls = ['https://www.yodobashi.com/category/19531/11970/34646/']

    # def parse(self, response):
    #     logging.info(response.url)
    #     products = response.xpath('//div[contains(@class, "productListTile")]')
    #     for product in products:
    #         maker = product.xpath(".//div[contains(@class, 'pName')]/p/text()").get() # 取得済みのセレクターオブジェクトに対してxpathを使うときはパスの最初に. が必要ー
    #         name = product.xpath(".//div[contains(@class, 'pName')]/p[2]/text()").get()
    #         price = product.xpath(".//span[@class='productPrice']/text()").get()

    #         yield {
    #             'maker': maker,
    #             'name': name,
    #             'price': price
    #         }
    #     next_page = response.xpath('//a[@class="next"]/@href').get()
    #     if next_page:
    #         yield response.follow(url=next_page, callback=self.parse)
    def parse(self, response):
        logging.info(response.request.headers["User-Agent"])