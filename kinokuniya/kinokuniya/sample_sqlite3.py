import sqlite3

connection = sqlite3.connect('BOOKDB.db') # BOOKDBのdbに接続
cursor = connection.cursor() # cursorを取得し変数c に代入

for row in cursor.execute('SELECT * FROM computer_books WHERE size = " A5" ORDER BY isbn'):
    print(row)