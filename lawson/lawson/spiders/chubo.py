import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChuboSpider(CrawlSpider):
    name = 'chubo'
    allowed_domains = ['www.lawson.co.jp']
    start_urls = ['https://www.lawson.co.jp/recommend/original/machikadochubo/sandwich/index.html', 'https://www.lawson.co.jp/recommend/original/machikadochubo/bento/index.html', 'https://www.lawson.co.jp/recommend/original/machikadochubo/rice/index.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//p[@class="img"]/a'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
