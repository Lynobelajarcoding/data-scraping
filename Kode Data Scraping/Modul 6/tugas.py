import pandas as pd

# URL sumber data
url = 'https://www.w3schools.com/html/html_tables.asp'

# Ambil semua tabel HTML dari halaman
tables = pd.read_html(url, header=0)

# Ambil tabel pertama yang berisi data "Contact Information"
df = tables[0]

# Tampilkan DataFrame asli
print("📋 Sebelum sorting dan filtering:")
print(df)

# 🎯 Tambahkan kolom baru: jumlah huruf di Contact dan Country
df["Contact_Length"] = df["Contact"].apply(len)
df["Country_Length"] = df["Country"].apply(len)
df["Total_Length"] = df["Contact_Length"] + df["Country_Length"]

# 🔡 Sorting berdasarkan kolom "Country"
df_sorted = df.sort_values("Country")

# 🔍 Filtering data hanya yang berasal dari "Germany"
df_filtered = df[df["Country"] == "Germany"]

# 💾 Simpan hasil ke file
df_sorted.to_csv("output_sorted.csv", index=False)
df_filtered.to_excel("output_filtered.xlsx", index=False)

# 🖨️ Tampilkan hasil akhir
print("\n📊 Setelah sorting dan filtering:")
print("Data Terurut:")
print(df_sorted)
print("\nData Germany Saja:")
print(df_filtered)