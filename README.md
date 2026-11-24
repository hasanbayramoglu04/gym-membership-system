# Spor Salonu Üyelik, Giriş ve Antrenman Takip Sistemi (Gym Membership System)

Modern Yazılım Mühendisliği - Bulut ve DevOps dersi kapsamında geliştirilmiş; Agile (Kanban), Git branching, otomatik test (Pytest), CI/CD (GitHub Actions), Docker ve Bulut dağıtım süreçleri uygulanmış web uygulamasıdır.

## Sistem Fonksiyonları (Toplam 12 Fonksiyon)

1. **Yeni Üye Kaydı (`POST /add`):** Üyenin ad-soyad, telefon, üyelik paketi (1 Aylık, 3 Aylık, 12 Aylık) ve bitiş tarihi bilgilerini kaydeder.
2. **Üye Listeleme ve Durum Kontrolü (`GET /`):** Kayıtlı üyeleri güncel tarihe göre **Aktif** veya **Süresi Dolmuş** statüsünde listeler.
3. **Salona Giriş Kontrolü / Check-in (`POST /checkin/<id>`):** Üyenin salona girişini kaydeder, toplam ziyaret sayısını (`visit_count`) ve son giriş saatini günceller. Üyeliğin süresi dolmuşsa girişi reddeder.
4. **Üyelik Süresi Uzatma (`POST /renew/<id>`):** Mevcut üyeliğin bitiş tarihini 30 gün ileriye uzatır.
5. **Üye Kaydı Silme (`POST /delete/<id>`):** Seçilen üye kaydını veritabanından kalıcı olarak siler.
6. **Sistem Sağlık Kontrolü (`GET /health`):** Bulut izleme sistemleri için uygulamanın ayakta olduğunu doğrulayan JSON yanıtı (`{"status": "healthy"}`) döner.
7. **İsme Göre Arama (`GET /?q=...`):** Kayıtlı üyeler arasında isme göre hızlı arama yapar.
8. **Üyelik Durumuna Göre Filtreleme (`GET /?status=...`):** Üyeleri aktif, dondurulmuş veya süresi dolan statülerine göre filtreler.
9. **Paket Yükseltme / VIP Geçişi (`POST /upgrade/<id>`):** Üyenin paketini 12 Aylık VIP pakete yükseltir ve bitiş tarihini 365 gün olarak günceller.
10. **Canlı İstatistik ve Ciro Panosu:** Toplam, aktif, dondurulmuş ve süresi dolan üye sayıları ile paket bazlı tahmini toplam ciroyu (TL) dinamik olarak hesaplar.
11. **Vücut Kitle İndeksi (VKİ / BMI) Ölçümü (`POST /bmi/<id>`):** Girilen boy ve kilo değerlerine göre üyenin VKİ skorunu hesaplar ve sağlık kategorisini (*Zayıf*, *Normal*, *Fazla Kilolu*, *Obez*) kaydeder.
12. **Üyelik Dondurma ve Antrenör Atama (`POST /toggle-freeze/<id>`, `POST /assign-trainer/<id>`):** Üyeliği dondurur/aktifleştirir ve üyeye uzman antrenör ile antrenman programı atar.

## Kullanılan Teknolojiler
- **Backend:** Python 3.11, Flask, Gunicorn
- **Veritabanı:** SQLite (`gym.db`)
- **Test & CI/CD:** Pytest, GitHub Actions
- **Konteyner & Bulut:** Docker, Render (PaaS)

## Yerelde Çalıştırma
```bash
pip install -r requirements.txt
python src/app.py