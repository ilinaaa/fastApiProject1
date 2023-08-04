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
    translation = translate(text, target_lang, source_lang)
    target_text = translation[0]


    # Сохраняем перевод в базу данных
    cursor.execute("INSERT INTO Translations (source, target) VALUES (?, ?)", (text, target_text))
    connection.commit()

    return {"source": text, "target": target_text}

#
#
# app = FastAPI()
#
# @app.get("/test")
# def test(text, tl):
#     out = translate(text, tl)
#     print(out)
#     return {'translate': out[0]}
