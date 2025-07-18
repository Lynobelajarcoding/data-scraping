from bs4 import BeautifulSoup
import requests
import fungsi
from flask import Flask, render_template

app = Flask(__name__)

def main_scraper(url, directory):
    fungsi.create_directory(directory)
    sumber_kode = requests.get(url)
    sumber_text = sumber_kode.text
    soup = BeautifulSoup(sumber_text, 'html.parser')
    articles = soup.find_all('a', {'class': 'media__link'})
    
    data = []

    for article in articles:
        article_format = {
            "url": article.get("href"),
            "title": article.text.strip()
        }
        data.append(article_format)
        
    return data

@app.route("/")
def home():
    url = "https://detik.com"
    directory = "Hasil"
    data = main_scraper(url, directory)
    return render_template("index.html", articles=data)

app.run(debug=True)