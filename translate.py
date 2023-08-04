import sqlite3

connection = sqlite3.connect('translate.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        target TEXT,
        language TEXT)
''')
connection.commit()
connection.close()