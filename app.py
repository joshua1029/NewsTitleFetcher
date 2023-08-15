from flask import Flask, render_template, request, jsonify # 引入flask的東西
from abmediatext import getAbTitle # 從我的abmediatext.py中拿getAbTitle函式

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    pages = int(request.form["pages"])
    titles = getAbTitle(pages, keyword)
    
    return jsonify(titles)

