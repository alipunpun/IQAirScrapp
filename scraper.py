import cloudscraper
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

URL_JAKARTA = "https://www.iqair.com/indonesia/jakarta"

def scrape_jakarta():
    # Memodifikasi scraper agar lebih identik dengan browser Google Chrome di PC Windows
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile('iqair_data.csv')
    
    # Buka file CSV untuk menyimpan data
    with open('iqair_data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Kota', 'AQI']) # Header kolom jika file baru
            
        try:
            print("Mengambil data untuk Jakarta...")
            response = scraper.get(URL_JAKARTA)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Mengambil nilai AQI
                aqi_element = soup.find(class_="aqi-value__value")
                
                if aqi_element:
                    aqi_value = aqi_element.text.strip()
                    writer.writerow([now, 'Jakarta', aqi_value])
                    print(f"-> Sukses! AQI Jakarta saat ini: {aqi_value}")
                else:
                    print("-> Gagal menemukan elemen HTML AQI. Struktur web mungkin berubah.")
            else:
                print(f"-> Diblokir/Error. Status Code: {response.status_code}")
                print("-> Info: Jika terus 429, berarti IP GitHub Actions sedang dilimit oleh IQAir.")
                
        except Exception as e:
            print(f"-> Terjadi error: {e}")

if __name__ == "__main__":
    scrape_jakarta()
