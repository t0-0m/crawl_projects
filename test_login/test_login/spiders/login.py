import scrapy
from scrapy import FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        print(csrf_token)
        print('-----------')
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'test_user',
                'password': 'test'
            },
            callback=self.after_login
            
        )


    def after_login(self, response):
        if response.xpath('.//a[@href="/logout"]/text()').get():
            print('Login Succeded!!!')
            print('%%%%%%%%') # みやすくするためだけなので消した方が良い
        else:
            print('Login Failed!!')
            print('%%%%%%%%') # みやすくするためだけなので消した方が良い