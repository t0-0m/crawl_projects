import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging

class BooksCrawlSpider(CrawlSpider):
    name = 'books_crawl'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a'))
    )

    def parse_item(self, response):
        book_detail = response.xpath('//div[contains(@class, "product_main")]')
        
        title = book_detail.xpath('.//h1/text()').get()
        price = book_detail.xpath('.//p[@class="price_color"]/text()').get()
        stock = book_detail.xpath('.//p[@class="instock availability"]/text()').get()
        rating = book_detail.xpath('.//p[contains(@class, "star-rating")]/@class').get()

        detail_table = response.xpath('//table')
        upc = detail_table.xpath('.//tr/th[text()= "UPC"]/following-sibling::td[1]/text()').get()
        nor = detail_table.xpath('.//tr/th[text()= "Number of reviews"]/following-sibling::td[1]/text()').get()
        yield {
            'title': title,
            'price': price,
            'stock': stock,
            'rating': rating,
            'UPC': upc,
            'Number of review': nor
        }

        # logging.info(response.url) # 詳細ページのurlが取得できているか確かめるためにloggingで確認
        
        # yield {
        #     'title': response.xpath('.//h1/text()').get(),
        #     'price': response.xpath('//p[@class="price_color"]/text()').get(),
        #     'stock': response.xpath('.//p[@class="instock availability"]/text()').get(),
        #     'rating':response.xpath('.//p[contains(@class, "star-rating")]/@class').get(),
        #     'UPC': response.xpath('.//tr/th[text()= "UPC"]/following-sibling::td[1]/text()').get(),
        #     'Number of review': response.xpath('.//tr/th[text()= "Number of reviews"]/following-sibling::td[1]/text()').get()
        # }


