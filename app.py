import os
import re
import urllib.parse
from flask import Flask, render_template, request, url_for, send_from_directory, redirect
from datetime import datetime
import db

app = Flask(__name__)
# app.secret_key = 'hogehoge'

#フロントエンドでフォルダを認識させるためのおまじないコード
SAVE_DIR = "image"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

#ここで認識させている
@app.route('/image/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET': 
        data = db.read_all()

        return render_template('index.html', \
            data=data)

    if request.method == 'POST':

        req = request.get_data()
        print(req)
        id, value = req.decode().split('=')
        value = urllib.parse.unquote(value)

        if value == '詳細情報':

            data = db.read_all()
            detail_url = db.read_id(id).url

            return render_template('index.html', \
            data=data, detail_url=detail_url)

        else:
            db.chage_favorit(id)
            return redirect(url_for('index'))


@app.route('/detail', methods=['GET', 'POST'])
def detail():

    id = request.args.get('id')

    detail_url = db.read_id(id).url
    data = db.read_all()

    if request.method == 'GET':
        return render_template('index.html', \
            data=data, detail_url=detail_url)

@app.route('/list', methods=['GET'])
def genre():
    genre = request.args.get('genre', None)
    data = db.read_genre(genre)
    return render_template('index.html', \
            data=data)

@app.route('/favorit', methods=['GET'])
def favorit():
    data = db.read_favorit()
    return render_template('index.html', \
            data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)