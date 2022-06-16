import pymongo


client = pymongo.MongoClient('mongodb+srv://t0_0m:Open1234@cluster0.mzzhs.mongodb.net/?retryWrites=true&w=majority')
db = client['BOOKDB']
collection = db['computer_books']

# findの中に辞書型で条件を入れることもできる
#for document in collection.find({'author': '小川 雄大'}):
for document in collection.find():
    print(document)


