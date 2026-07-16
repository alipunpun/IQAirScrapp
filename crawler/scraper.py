import cloudscraper
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import time

# Daftar kota yang ingin kamu scrap (kamu bisa tambah atau ganti sesuai URL di IQAir)
KOTA_LIST = [
    {"nama": "Jakarta", "url": "https://www.iqair.com/indonesia/jakarta"},
    {"nama": "Hanoi", "url": "https://www.iqair.com/vietnam/hanoi"},
    {"nama": "Ho Chi Minh", "url": "https://www.iqair.com/vietnam/ho-chi-minh-city"}
]

def scrape_all_cities():
    # Membuat session anti-bot Cloudflare
    scraper = cloudscraper.create_scraper(delay=10)
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile('iqair_data.csv')
    
    # Buka file CSV untuk menyimpan data
    with open('iqair_data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Kota', 'AQI']) # Header kolom jika file baru
            
        for kota in KOTA_LIST:
            try:
                print(f"Mengambil data untuk {kota['nama']}...")
                response = scraper.get(kota['url'])
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Mengambil nilai AQI dari class HTML IQAir
                    aqi_element = soup.find(class_="aqi-value__value")
                    
                    if aqi_element:
                        aqi_value = aqi_element.text.strip()
                        writer.writerow([now, kota['nama'], aqi_value])
                        print(f"-> Sukses! AQI {kota['nama']}: {aqi_value}")
                    else:
                        print(f"-> Gagal menemukan elemen elemen HTML AQI di kota {kota['nama']}.")
                else:
                    print(f"-> Diblokir/Error di kota {kota['nama']}. Status Code: {response.status_code}")
                
                # Jeda 2 detik antar kota agar tidak dianggap spamming oleh server IQAir
                time.sleep(2)
                
            except Exception as e:
                print(f"-> Terjadi error pada kota {kota['nama']}: {e}")

if __name__ == "__main__":
    scrape_all_cities()
