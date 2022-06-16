# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from doctest import OutputChecker
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

def strip_yen(element):
    if element:
        return element.replace('¥','')
    return element

def strip_comma(element):
    if element:
        return element.replace(',','')
    return element

def convert_integer(element):
    if element:
        return int(element)
    return 0

def get_size(element):
    if element:
        return element.split('／')[0].replace('サイズ', '').replace('判','')
    return element

def get_page(element):
    if element:
        return element.split('／')[1].replace('ページ数 ', '').replace('p','')
    return element

def strip_item(element):
    if element:
        return element.replace('商品コード ', '')

class BookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(str.lstrip),
        output_processor = Join(' ')
    )
    author = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(strip_yen, strip_comma, convert_integer),
        output_processor = TakeFirst()
    )
    publisher = scrapy.Field(
        output_processor = TakeFirst()
    )
    size = scrapy.Field(
        input_processor = MapCompose(get_size),
        output_processor = TakeFirst()
    )
    page = scrapy.Field(
        input_processor = MapCompose(get_page, convert_integer),
        output_processor = TakeFirst()
    )
    isbn = scrapy.Field(
        input_processor = MapCompose(strip_item),
        output_processor = TakeFirst()
    )
    image_urls = scrapy.Field()
