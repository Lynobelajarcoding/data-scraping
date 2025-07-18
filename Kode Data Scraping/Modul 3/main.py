from bs4 import BeautifulSoup
import requests
import fungsi

def main_scrapper(url, directory):
    fungsi.create_directory(directory)
    sumber_kode = requests.get(url)
    sumber_text = sumber_kode.text
    soup = BeautifulSoup(sumber_text, "html.parser")
    articles = soup.find_all("div", {'class' : 'card__post__content'})

    for article in articles:
        judul_div = article.find("div", class_="card__post__title")
        link_tag = judul_div.find("a") if judul_div else None

        url_berita = link_tag.get("href") if link_tag else "URL tidak ditemukan"
        judul = link_tag.get("title") if link_tag else "Judul tidak ditemukan"

        tanggal_span = article.find("span", class_="text-dark text-capitalize")
        tanggal = tanggal_span.get_text(strip=True) if tanggal_span else "Tanggal tidak ditemukan"

        ringkasan = article.p.get_text(strip=True) if article.p else "Ringkasan tidak ditemukan"

        article_format = f"Judul : {judul}\nTanggal Posting : {tanggal}\nRingkasan : {ringkasan}\nURL : {url_berita}\n"

        if not fungsi.does_file_exist(directory + "/artikel.doc"):
            fungsi.create_new_file(directory + "/artikel.doc")

        fungsi.write_to_file(directory + "/artikel.doc", article_format)
        print(article_format)

main_scrapper("https://www.antaranews.com/olahraga/bulutangkis", "Hasil")