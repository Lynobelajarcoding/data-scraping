from flask import Flask, render_template, request
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    kincir = kincir_articles()
    jagat = jagat_articles()
    game8 = game8_articles()
    eurogamer = eurogamer_articles()

    return render_template("index.html", kincir=kincir, jagat=jagat, game8=game8, eurogamer=eurogamer)

def kincir_articles():
    html_doc = requests.get('https://kincir.com/category/game/')
    soup = BeautifulSoup(html_doc.text, "html.parser")
    popular_area = soup.find(attrs={'class': 'd-lg-grid category__latest-listSingle'})

    data = popular_area.find_all(attrs={'class': 'card__post-landscape'})
    kincir = []
    for item in data:
        img_tag = item.find('img')
        img = img_tag.get('data-lazy-src') or img_tag.get('src')
        url = item.find('a')['href']
        title = item.find('a')['aria-label']
        time = item.find('span').text

        kincir.append({
            'img': img,
            'link': url,
            'title': title,
            'time': time
        })

    return kincir

def jagat_articles():
    html_doc = requests.get('https://jagatplay.com/')
    soup = BeautifulSoup(html_doc.text, "html.parser")
    popular_area = soup.find(attrs={'class': 'ct__main'})

    data = popular_area.find_all(attrs={'class': 'art'})
    jagat = []
    for item in data:
        img = item.find('img')['src']
        url = item.find('a')['href']
        title = item.find('h2').text
        time = item.find('div', {'class': 'art__date'}).text

        jagat.append({
            'img': img,
            'link': url,
            'title': title,
            'time': time
        })

    return jagat

def game8_articles():
    html_doc = requests.get('https://game8.co/articles/reviews')
    soup = BeautifulSoup(html_doc.text, "html.parser")
    popular_area = soup.find(attrs={'class': 'p-articleListItem__reviews'})

    data = popular_area.find_all(attrs={'class': 'p-articleListItem'})
    game8 = []
    for item in data:
        img = item.find('img')['data-src']
        url = item.find('a')['href']
        title = item.find('div', {'class': 'p-articleListItem__title'}).text
        time = item.find('time').text
        
        if url.startswith('/'):
            url = f'https://game8.co{url}'

        game8.append({
            'img': img,
            'link': url,
            'title': title,
            'time': time
        })

    return game8

def eurogamer_articles():
    html_doc = requests.get('https://www.eurogamer.net/news')
    soup = BeautifulSoup(html_doc.text, "html.parser")
    popular_area = soup.find(attrs={'class': 'archive__items'})

    data = popular_area.find_all(attrs={'class': 'archive__item'})
    eurogamer = []
    for item in data:
        img = item.find('img')['src']
        url = item.find('a')['href']
        title = item.find('h2').text
        time = item.find('time').text

        eurogamer.append({
            'img': img,
            'link': url,
            'title': title,
            'time': time
        })

    return eurogamer

def fetch_article(url, source):
    url = request.args.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = {}

    if source == "kincir":
        data = soup.find(attrs={'class': 'article'})
        if data:
            title = data.find('h1').text
            time = data.find('div', class_='article__info-date info').text
            thumb = data.find('div', class_='inner').find('img')['src']
            konten_div = data.find('div', class_='content')
            if konten_div:
                konten = konten_div.find_all(['p', 'h2', 'h3', 'img'])
                konten_list = []
                for tag in konten:
                    if tag.name == 'img':
                        img_src = tag.get('src', '') or tag.get('data-lazy-src', '')
                        if "cloudfront.net" in img_src:
                            konten_list.append(str(tag))
                    else:
                        konten_list.append(str(tag))
            else:
                konten_list = []

            article = {
                'title': title,
                'time': time,
                'thumb': thumb,
                'konten': konten_list
            }

    elif source == "jagat":
        data = soup.find(attrs={'class': 'jgpost__box'})
        if data:
            title = data.find('h1').text
            time = data.find('div', class_='jgauthor__posted').text

            thumb_div = data.find('div', class_='jgpost__feat-img')
            if thumb_div and 'style' in thumb_div.attrs:
                style = thumb_div['style']
                match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
                thumb = match.group(1) if match else None
            else:
                thumb = None

            figure = data.find('picture').find('img')['src']
            konten_div = data.find('div', class_='jgpost__content')
            if konten_div:
                konten = konten_div.find_all(['p', 'h5', 'h3', 'figure'])
                konten_list = [str(tag) for tag in konten]
            else:
                konten_list = []

            article = {
                'title': title,
                'time': time,
                'thumb': thumb,
                'figure': figure,
                'konten': konten_list
            }

    elif source == "game8":
        data = soup.find(attrs={'class': 'l-2col__main__article'})
        if data:
            title = data.find('h1').text
            time = data.find('time').text
            img_tag = data.find('p').find('img')
            if img_tag:
                thumb = img_tag['src']
            else:
                thumb_div = data.find('div', class_='p-article__gameScore__head')
                if thumb_div and 'style' in thumb_div.attrs and 'background-image' in thumb_div['style']:
                    style_content = thumb_div['style']
                    match = re.search(r'url\(["\']?(.*?)["\']?\)', style_content)
                    if match:
                        thumb = match.group(1)
                else:
                    thumb = None

            konten_div = data.find('div', class_='p-articleBody article-style-wrapper')
            if konten_div:
                konten = konten_div.find_all(['p', 'h2', 'h3', 'iframe'])
                konten_list = []
                for tag in konten:
                    if tag.name == 'iframe' and tag.get('data-src'):
                        tag['src'] = tag['data-src']
                    konten_list.append(str(tag))
            else:
                konten_list = []

            article = {
                'title': title,
                'time': time,
                'thumb': thumb,
                'konten': konten_list
            }

    elif source == "eurogamer":
        data = soup.find(attrs={'class': 'page_content'})
        if data:
            title = data.find('h1').text
            time = data.find('time').text
            thumb = data.find('img')['src']
            konten_div = data.find('div', class_='article_body')
            if konten_div:
                konten = konten_div.find_all('p')
                konten_list = [str(tag) for tag in konten]
            else:
                konten_list = []

            article = {
                'title': title,
                'time': time,
                'thumb': thumb,
                'konten': konten_list
            }

    return article

@app.route("/article/<source>")
def detail_article(source):
    url = request.args.get('url')
    article = fetch_article(url, source)
    return render_template("article.html", articles={source: article})

@app.route("/news/<source>")
def news(source):
    articles = {
        "kincir": kincir_articles,
        "jagat": jagat_articles,
        "game8": game8_articles,
        "eurogamer": eurogamer_articles
    }
    
    if source in articles:
        article_data = articles[source]()
        return render_template("news.html", source=source, articles=article_data)
    
if __name__ == "__main__":
    app.run(debug=True)