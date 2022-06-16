import json 

with open('data.json', encoding='utf-8') as f:
    qiita_data = json.load(f)
    # print(qiita_data[0])
    titles = qiita_data[0]['titles']
    # print(titles)
    urls = qiita_data[0]['urls']
    # print(urls)

for title, url in zip(titles, urls):
    print(title, url)
    print('---------')