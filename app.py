from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('')
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    diaries = list(db.diary.find({}, {'_id': False}))
    return render_template('index.html', diaries=diaries)


@app.route('/posting', methods=['POST'])
def posting():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'content': content_receive,
        'time': mytime,
        'file': f'{filename}.{extension}',
        'idx': db.diary.find_one({'$query':{}, '$orderby':{'idx':-1}})['idx']+1
    }

    db.diary.insert_one(doc)
    return jsonify({'msg':'업로드 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=50400,debug=True)