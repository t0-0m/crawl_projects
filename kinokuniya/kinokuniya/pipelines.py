# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
import sqlite3
from scrapy.pipelines.images import ImagesPipeline

class customImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None,* , item=None):
        name = item.get('isbn') + '.jpg'
        filename = r'computer_books/' + name
        # return request.url.split('/')[-1]
        return filename

class CheckItemPipeline:
    def process_item(self, item, spider):
        if not item.get('isbn'):
            raise DropItem('Missing ISBN')
        return item

class MongoPipeline:
    collection_name = 'computer_books'
    # open_spider はスパイダーの開始時に実行される、なのでdbへの接続とかの処理をすることが多いよ
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb+srv://t0_0m:Open1234@cluster0.mzzhs.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['BOOKDB']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))


class SQLitePipeline:
    # open_spiderメソッドで接続、テーブル作成(テーブルはすでにあれば例外処理)
    def open_spider(self, spider):
        self.connection = sqlite3.connect('BOOKDB.db') # BOOKDBのdbに接続
        self.c = self.connection.cursor() # cursorを取得し変数c に代入
        try:
            self.c.execute('''
                CREATE TABLE computer_books(
                    title text,
                    author text,
                    price integer,
                    publisher text,
                    size text,
                    page integer,
                    isbn text primary key
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO computer_books (title, author, price, publisher, size, page, isbn)
            VALUES(?,?,?,?,?,?,?)
        ''', (
            item.get('title'),
            item.get('author'),
            item.get('price'),
            item.get('publisher'),
            item.get('size'),
            item.get('page'),
            item.get('isbn'),
        ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()