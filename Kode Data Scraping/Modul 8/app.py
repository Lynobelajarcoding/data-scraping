from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/bola-sport")
def bola_sport():
    html_doc = requests.get("https://www.bolasport.com/")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    data = soup.find_all("div", {'class':'news-list__item clearfix'})

    return render_template("bola-sport.html", data = data)

@app.route("/detik-jatim")
def detik_jatim():
    html_doc = requests.get("https://www.detik.com/jatim/berita/indeks")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    populer_area = soup.find(attrs={'class':'grid-row list-content'})

    texts = populer_area.findAll(attrs={'class':'media__text'})
    images = populer_area.findAll(attrs={'class':'media media--left media--image-radius block-link'})
    return render_template("detik-jatim.html", images = images, texts = texts)

@app.route("/detik-jateng")
def detik_jateng():
    html_doc = requests.get("https://www.detik.com/jateng/berita/indeks")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    populer_area = soup.find(attrs={'class':'grid-row list-content'})

    texts = populer_area.findAll(attrs={'class':'media__text'})
    images = populer_area.findAll(attrs={'class':'media media--left media--image-radius block-link'})
    return render_template("detik-jateng.html", images = images, texts = texts)

@app.route("/detik-jabar")
def detik_jabar():
    html_doc = requests.get("https://www.detik.com/jabar/berita/indeks")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    populer_area = soup.find(attrs={'class':'grid-row list-content'})

    texts = populer_area.findAll(attrs={'class':'media__text'})
    images = populer_area.findAll(attrs={'class':'media media--left media--image-radius block-link'})
    return render_template("detik-jabar.html", images = images, texts = texts)

if __name__=="__main__":
    app.run(debug=True)