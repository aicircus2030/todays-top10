from flask import Flask, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    news_file = os.path.join(app.root_path, "news.json")
    with open(news_file, "r", encoding="utf-8") as f:
        news_items = json.load(f)
    date_str = datetime.now().strftime('%Y年%m月%d日')
    return render_template("index.html", top=news_items[:10], rest=news_items[10:], date=date_str)

@app.route("/living")
def living():
    return render_template("living.html")

@app.route("/visa")
def visa():
    return render_template("visa.html")

@app.route("/immigration")
def immigration():
    return render_template("immigration.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/amazon")
def amazon():
    return render_template("amazon.html")

if __name__ == "__main__":
    app.run(debug=True)
