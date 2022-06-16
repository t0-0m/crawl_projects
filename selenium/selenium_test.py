from optparse import Option
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless')  ##ここの行のコメントアウトするかしないかでheadlessかどうか切り替えるのが楽らしい

# driver = webdriver.Chrome(executable_path='/Users/suzuki/Downloads/chromedriver', options=options)
driver = webdriver.Chrome(executable_path='/Users/suzuki/Downloads/chromedriver', options=options)
 
driver.get('https://www.bing.com/')

search_bar = driver.find_element_by_id('sb_form_q') # フォームを指定
search_bar.send_keys('井上尚弥')  # テキストを入力
search_bar.send_keys(Keys.ENTER) ##エンター


# search_btn = driver.find_element_by_xpath('.//label[@for="sb_form_go"]')
# search_btn.click() ## submitでも良いよー

# search_btn.submit()

i = 0
while True:
    sleep(2)
    for elem in driver.find_elements_by_xpath('.//div[@class="b_title"]/h2/a'):
        print(elem.text)
        print(elem.get_attribute('href'))
    next_link = driver.find_element_by_xpath('.//a[@title="次のページ"]')
    driver.get(next_link.get_attribute('href'))
    i += 1
    if i > 4:
        break

driver.close()