import scrapy
import logging
from scrapy.shell import inspect_response

class BooksBasicSpider(scrapy.Spider):
    name = 'books_basic'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    def parse(self, response):
        books = response.xpath("//ol/li[contains(@class, 'col-xs-6')]")

        for book in books:
            # title = book.xpath('.//h3/a/@title').get()
            detail_url = book.xpath('.//h3/a/@href').get()
            yield response.follow(url=detail_url, callback=self.parse_item)
            # yield{
            #     'title': title,
            #     'URL': url
            # }
        next_page = response.xpath('//ul/li[@class="next"]/a/@href').get()
        logging.debug({
            'response.status': response.status,
            'response.url': response.url,
            'next_page': next_page 
        })
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
    
    def convert_rating(self, rating):
        if rating:
            return rating.split()[-1]
        return rating

    def parse_item(self, response):
        # inspect_response(response, self) ## shell立ち上げるコード
        main_book_info = response.xpath('//div[contains(@class, "product_main")]')
        return {
            'title': main_book_info.xpath('.//h1/text()').get(),
            'price': main_book_info.xpath('.//p[@class="price_color"]/text()').get(),
            'stock': main_book_info.xpath('.//p[@class="instock availability"]/text()').get(),
            'rating': self.convert_rating(main_book_info.xpath('.//p[contains(@class, "star-rating")]/@class').get()),
            'UPC': response.xpath('//tr/th[text()= "UPC"]/following-sibling::td[1]/text()').get(),
            'Number of review': response.xpath('//tr/th[text()= "Number of reviews"]/following-sibling::td[1]/text()').get()
        }
