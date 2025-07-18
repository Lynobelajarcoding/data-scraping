import requests
import os
from bs4 import BeautifulSoup

url = 'https://indonesiakaya.com/rangkai-pustaka/cerita-rakyat/'
# mengambil halaman web
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# mencari semua <img> yang memiliki kelas "zoom_it"
images = []
for img in soup.find_all('img', class_='zoom_it'):
    img_url = img.get('src')  # atribut yang benar untuk URL
    if img_url is not None and img_url.endswith(('.jpg', '.png', '.gif')):
        images.append(img_url)

# lokasi penyimpanan yang Anda sebutkan
save_path = r'\Hasil'
if not os.path.exists(save_path):
    os.makedirs(save_path)

for img_url in images:
    # download konten gambarnya
    response = requests.get(img_url)
    # ambil nama file dari URL
    filename = os.path.basename(img_url)
    filepath = os.path.join(save_path, filename)
    # simpan file dalam mode binary
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"{filename} berhasil disimpan pada direktori {save_path}")