import sqlite3

connection = sqlite3.connect('translate.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Languages (
id INTEGER PRIMARY KEY AUTOINCREMENT,
language TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS SourceTexts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
source TEXT NOT NULL,
language_id INTEGER,
FOREIGN KEY (language_id) REFERENCES Languages (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Translations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
source_text_id INTEGER,
target TEXT NOT NULL,
target_lang_id INTEGER,
FOREIGN KEY (source_text_id) REFERENCES SourceTexts (id),
FOREIGN KEY (target_lang_id) REFERENCES Languages (id)
)
''')

connection.commit()