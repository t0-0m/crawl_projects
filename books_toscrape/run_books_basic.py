import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from books_toscrape.spiders.books_basic import BooksBasicSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(BooksBasicSpider)
process.start()
# crawlerProcess : scrapyの処理を外部から実行するため
# get_project_settings: スパイダー実行時にsettigsの設定を読み込む

# この6行でおそらくこのファイルからデバッグ対象のcrawlを読み込んだり、スタートできる
# ようにしただけなんだと思う。
