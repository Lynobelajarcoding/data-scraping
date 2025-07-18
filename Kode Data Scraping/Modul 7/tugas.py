from bs4 import BeautifulSoup
import requests
import fungsi
from flask import Flask, render_template

app = Flask(__name__)

def main_scraper(url, directory):
    fungsi.create_directory(directory)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("h3", {'class': 'media__title'})

    data = []
    for article in articles:
        link_tag = article.find("a")
        if not link_tag:
            continue
        article_format = {
            "url": link_tag.get("href"),
            "title": link_tag.text.strip()
        }
        data.append(article_format)

    return data

@app.route('/')
def home():
    url = "https://www.detik.com/"
    directory = "Hasil"
    data = main_scraper(url, directory)
    return render_template("index.html", articles=data)

if __name__ == "__main__":
    app.run(debug=True)
