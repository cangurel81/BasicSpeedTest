# ⚡ Basic Speed Test (v1.2)

A modern, high-performance, and sleek dark-themed internet speed testing application. Now featuring **Animated Gauges**, **Multi-Provider Support**, and **High-Precision Measurement**!

---
## 🇹🇷 Türkçe

### 🖥️ Özellikler
- **🚀 3 Farklı Test Sağlayıcısı:** Ookla (Speedtest), Cloudflare ve LibreSpeed arasından seçim yapabilme.
- **🎨 Animasyonlu Göstergeler:** Download ve upload hızını canlı, dairesel ve modern göstergelerle takip edin.
- **📈 Yüksek Hassasiyetli Ölçüm:** Delta-zaman tabanlı yeni algoritma ile milisaniyelik doğrulukta hız ölçümü.
- **🇹🇷 Çift Dil Desteği (TR/EN):** Arayüz üzerinden anlık dil değiştirme ve tercihlerin kaydedilmesi.
- **⏱️ Zamanlanmış Otomatik Test:** 1 dakikadan 4 saate kadar belirlediğiniz aralıklarla periyodik test yapma.
- **🔍 Detaylı IP ve Güvenlik Bilgisi:** IP, Konum, ISP, AS Numarası ve VPN/Proxy kontrolü.
- **📋 Gelişmiş Test Geçmişi:** Son 20 testin detaylı tablosu ve temizleme seçeneği.

<img width="729" height="719" alt="Ekran görüntüsü 2026-03-30 221158" src="https://github.com/user-attachments/assets/c15d31bc-b0ba-417d-88a9-ed4cb0c44155" />

### 🚀 Kullanım
**Python ile Çalıştırma:**
```bash
pip install -r requirements.txt
python speed_test.py
```

**EXE Yapma:**
`PyInstaller` kullanırken şu komutla derlemeniz önerilir (hataları önlemek için):
```bash
pyinstaller --noconfirm --onefile --windowed --add-data "sphere.png;." --add-data "sphere.ico;." --icon "sphere.ico" --collect-all speedtest speed_test.py
```
*Not: v1.2 sürümüyle birlikte EXE çevirme sırasında oluşan `fileno` ve `__builtin__` hataları kod seviyesinde giderilmiştir.*

---
## 🇬🇧 English

### 🖥️ Features
- **🚀 3 Test Providers:** Choose between Ookla (Speedtest), Cloudflare, and LibreSpeed for your tests.
- **🎨 Animated Gauges:** Track download and upload speeds with sleek, modern, and animated circular gauges.
- **📈 High-Precision Measurement:** New delta-time based algorithm providing millisecond-level speed accuracy.
- **🇬🇧 Bilingual Support (EN/TR):** Instant language switching with persistent user preferences.
- **⏱️ Scheduled Automated Testing:** Automatically run tests at intervals ranging from 1 minute to 4 hours.
- **🔍 Detailed IP & Security Info:** Displays IP, Location, ISP, AS Number, and VPN/Proxy detection.
- **📋 Advanced Test History:** Detailed table of your last 20 tests with a clear-all option.

<img width="725" height="717" alt="Ekran görüntüsü 2026-03-30 221208" src="https://github.com/user-attachments/assets/713d228a-bfbe-4606-985b-47b85ae6e0bc" />

### 🚀 Getting Started
**Running via Python:**
```bash
pip install -r requirements.txt
python speed_test.py
```

**Creating an EXE:**
When using `PyInstaller`, the following command is recommended to avoid common errors:
```bash
pyinstaller --noconfirm --onefile --windowed --add-data "sphere.png;." --add-data "sphere.ico;." --icon "sphere.ico" --collect-all speedtest speed_test.py
```
*Note: The `fileno` and `__builtin__` errors encountered during EXE conversion have been addressed in the code for v1.2.*
