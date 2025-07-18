import requests
from bs4 import BeautifulSoup
import os
import fungsi

# Buat folder hasil
def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Level 1: Ambil daftar subkategori dari halaman utama
def scrape_categories(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Gagal akses base URL: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    kategori_links = soup.select("nav a[href^='https://']")  # fleksibel dan lebih aman

    kategori_urls = []
    for a in kategori_links:
        href = a.get("href")
        if href not in kategori_urls:
            kategori_urls.append(href)
    return kategori_urls

# Level 2: Ambil daftar artikel dari subkategori
def scrape_article_links(kategori_url):
    try:
        response = requests.get(kategori_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Gagal akses kategori: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    entries = soup.find_all("article")
    links = []
    for entry in entries:
        a_tag = entry.find("a")
        if a_tag and a_tag.get("href") and a_tag["href"].startswith("https://"):
            links.append(a_tag["href"])
    return links

# Level 3: Ambil isi konten artikel
def scrape_article_detail(article_url, folder="Hasil"):
    try:
        response = requests.get(article_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Gagal akses artikel: {e}")
        return

# Level 3: Ambil isi konten artikel
def scrape_article_detail(article_url, folder="Hasil"):
    try:
        response = requests.get(article_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Gagal akses artikel: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
# Gunakan fallback untuk struktur HTML yang berbeda-beda
    content = soup.find("article") or soup.find("div", class_="detail__body-text") or soup.find("div", class_="itp_bodycontent")
    if not content:
        print("Konten tidak ditemukan.")
        return

# Tambahkan judul artikel
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

    paragraphs = content.find_all("p")
    ensure_folder_exists(folder)
    filepath = os.path.join(folder, "artikel.txt")
    fungsi.write_to_file(filepath, f"\nURL: {article_url}\n")
    fungsi.write_to_file(filepath, f"Judul: {title}\n\n")

    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:
            fungsi.write_to_file(filepath, text + "\n")
    fungsi.write_to_file(filepath, "===============\n")

    soup = BeautifulSoup(response.text, "html.parser")
    # Gunakan fallback untuk struktur HTML yang berbeda-beda
    content = soup.find("article") or soup.find("div", class_="detail__body-text") or soup.find("div", class_="itp_bodycontent")
    if not content:
        print("Konten tidak ditemukan.")
        return

    paragraphs = content.find_all("p")
    ensure_folder_exists(folder)
    filepath = os.path.join(folder, "artikel.txt")
    fungsi.write_to_file(filepath, f"\nURL: {article_url}\n")

    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:
            fungsi.write_to_file(filepath, text + "\n")
    fungsi.write_to_file(filepath, "===============\n")

# Jalankan scraping multi-level
def scrape_multilevel(base_url):
    kategori_urls = scrape_categories(base_url)
    for kategori in kategori_urls:
        print(f"[Kategori] {kategori}")
        artikel_links = scrape_article_links(kategori)
        for artikel in artikel_links:
            print(f"  ↳ Scraping: {artikel}")
            scrape_article_detail(artikel)

if __name__ == "__main__":
    scrape_multilevel("https://www.detik.com/")