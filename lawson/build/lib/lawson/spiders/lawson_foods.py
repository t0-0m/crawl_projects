import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging

class LawsonFoodsSpider(CrawlSpider):
    name = 'lawson_foods'
    allowed_domains = ['www.lawson.co.jp']
    start_urls = ['https://www.lawson.co.jp/recommend/original/rice/', 'https://www.lawson.co.jp/recommend/original/sushi/', 'https://www.lawson.co.jp/recommend/original/bento/', 'https://www.lawson.co.jp/recommend/original/chilledbento/',
    'https://www.lawson.co.jp/recommend/original/sandwich/', 'https://www.lawson.co.jp/recommend/original/bakery/', 'https://www.lawson.co.jp/recommend/original/pasta/', 'https://www.lawson.co.jp/recommend/original/noodle/','https://www.lawson.co.jp/recommend/original/salad/',
    'https://www.lawson.co.jp/recommend/original/select/osozai/', 'https://www.lawson.co.jp/recommend/original/soup/', 'https://www.lawson.co.jp/recommend/original/gratin/', 'https://www.lawson.co.jp/recommend/original/konamono/','https://www.lawson.co.jp/recommend/original/fry/']
    # start_urls = ['https://www.lawson.co.jp/recommend/original/bakery/']

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="list_btn brn pbNested pbNestedWrapper "]//a')),
        # Rule(LinkExtractor(restrict_xpaths='//section[@id="sec-02"]//a')),
        Rule(LinkExtractor(restrict_xpaths='//p[@class="img"]/a'), callback='parse_item', follow=False),
        # Rule(LinkExtractor(restrict_xpaths='//li/a[text()="［次へ］"]')),
        
    )


    def get_id(self, url):
        # return int(url.split('detail/')[-1].replace('.html', ''))
        return int(url.split('detail/')[-1].replace('.html', '').split('_')[0])

    def get_title(self, title):
        if title:
            return title.replace('\u3000', '')  # lstrip は指定文字を先頭から削除する。何も指定しなければ改行や全角スペースを削除してくれる
        return title    
    
    # def get_notax_price(self, price):
    #     if price:
    #         return (float(price.replace('円', '').replace(',', '')) / 1.08)
    #     return 0

    def get_taxin_price(self, price):
        if price:
            return int(price.replace('円', '').replace(',', ''))
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
            k = kcal.replace('kcal', '').replace(',', '')
            if '当り' in k:
                k = float(k.split('当り')[-1])
            return float(k)
        return kcal


    def remove_g(self, g):
        if g:
            return float(g.replace('g', '').replace(',', ''))
        return g

    def parse_item(self, response):
        logging.info(response.url) # 詳細ページのurlが取得できているか確かめるためにloggingで確認
        price = response.xpath('//div[@class="rightBlock"]//dl/dd/span[contains(text(), "円")]/text()').get()
        print('------------------')
        yield {
            'id': self.get_id(response.url),
            'title': response.xpath('//div[@class="rightBlock"]/p[@class="ttl"]/text()').get(),
            'cat': response.xpath('//h2[@class="pageTitle"]/text()').get(),
            # 'price_notax': self.get_notax_price(price),
            'price_taxin': self.get_taxin_price(price),
            'kcal': self.get_kcal(response.xpath('//div[@class="rightBlock"]//dl/dd[contains(text(), "kcal")]/text()').get()),
            'protein': self.remove_g(response.xpath('//div[@class="tbody"]/dl/dt[text()="たんぱく質"]/following-sibling::dd/text()').get()),
            'salt': self.remove_g(response.xpath('//div[@class="tbody"]/dl/dt[text()="食塩相当量"]/following-sibling::dd/text()').get()),
            'kcal_info':response.xpath('//div[@class="rightBlock"]//dl/dd[contains(text(), "kcal")]/text()').get(),
            'url': response.url,
            'img_url': response.xpath('//div[@class="leftBlock"]/p/img/@src').get()
            }

        
   
