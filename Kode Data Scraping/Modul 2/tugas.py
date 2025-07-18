from bs4 import BeautifulSoup
import requests

url = "https://www.antaranews.com/olahraga/bulutangkis"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
for news in soup.find_all('h1', 'h2', 'h4', 'p'):
    print(news.text.strip())
for link in soup.find_all("a"):
    print(link.get("href"))