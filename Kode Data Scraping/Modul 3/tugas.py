from bs4 import BeautifulSoup
import requests
import fungsi

def main_scrapper(url, directory):
    fungsi.create_directory(directory)
    sumber_kode = requests.get(url)
    sumber_text = sumber_kode.text
    soup = BeautifulSoup(sumber_text, "html.parser")
    
    articles = soup.find_all("article")  # Elemen umum untuk tiap artikel di Detik

    for article in articles:
        # Judul dan URL
        link_tag = article.find("a")
        judul_tag = article.find("h2")  # Misalnya judul artikel selalu di dalam <h2>
        judul = judul_tag.get_text(strip=True) if judul_tag else "Judul tidak ditemukan"
        url_berita = link_tag.get("href") if link_tag else "URL tidak ditemukan"

        # Detik biasanya tidak menampilkan ringkasan & tanggal langsung pada halaman utama
        ringkasan = "Ringkasan tidak tersedia pada halaman ini"
        tanggal = "Tanggal tidak tersedia pada halaman ini"

        article_format = f"Judul : {judul}\nTanggal Posting : {tanggal}\nRingkasan : {ringkasan}\nURL : {url_berita}\n"

        if not fungsi.does_file_exist(directory + "/artikel_detik.doc"):
            fungsi.create_new_file(directory + "/artikel_detik.doc")

        fungsi.write_to_file(directory + "/artikel_detik.doc", article_format)
        print(article_format)

main_scrapper("https://www.detik.com/tag/olahraga", "Hasil")