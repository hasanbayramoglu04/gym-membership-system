# Sistem Mimarisi ve Veri Modeli

## 1. Mimari Yapı
- **Backend:** Python 3.11 & Flask Web Framework
- **Veritabanı:** SQLite (`gym.db`)
- **Konteynerleştirme:** Docker
- **CI/CD:** GitHub Actions (Otomatik Pytest)
- **Cloud Platform:** Render (PaaS)

## 2. Veri Modeli (`members` Tablosu - v1.0)
| Alan Adı | Veri Tipi | Açıklama |
| :--- | :--- | :--- |
| `id` | INTEGER (PK) | Otomatik artan benzersiz üye numarası |
| `name` | TEXT | Üyenin adı ve soyadı |
| `phone` | TEXT | Üyenin iletişim numarası |
| `plan` | TEXT | Üyelik paketi (`1 Aylik`, `3 Aylik`, `12 Aylik`) |
| `end_date` | TEXT | Üyelik bitiş tarihi (`YYYY-MM-DD`) |
| `visit_count` | INTEGER | Toplam salona giriş (check-in) sayısı |
| `last_visit` | TEXT | Son salona giriş tarih ve saati |