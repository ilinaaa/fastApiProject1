from fastapi import FastAPI, Query, HTTPException
import requests
import sqlite3

app = FastAPI()

connection = sqlite3.connect('translate.db')
cursor = connection.cursor()


def translate(text, tl, sl):
    query = {

        'client': 'dict-chrome-ex',
        'sl': sl,  # Source Language
        'tl': tl,  # Target Language
        'q': text,  # Query
    }

    resp = requests.get(
        'https://clients5.google.com/translate_a/t',
        params=query
    )
    data = resp.json()
    return data

@app.get("/translate")
async def translate_text(text: str = Query(..., min_length=1, max_length=500), target_lang: str = Query(...), source_lang: str = Query(...)):
    if len(text) > 500:
        raise HTTPException(status_code=400, detail='Text is too long')

    # Проверяем, существует ли язык в таблице Languages
    cursor.execute("SELECT id FROM Languages WHERE language=?", (source_lang,))
    source_lang_id = cursor.fetchone()
    if source_lang_id is None:
        # Если язык не существует, добавляем его в таблицу Languages
        cursor.execute("INSERT INTO Languages (language) VALUES (?)", (source_lang,))
        source_lang_id = cursor.lastrowid
    else:
        source_lang_id = source_lang_id[0]

    cursor.execute("SELECT id FROM Languages WHERE language=?", (target_lang,))
    target_lang_id = cursor.fetchone()
    if target_lang_id is None:
        # Если язык не существует, добавляем его в таблицу Languages
        cursor.execute("INSERT INTO Languages (language) VALUES (?)", (target_lang,))
        target_lang_id = cursor.lastrowid
    else:
        target_lang_id = target_lang_id[0]

    # Проверяем, существует ли исходный текст в таблице CourseTexts
    cursor.execute("SELECT id FROM SourceTexts WHERE source=?", (text,))
    source_text_id = cursor.fetchone()
    if source_text_id is None:
        # Если перевод не существует, добавляем его в таблицу CourseTexts
        cursor.execute("INSERT INTO SourceTexts (source, language_id) VALUES (?, ?)", (text, source_lang_id))
        source_text_id = cursor.lastrowid
    else:
        source_text_id = source_text_id[0]

        # Проверяем наличие перевода в базе данных
    cursor.execute("SELECT target FROM Translations WHERE source_text_id = ? AND target_lang_id = ?",
                   (source_text_id, target_lang_id))
    saved_translation = cursor.fetchone()
    if saved_translation:
        target_text = saved_translation[0]
    else:
        # Если перевода нет, обращаемся к Google Переводчику
        translation = translate(text, target_lang, source_lang)
        target_text = translation[0]

        # Сохраняем перевод в базу данных
        cursor.execute("INSERT INTO Translations (source_text_id, target, target_lang_id) VALUES (?, ?, ?)",
                       (source_text_id, target_text, target_lang_id))
        connection.commit()

    return {"source": text, "target": target_text}


