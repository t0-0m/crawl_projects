import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging

class OnigiriSpider(CrawlSpider):
    name = 'onigiri'
    allowed_domains = ['www.sej.co.jp']
    start_urls = ['https://www.sej.co.jp/products/a/onigiri']
    # start_urls = ['https://www.sej.co.jp/products/a/cat/010010010000000']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_btn brn pbNested pbNestedWrapper "]//a')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="item_ttl"]/p/a'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths='//li/a[text()="［次へ］"]')),
    )

   
    def get_id(self, url):
        return int(url.split('item/')[-1].replace('/', ''))

    def get_title(self, title):
        if title:
            return title.replace('\u3000', '')  
        return title    
    
    def get_notax_price(self, price):
        if price:
            return int(price.split('（')[0].replace('円', ''))
        return 0

    def get_taxin_price(self, price):
        if price:
            return float(price.split('（')[1].replace('税込', '').replace('円）', ''))
        return 0

    def to_dict(self, info):
        if info:
            dict = {}
            for item in info.split('、'):
                dict[item.split('：')[0]] = item.split('：')[1]
            return dict
        return info

    def get_kcal(self, kcal):
        if kcal:
            return float(kcal.replace('kcal', ''))
        return kcal

    def get_g(self, g):
        if g:
            return float(g.replace('g', ''))
        return g

    def remove_g(self, g):
        if g:
            return float(g.replace('g', ''))
        return g

    def get_kcal(self, kcal):
        if kcal:
            return float(kcal.replace('kcal', ''))
        return kcal

        
    def parse_item(self, response):
        logging.info(response.url) 
        item_info = response.xpath('//th[text()="栄養成分"]/following-sibling::td/text()').get()
        info_dict = self.to_dict(item_info)
        # logging.info(response.request.headers['User-Agent']) # user agent(消しても良いよ) 
        print('------------------')
        yield {
            'id': self.get_id(response.url),
            'title': response.xpath('//h1/text()').get(),
            'price_notax': self.get_notax_price(response.xpath('//div[@class="item_price"]/p/text()').get()),
            'price_taxin': self.get_taxin_price(response.xpath('//div[@class="item_price"]/p/text()').get()),
            'kcal': self.get_kcal(info_dict['熱量']),
            'protein': self.remove_g(info_dict['たんぱく質']),
            'salt': self.remove_g(info_dict['食塩相当量']),
            'url': response.url,
            'price_info': response.xpath('//div[@class="item_price"]/p/text()').get(),
            'item_info': item_info
        }