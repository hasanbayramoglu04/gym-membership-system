# Spor Salonu Uyelik Yonetim Sistemi (Gym Membership System)

Modern Yazilim Muhendisligi - Bulut ve DevOps dersi kapsaminda gelistirilmis mini web uygulamasidir.

## Temel Fonksiyonlar
1. Yeni uye kaydi olusturma
2. Kayitli uyeleri ve uyelik durumlarini listeleme
3. Uyelik suresini 30 gun uzatma
4. Uye kaydini silme
5. Sistem saglik kontrolu (/health endpoint)

## Yerelde Calistirma
pip install -r requirements.txt
python src/app.py

## Docker ile Calistirma
docker build -t gym-app .
docker run -p 5000:5000 gym-app

## Canli Uygulama Linki (Cloud)
- Uygulama URL: (4. Haftada eklenecek)
