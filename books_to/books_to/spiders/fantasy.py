import scrapy


class FantasySpider(scrapy.Spider):
    name = 'fantasy'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    def parse(self, response):
        books = response.xpath("//ol/li[contains(@class, 'col-xs-6')]")
        for book in books:
            title = book.xpath('.//h3/a/text()').get()
            url = book.xpath('.//h3/a/@href').get()
            yield{
                'title': title,
                'url': url
            }
        next_page = response.xpath('//ul/li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
            
        